"""Cerebro técnico del agente: NSR-10 K.4 y fichas técnicas de sistemas.

Todo cálculo aquí es determinístico y sale de tablas en `datos/`. El agente de IA
nunca calcula ni inventa valores técnicos: llama a estas funciones y explica el
resultado citando el numeral de la norma o la ficha.

Criterio conservador en todas las búsquedas en tablas:
- Presión de diseño entre dos renglones -> se usa el renglón de presión mayor.
- Dimensión entre dos pasos de tabla -> se usa el paso mayor (menor resistencia).
- Fuera del rango publicado -> no se dictamina: se escala a Ingeniería.
"""

import ast
import json
import math
import operator
from dataclasses import dataclass, field
from pathlib import Path

DATOS = Path(__file__).parent / "datos"

KG_M2_A_KN_M2 = 9.80665 / 1000
PESO_VIDRIO_KG_M2_POR_MM = 2.5  # densidad 2500 kg/m3 (Tabla K.4.2-0)

PESOS_PERFILES = json.loads((DATOS / "pesos_perfiles.json").read_text(encoding="utf-8"))["perfiles"]


def kgm2_a_knm2(presion_kgm2: float) -> float:
    return presion_kgm2 * KG_M2_A_KN_M2


# --- Fórmulas de despiece ("A - 20", "A/2 - 46", "4*A + 4*H") ----------------

_OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluar(formula: str, **medidas: float) -> float:
    """Evalúa una fórmula de ficha técnica con solo + - * / y las medidas dadas."""

    def _eval(nodo):
        if isinstance(nodo, ast.Expression):
            return _eval(nodo.body)
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return nodo.value
        if isinstance(nodo, ast.Name) and nodo.id in medidas:
            return medidas[nodo.id]
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
            return _OPERADORES[type(nodo.op)](_eval(nodo.left), _eval(nodo.right))
        if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.USub):
            return -_eval(nodo.operand)
        raise ValueError(f"Fórmula no permitida: {formula!r}")

    return _eval(ast.parse(formula, mode="eval"))


# --- Resultado de una verificación ---------------------------------------------

@dataclass
class Verificacion:
    concepto: str
    cumple: bool | None  # None = fuera de tablas, lo decide Ingeniería
    detalle: str
    referencia: str

    @property
    def requiere_ingenieria(self) -> bool:
        return self.cumple is None


@dataclass
class Dictamen:
    verificaciones: list[Verificacion] = field(default_factory=list)

    @property
    def estado(self) -> str:
        if any(v.cumple is False for v in self.verificaciones):
            return "no_cumple"
        if any(v.cumple is None for v in self.verificaciones):
            return "requiere_ingenieria"
        return "cumple"


# --- NSR-10 Capítulo K.4 --------------------------------------------------------

