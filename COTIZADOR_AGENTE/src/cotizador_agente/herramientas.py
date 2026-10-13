"""Herramientas que el agente conversacional llama para todo cálculo técnico.

Cada herramienta envuelve funciones determinísticas ya probadas (viento.py,
criterio_tecnico.py, vano.py) y devuelve un dict serializable a JSON. El modelo de
IA no calcula: pregunta, llama estas herramientas y explica el resultado.

El despiece, los cortes y los precios NO están aquí: los hace el software de
cotización integrado (motor), por decisión de Dirección General (2026-10-13).
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .criterio_tecnico import DATOS, NormaK4, Sistema, _paso_superior, kgm2_a_knm2
from .modelos import ErrorCotizacion, FallaMotor, RespuestaCotizacion, SolicitudCotizacion
from .motor.base import MotorCotizacion
from .pdf_cotizacion import Empresa, FichaTecnicaItem, generar_pdf
from .vano import distribuir_vano
from .viento import _normalizar, presion_diseno, region_de_ciudad

# Series fuera del portafolio (Dirección General): no se cargan ni se ofrecen.
FUERA_DE_ALCANCE = {
    "serie 35 corrediza": "La Ventanería no maneja la Serie 35 corrediza (decisión de Dirección General).",
    "koncept 55": "La Koncept 55 plegable no tiene tabla de presión en su ficha: se escala a Ingeniería.",
}

FACTOR_ESQUINA_ALUMINA = 1.35  # nota de los planos TR de Alúmina: zona 5 = zona 4 × 1.35

_NORMA = NormaK4()


@dataclass
class Sesion:
    """Estado de una conversación: motor conectado y última cotización recibida."""
    motor: MotorCotizacion | None = None
    carpeta_pdf: Path = Path("cotizaciones")
    empresa: Empresa | None = None
    ultima_solicitud: SolicitudCotizacion | None = None
    ultima_respuesta: RespuestaCotizacion | None = None


def _codigos_sistemas() -> list[str]:
    return sorted(p.stem for p in (DATOS / "sistemas").glob("*.json"))


def _grupos(datos: dict) -> dict[str, dict]:
    return {n: g for n, g in datos.items() if isinstance(g, dict) and "orden" in g}


def _referencia_alumina() -> dict:
    datos = json.loads((DATOS / "sistemas" / "alumina_vc8025.json").read_text(encoding="utf-8"))
    return datos["referencia_alumina"]["presion_por_ciudad_kgm2"]


# --- Herramientas -----------------------------------------------------------------

def presion_viento(ciudad: str, altura_edificio_m: float, ancho_m: float, alto_m: float,
                   departamento: str | None = None, zona: int = 5) -> dict:
    """Presión de diseño NSR-10 (B.6) para un elemento de ancho_m × alto_m.

    Si Alúmina publica tabla para la ciudad, usa el mayor valor entre la NSR-10 y esa
    tabla (LV-ING-REF-003), con la altura redondeada hacia arriba.
    """
    region = region_de_ciudad(ciudad, departamento)
    if region is None:
        return {"error": f"No se encontró la región de viento de '{ciudad}'. Pida el departamento "
                         "para usar la región máxima del departamento, o escale a Ingeniería."}
    p = presion_diseno(region["region"], altura_edificio_m, area_efectiva_m2=ancho_m * alto_m, zona=zona)
    resultado = {
        "region": region["region"], "V_ms": region["V_ms"], "criterio_region": region["criterio"],
        "presion_nsr10_kgm2": round(p.presion_kgm2), "metodo": p.metodo, "detalle": p.detalle,
    }
    diseno = p.presion_kgm2
    ref = _referencia_alumina()
    clave = _normalizar(ciudad)
    if clave in ref:
        altura = _paso_superior(altura_edificio_m, ref["alturas_m"]) or ref["alturas_m"][-1]
        valor = ref[clave][ref["alturas_m"].index(altura)] * (FACTOR_ESQUINA_ALUMINA if zona == 5 else 1)
        resultado["presion_tabla_alumina_kgm2"] = round(valor)
        diseno = max(diseno, valor)
    resultado["presion_diseno_kgm2"] = round(diseno)
    resultado["presion_diseno_knm2"] = round(kgm2_a_knm2(diseno), 3)
    resultado["referencia"] = "NSR-10 B.6 (LV-ING-REF-003); mayor valor entre NSR-10 y tabla Alúmina"
    return resultado


def listar_sistemas() -> dict:
    """Series cargadas, su uso, configuraciones y los grupos de perfiles que se verifican."""
    sistemas = []
    for codigo in _codigos_sistemas():
        datos = json.loads((DATOS / "sistemas" / f"{codigo}.json").read_text(encoding="utf-8"))
        sistemas.append({
            "codigo": codigo,
            "nombre": datos["nombre"],
            "caracteristicas": datos.get("caracteristicas", {}),
            "como_leer_medidas": datos.get("_convenciones", ""),
            "grupos_verificables": {
                n: {"descripcion": g.get("_descripcion", ""), "opciones": [v["codigo"] for v in g["orden"]]}
                for n, g in _grupos(datos).items()
            },
        })
    return {"sistemas": sistemas, "fuera_de_alcance": FUERA_DE_ALCANCE}


def verificar_perfil(sistema: str, grupo: str, ancho_m: float, alto_m: float, presion_kgm2: float) -> dict:
    """Escoge la opción más liviana del grupo (enganche, cierre, vertical...) que resiste."""
    s = Sistema(sistema)
    if grupo not in _grupos(s.datos):
        return {"error": f"El sistema {sistema} no tiene el grupo '{grupo}'. "
                         f"Grupos: {', '.join(_grupos(s.datos))}"}
    r = s.seleccionar_variante(grupo, ancho_m, alto_m, presion_kgm2)
    sel = r["seleccion"]
    return {
        "sistema": s.nombre, "grupo": grupo, "presion_requerida_kgm2": round(presion_kgm2),
        "resiste": sel is not None,
        "seleccion": None if sel is None else {
            "codigo": sel["codigo"], "descripcion": sel.get("descripcion", ""),
            "perfiles": sel.get("perfiles", []), "resiste_kgm2": r["resiste_kgm2"],
        },
        "evaluadas": r["evaluadas"],
        "accion_si_no_resiste": "Proponer naves más angostas, otra serie o escalar a Ingeniería.",
        "referencia": f"Ficha técnica {s.nombre} (LV-ING-REF-005/006)",
    }


def comparar_series(ancho_nave_m: float, alto_m: float, presion_kgm2: float, grupo: str = "enganches") -> dict:
    """Corre el mismo grupo en todas las series que lo tienen, para proponer la más adecuada."""
    filas = []
    for codigo in _codigos_sistemas():
        s = Sistema(codigo)
        if grupo not in _grupos(s.datos):
            continue
        r = s.seleccionar_variante(grupo, ancho_nave_m, alto_m, presion_kgm2)
        filas.append({
            "sistema": codigo, "nombre": s.nombre,
            "resiste": r["seleccion"] is not None,
            "opcion": r["seleccion"]["codigo"] if r["seleccion"] else None,
            "resiste_kgm2": r["resiste_kgm2"],
            "maximo_tabla_kgm2": max((e["resiste_kgm2"] for e in r["evaluadas"] if e["resiste_kgm2"]), default=None),
        })
    return {"grupo": grupo, "presion_requerida_kgm2": round(presion_kgm2), "series": filas,
            "nota": "Medidas fuera de la tabla de una serie dan 'resiste: false' y maximo_tabla null."}


def vidrio_por_viento(ancho_mm: float, alto_mm: float, presion_kgm2: float) -> dict:
    """Espesor mínimo por viento de cada tipo de vidrio (NSR-10 K.4.2, tablas K.4.2-2 a K.4.2-5)."""
    knm2 = kgm2_a_knm2(presion_kgm2)
    tipos = {}
    for tipo in ("recocido", "templado", "laminado_pvb"):
        espesor = _NORMA.espesor_minimo_por_viento(tipo, ancho_mm, alto_mm, knm2)
        v = (_NORMA.verificar_vidrio_por_viento(tipo, espesor, ancho_mm, alto_mm, knm2) if espesor
             else _NORMA.verificar_vidrio_por_viento(tipo, _NORMA.datos["areas_maximas_por_viento"][tipo]
                                                     ["espesores_mm"][-1], ancho_mm, alto_mm, knm2))
        tipos[tipo] = {"espesor_minimo_mm": espesor, "detalle": v.detalle, "referencia": v.referencia}
    return {"area_m2": round(ancho_mm * alto_mm / 1e6, 3), "presion_knm2": round(knm2, 3), "por_tipo": tipos,
            "nota": "espesor_minimo_mm null = fuera de tabla: calcular por ASTM E1300 o escalar a Ingeniería."}


def vidrio_seguridad(uso: str, tipo_vidrio: str, altura_inferior_mm: float, edificacion: str = "vivienda") -> dict:
    """Exigencias de vidrio de seguridad por uso y altura (NSR-10 K.4.3.9)."""
    return asdict(_NORMA.verificar_seguridad(uso, tipo_vidrio, altura_inferior_mm, edificacion))


def distribuir_vano_tool(ancho_mm: float, alto_vano_mm: float, altura_muro_mm: float = 0,
                         desnivel_exterior: bool = True, alto_max_ventana_mm: float | None = None,
                         fijo_superior_mm: float = 0, fijo_inferior_solicitado: bool = False,
                         travesano_mm: float = 1100, edificacion: str = "vivienda") -> dict:
    """Reparte el vano en fijo inferior, ventana y fijo superior (NSR-10 K.4.3.9.7)."""
    d = distribuir_vano(ancho_mm, alto_vano_mm, altura_muro_mm, desnivel_exterior, alto_max_ventana_mm,
                        fijo_superior_mm, fijo_inferior_solicitado, travesano_mm, edificacion)
    return {
        "franjas": [{**asdict(f), "alto_mm": f.alto_mm} for f in d.franjas],
        "avisos": d.avisos,
        "referencia": "NSR-10 K.4.3.9.7, Tabla K.4.3-7 (LV-ING-REF-006)",
    }


def enviar_a_cotizar(sesion: Sesion, solicitud: dict) -> dict:
    """Valida la solicitud y la envía al software de cotización (despiece y precios)."""
    try:
        s = SolicitudCotizacion.model_validate(solicitud)
    except ValueError as e:
        return {"error": f"Solicitud inválida: {e}"}
    if sesion.motor is None:
        return {"estado": "pendiente_motor", "solicitud": s.model_dump(),
                "nota": "No hay software de cotización conectado: la solicitud quedó lista para enviarse."}
    try:
        respuesta = sesion.motor.cotizar(s)
    except ErrorCotizacion as e:
        return {"error": e.mensaje, "codigo": e.codigo, "indice_item": e.indice_item}
    except FallaMotor as e:
        return {"error": f"El software de cotización no respondió: {e}. Reintentar más tarde."}
    sesion.ultima_solicitud, sesion.ultima_respuesta = s, respuesta
    return {"estado": "cotizada", "respuesta": respuesta.model_dump()}


def generar_pdf_cotizacion(sesion: Sesion, cliente: str, fichas_tecnicas: list[dict]) -> dict:
    """PDF de la última cotización: precios del software y especificación técnica del agente."""
    if sesion.ultima_respuesta is None:
        return {"error": "Primero hay que cotizar con enviar_a_cotizar: el PDF usa los precios del software."}
    fichas = [FichaTecnicaItem.model_validate(f) for f in fichas_tecnicas]
    indices = {it.indice for it in sesion.ultima_respuesta.items}
    sobrantes = [f.indice for f in fichas if f.indice not in indices]
    if sobrantes:
        return {"error": f"Fichas con índices que no están en la cotización: {sobrantes}. Índices válidos: "
                         f"{sorted(indices)}"}
    r = sesion.ultima_respuesta
    nombre = "".join(c if c.isalnum() or c in "-_" else "_" for c in f"cotizacion_{r.cotizacion_id}")
    ruta = generar_pdf(r, fichas, sesion.carpeta_pdf / f"{nombre}.pdf", cliente,
                       sesion.ultima_solicitud.ciudad, sesion.empresa)
    return {"estado": "pdf_generado", "archivo": str(ruta), "cotizacion_id": r.cotizacion_id, "total": r.total}


# --- Definiciones para la API de Claude --------------------------------------------

_NUM = {"type": "number"}

DEFINICIONES = [
    {
        "name": "presion_viento",
        "description": "Presión de viento de diseño NSR-10 para un elemento (nave o paño) en una ciudad y altura "
                       "de edificio. Devuelve kg/m² y kN/m². Úsela antes de cualquier verificación de perfiles o vidrio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {"type": "string"},
                "departamento": {"type": "string", "description": "Opcional; si la ciudad no está en la tabla."},
                "altura_edificio_m": {**_NUM, "description": "Altura total del edificio en m (unos 3 m por piso)."},
                "ancho_m": {**_NUM, "description": "Ancho del elemento que recibe el viento (nave), m."},
                "alto_m": {**_NUM, "description": "Alto del elemento, m."},
                "zona": {"type": "integer", "enum": [4, 5], "description": "5 = esquina (por defecto), 4 = interior."},
            },
            "required": ["ciudad", "altura_edificio_m", "ancho_m", "alto_m"],
        },
    },
    {
        "name": "listar_sistemas",
        "description": "Lista las series de perfilería cargadas, su uso, configuraciones, cómo se leen sus medidas "
                       "y los grupos de perfiles verificables (enganches, cierres, verticales, horizontales, uniones).",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "comparar_series",
        "description": "Evalúa un mismo grupo (por defecto 'enganches') en todas las series que lo tienen, para "
                       "proponer la serie más liviana que resiste la presión.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ancho_nave_m": _NUM, "alto_m": _NUM, "presion_kgm2": _NUM,
                "grupo": {"type": "string"},
            },
            "required": ["ancho_nave_m", "alto_m", "presion_kgm2"],
        },
    },
    {
        "name": "verificar_perfil",
        "description": "En una serie, escoge la opción más liviana de un grupo (enganche, cierre central, vertical, "
                       "horizontal, unión) que resiste la presión. ancho_m y alto_m según 'como_leer_medidas'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sistema": {"type": "string", "description": "Código de listar_sistemas, p. ej. 'koncept_70'."},
                "grupo": {"type": "string"},
                "ancho_m": _NUM, "alto_m": _NUM, "presion_kgm2": _NUM,
            },
            "required": ["sistema", "grupo", "ancho_m", "alto_m", "presion_kgm2"],
        },
    },
    {
        "name": "vidrio_por_viento",
        "description": "Espesor mínimo por viento de vidrio recocido, templado y laminado para un paño.",
        "input_schema": {
            "type": "object",
            "properties": {"ancho_mm": _NUM, "alto_mm": _NUM, "presion_kgm2": _NUM},
            "required": ["ancho_mm", "alto_mm", "presion_kgm2"],
        },
    },
    {
        "name": "vidrio_seguridad",
        "description": "Revisa si el uso o la altura exigen vidrio de seguridad (NSR-10 K.4.3.9).",
        "input_schema": {
            "type": "object",
            "properties": {
                "uso": {"type": "string", "enum": ["ventana", "puerta_batiente", "puerta_corrediza", "division_bano",
                                                   "puerta_ducha", "baranda", "piso", "claraboya", "fachada"]},
                "tipo_vidrio": {"type": "string", "enum": ["recocido", "templado", "laminado_pvb", "termoendurecido"]},
                "altura_inferior_mm": {**_NUM, "description": "Altura del borde inferior del vidrio sobre el piso."},
                "edificacion": {"type": "string", "enum": ["vivienda", "oficina", "comercio", "escuela", "otra"]},
            },
            "required": ["uso", "tipo_vidrio", "altura_inferior_mm"],
        },
    },
    {
        "name": "distribuir_vano",
        "description": "Reparte el alto del vano en fijo inferior, ventana y fijo superior según la NSR-10 "
                       "(travesaño de protección por defecto a 1100 mm) y propone el vidrio bajo el travesaño.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ancho_mm": _NUM,
                "alto_vano_mm": {**_NUM, "description": "Alto del vano libre, medido desde el tope del muro."},
                "altura_muro_mm": {**_NUM, "description": "Muro o antepecho desde piso terminado (0 si llega al piso)."},
                "desnivel_exterior": {"type": "boolean", "description": "Hay caída de 1 m o más al otro lado."},
                "alto_max_ventana_mm": {**_NUM, "description": "Alto máximo de la serie; el sobrante va a fijo superior."},
                "fijo_superior_mm": _NUM,
                "fijo_inferior_solicitado": {"type": "boolean"},
                "travesano_mm": {**_NUM, "description": "Entre 760 y 1100; por defecto 1100."},
                "edificacion": {"type": "string", "enum": ["vivienda", "oficina", "comercio", "escuela", "otra"]},
            },
            "required": ["ancho_mm", "alto_vano_mm"],
        },
    },
    {
        "name": "enviar_a_cotizar",
        "description": "Envía la solicitud final al software de cotización, que hace el despiece, los cortes y los "
                       "precios. Úsela solo cuando el cliente confirmó medidas, serie, vidrio y color.",
        "input_schema": {
            "type": "object",
            "properties": {
                "solicitud": {
                    "type": "object",
                    "properties": {
                        "referencia_cliente": {"type": "string"},
                        "ciudad": {"type": "string"},
                        "items": {"type": "array", "items": {
                            "type": "object",
                            "properties": {
                                "sistema": {"type": "string"}, "ancho_mm": {"type": "integer"},
                                "alto_mm": {"type": "integer"}, "cantidad": {"type": "integer"},
                                "vidrio": {"type": "string"}, "color_perfil": {"type": "string"},
                                "piso": {"type": "integer"},
                            },
                            "required": ["sistema", "ancho_mm", "alto_mm", "cantidad", "vidrio", "color_perfil", "piso"],
                        }},
                    },
                    "required": ["referencia_cliente", "ciudad", "items"],
                },
            },
            "required": ["solicitud"],
        },
    },
    {
        "name": "generar_pdf_cotizacion",
        "description": "Genera el PDF para el cliente con la última cotización del software (precios, IVA, total y "
                       "vigencia) y la especificación técnica que usted verificó. Úsela después de enviar_a_cotizar "
                       "cuando el cliente quiera el documento. Usted no escribe precios: salen del software.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cliente": {"type": "string", "description": "Nombre del cliente como debe aparecer en el PDF."},
                "fichas_tecnicas": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "indice": {"type": "integer", "description": "Índice del ítem en la cotización (desde 0)."},
                        "sistema": {"type": "string", "description": "Nombre de la serie, p. ej. 'Koncept 70 (Alúmina)'."},
                        "configuracion": {"type": "string"},
                        "presion_diseno_kgm2": {"type": "number"},
                        "perfiles": {"type": "array", "items": {"type": "string"},
                                     "description": "Opciones verificadas: enganche, cierre, verticales..."},
                        "franjas": {"type": "array", "items": {
                            "type": "object",
                            "properties": {"tipo": {"type": "string", "enum": ["fijo_inferior", "ventana", "fijo_superior"]},
                                           "alto_mm": {"type": "number"}, "vidrio": {"type": "string"}},
                            "required": ["tipo", "alto_mm"]}},
                        "vidrio": {"type": "string"},
                        "normas": {"type": "array", "items": {"type": "string"}},
                        "observaciones": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["indice", "sistema"]}},
            },
            "required": ["cliente", "fichas_tecnicas"],
        },
    },
]


def ejecutar(nombre: str, entrada: dict, sesion: Sesion | None = None) -> dict:
    """Despacha una llamada de herramienta del modelo. Lanza excepción si los datos no sirven."""
    sesion = sesion or Sesion()
    funciones = {
        "presion_viento": presion_viento,
        "listar_sistemas": listar_sistemas,
        "comparar_series": comparar_series,
        "verificar_perfil": verificar_perfil,
        "vidrio_por_viento": vidrio_por_viento,
        "vidrio_seguridad": vidrio_seguridad,
        "distribuir_vano": distribuir_vano_tool,
    }
    if nombre == "enviar_a_cotizar":
        return enviar_a_cotizar(sesion, entrada["solicitud"])
    if nombre == "generar_pdf_cotizacion":
        return generar_pdf_cotizacion(sesion, **entrada)
    if nombre not in funciones:
        raise ValueError(f"Herramienta desconocida: {nombre}")
    return funciones[nombre](**entrada)