class NormaK4:
    def __init__(self, ruta: Path = DATOS / "nsr10_k4.json"):
        self.datos = json.loads(ruta.read_text(encoding="utf-8"))

    def area_maxima_por_viento(self, tipo: str, espesor_mm: int, presion_knm2: float) -> float | None:
        """Tablas K.4.2-2 a K.4.2-5. None si el espesor o la presión están fuera de la tabla."""
        tabla = self.datos["areas_maximas_por_viento"][tipo]
        if espesor_mm not in tabla["espesores_mm"]:
            return None
        columna = tabla["espesores_mm"].index(espesor_mm)
        for fila in tabla["filas"]:
            if fila["presion"] >= presion_knm2 - 1e-9:
                return fila["areas"][columna]
        return None

    def verificar_vidrio_por_viento(
        self, tipo: str, espesor_mm: int, ancho_mm: float, alto_mm: float, presion_knm2: float
    ) -> Verificacion:
        tabla = self.datos["areas_maximas_por_viento"][tipo]["tabla"]
        referencia = f"NSR-10 K.4.2.6, tabla {tabla}"
        area = ancho_mm * alto_mm / 1e6
        relacion = max(ancho_mm, alto_mm) / min(ancho_mm, alto_mm)
        if relacion > 2:
            return Verificacion(
                "vidrio_viento", None,
                f"Relación largo/ancho {relacion:.2f} > 2: fuera del alcance de la tabla, "
                "requiere cálculo por ASTM E1300-09a.",
                referencia,
            )
        area_max = self.area_maxima_por_viento(tipo, espesor_mm, presion_knm2)
        if area_max is None:
            return Verificacion(
                "vidrio_viento", None,
                f"Sin valor tabulado para {tipo} {espesor_mm} mm a {presion_knm2:.2f} kN/m2.",
                referencia,
            )
        return Verificacion(
            "vidrio_viento", area <= area_max,
            f"Área {area:.2f} m2 vs máxima {area_max:.2f} m2 ({tipo} {espesor_mm} mm, "
            f"presión {presion_knm2:.2f} kN/m2).",
            referencia,
        )

    def espesor_minimo_por_viento(
        self, tipo: str, ancho_mm: float, alto_mm: float, presion_knm2: float
    ) -> int | None:
        for espesor in self.datos["areas_maximas_por_viento"][tipo]["espesores_mm"]:
            if self.verificar_vidrio_por_viento(tipo, espesor, ancho_mm, alto_mm, presion_knm2).cumple:
                return espesor
        return None

    def verificar_seguridad(
        self, uso: str, tipo_vidrio: str, altura_inferior_mm: float, edificacion: str = "vivienda"
    ) -> Verificacion:
        """Reglas de vidrio de seguridad (K.4.3.9). Simplificado: zonas de la figura K.4.3-0 por confirmar."""
        es_seguridad = tipo_vidrio in ("templado", "laminado_pvb")
        exige = {
            "puerta_batiente": "K.4.3.9.2.1",
            "division_bano": "K.4.3.9.6.1",
            "puerta_ducha": "K.4.3.9.6.4",
            "baranda": "K.4.3.9.9.1",
            "piso": "K.4.2.5.6.2",
        }
        if uso in exige:
            return Verificacion(
                "vidrio_seguridad", es_seguridad,
                f"Uso '{uso}' exige vidrio de seguridad.", f"NSR-10 {exige[uso]}",
            )
        if edificacion == "escuela" and altura_inferior_mm < 800:
            return Verificacion(
                "vidrio_seguridad", es_seguridad,
                "Escuelas y guarderías: vidrio de seguridad hasta 800 mm del piso.",
                "NSR-10 K.4.3.9.1.9",
            )
        if uso == "claraboya":
            return Verificacion(
                "vidrio_seguridad", None,
                "Vidrio inclinado o sobre cabeza: requiere diseño de Ingeniería.",
                "NSR-10 K.4.2.5.2",
            )
        if altura_inferior_mm < 500 and not es_seguridad:
            return Verificacion(
                "vidrio_seguridad", None,
                "Vidrio recocido a menos de 500 mm del piso: mínimo 5 mm y revisión de "
                "zona de riesgo de impacto con Ingeniería.",
                "NSR-10 K.4.3.9.5.1",
            )
        return Verificacion(
            "vidrio_seguridad", True,
            "Sin exigencia de vidrio de seguridad por uso o altura en las reglas cargadas.",
            "NSR-10 K.4.3.9",
        )


# --- Sistemas de perfilería (fichas técnicas) -----------------------------------

def _paso_superior(valor: float, pasos: list[float]) -> float | None:
    """Primer paso de la tabla >= valor; si el valor es menor que el mínimo, el mínimo."""
    for paso in pasos:
        if paso >= valor - 1e-9:
            return paso
    return None


def _leer_tabla(tabla: dict, ancho_m: float, alto_m: float) -> int | None:
    """Presión resistente de una tabla de ficha, redondeando las medidas hacia arriba."""
    columnas = tabla["columnas_m"]
    filas = sorted(float(h) for h in tabla["filas"])
    col = _paso_superior(ancho_m, columnas)
    fila = _paso_superior(alto_m, filas)
    if col is None or fila is None:
        return None
    return tabla["filas"][f"{fila:.2f}"][columnas.index(col)]


class Sistema:
    def __init__(self, codigo: str):
        ruta = DATOS / "sistemas" / f"{codigo}.json"
        self.datos = json.loads(ruta.read_text(encoding="utf-8"))
        self.codigo = codigo
        self.nombre = self.datos["nombre"]

    def configuracion(self, config: str) -> dict:
        try:
            return self.datos["configuraciones"][config]
        except KeyError:
            disponibles = ", ".join(self.datos["configuraciones"])
            raise ValueError(f"Configuración '{config}' no existe. Disponibles: {disponibles}")

    def presion_resistente(self, config: str, ancho_m: float, alto_m: float) -> int | None:
        tabla = self.configuracion(config).get("tabla_presion")
        return None if tabla is None else _leer_tabla(tabla, ancho_m, alto_m)

    def seleccionar_variante(
        self, grupo: str, ancho_nave_m: float, alto_m: float, presion_kgm2: float
    ) -> dict:
        """Escoge la variante más liviana del grupo (p. ej. enganches) que resiste la presión.

        Las variantes vienen ordenadas en la ficha de más liviana a más resistente.
        """
        evaluadas = []
        for variante in self.datos[grupo]["orden"]:
            resiste = _leer_tabla(variante["tabla"], ancho_nave_m, alto_m)
            evaluadas.append({"codigo": variante["codigo"], "resiste_kgm2": resiste})
            if resiste is not None and resiste >= presion_kgm2:
                return {"seleccion": variante, "resiste_kgm2": resiste, "evaluadas": evaluadas}
        return {"seleccion": None, "resiste_kgm2": None, "evaluadas": evaluadas}

    def verificar_presion(
        self, config: str, ancho_m: float, alto_m: float, presion_kgm2: float
    ) -> Verificacion:
        referencia = f"Ficha técnica {self.nombre}, tabla de presión resistente ({config})"
        resistente = self.presion_resistente(config, ancho_m, alto_m)
        if resistente is None:
            return Verificacion(
                "perfileria_viento", None,
                f"Medidas {ancho_m:.2f} x {alto_m:.2f} m fuera de la tabla de la ficha, "
                "o configuración sin tabla.",
                referencia,
            )
        return Verificacion(
            "perfileria_viento", resistente >= presion_kgm2,
            f"Resiste {resistente} kg/m2 vs requerida {presion_kgm2:.0f} kg/m2.",
            referencia,
        )

    def seleccionar_brazo(self, ancho_nave_mm: float, alto_nave_mm: float, peso_kg: float) -> dict | None:
        for brazo in self.datos.get("brazos_proyectante", {}).get("apertura_horizontal", []):
            if (ancho_nave_mm <= brazo["ancho_max_mm"] and alto_nave_mm <= brazo["alto_max_mm"]
                    and peso_kg <= brazo["peso_max_kg"]):
                return brazo
        return None

    def despiece(self, config: str, espesor_vidrio_mm: int, **medidas_mm: float) -> dict:
        """Cortes de perfiles, vidrios y accesorios para una unidad."""
        datos = self.configuracion(config)
        perfiles = []
        for p in datos["perfiles"]:
            medida = evaluar(p["formula"], **medidas_mm)
            kg_m = PESOS_PERFILES.get(p["ref"], {}).get("kg_m")
            perfiles.append({
                **p, "medida_mm": round(medida, 1), "kg_m": kg_m,
                "peso_kg": None if kg_m is None else round(medida / 1000 * p["cant"] * kg_m, 2),
            })
        vidrios = []
        for v in datos["vidrios"]:
            ancho = evaluar(v["ancho"], **medidas_mm)
            alto = evaluar(v["alto"], **medidas_mm)
            vidrios.append({
                "seccion": v["seccion"], "ancho_mm": round(ancho, 1), "alto_mm": round(alto, 1),
                "cant": v["cant"], "area_m2": round(ancho * alto / 1e6, 3),
                "peso_kg": round(ancho * alto / 1e6 * espesor_vidrio_mm * PESO_VIDRIO_KG_M2_POR_MM, 1),
            })
        empaque_u = self.datos.get("empaque_u_por_espesor", {}).get(str(espesor_vidrio_mm))
        accesorios = []
        for a in datos["accesorios"]:
            try:
                cant = evaluar(a["cant"], **medidas_mm)
            except ValueError:
                cant = None
            ref = empaque_u if a["ref"] == "EMPAQUE_U" else a["ref"]
            accesorios.append({**a, "ref": ref, "cant": cant if cant is None else math.ceil(cant)})
        sin_peso = sorted({p["ref"] for p in perfiles if p["kg_m"] is None})
        resultado = {
            "perfiles": perfiles, "vidrios": vidrios, "accesorios": accesorios,
            "peso_aluminio_kg": round(sum(p["peso_kg"] or 0 for p in perfiles), 2),
            "perfiles_sin_peso": sin_peso,
        }
        if "nave" in datos:
            ancho_nave = evaluar(datos["nave"]["ancho"], **medidas_mm)
            alto_nave = evaluar(datos["nave"]["alto"], **medidas_mm)
            peso_vidrio = sum(v["peso_kg"] for v in vidrios if v["seccion"] == "nave")
            peso_aluminio = sum(p["peso_kg"] or 0 for p in perfiles if p["descripcion"].startswith("Nave"))
            peso_nave = round(peso_vidrio + peso_aluminio, 1)
            resultado["brazo"] = self.seleccionar_brazo(ancho_nave, alto_nave, peso_nave)
            resultado["nave_mm"] = {
                "ancho": ancho_nave, "alto": alto_nave, "peso_vidrio_kg": peso_vidrio,
                "peso_aluminio_kg": round(peso_aluminio, 2), "peso_total_kg": peso_nave,
            }
        return resultado
