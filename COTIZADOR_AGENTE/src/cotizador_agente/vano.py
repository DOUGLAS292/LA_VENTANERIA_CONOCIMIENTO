"""Distribución vertical del vano: fijo inferior, ventana y fijo superior (NSR-10 K.4.3.9.7).

Cuando la ventana protege contra un desnivel de 1000 mm o más, la Tabla K.4.3-7 pide un
travesaño o riel de protección entre 760 y 1100 mm sobre el piso. Debajo del travesaño el
vidrio es "tipo B": de seguridad, o recocido de mínimo 5 mm dentro del área de la columna 2
(vivienda) o 3 (demás edificaciones) de la Tabla K.4.3-2. Encima del travesaño es "tipo C" y
se selecciona por viento.

Criterios de La Ventanería (Dirección General, 2026-10-10):
- Travesaño por defecto a 1100 mm (el máximo de la norma).
- Debajo del travesaño el agente usa recocido de 5 mm o más cuando la norma lo permite; si el
  área supera la tabla, pasa a vidrio de seguridad.
- Un muro o antepecho de 760 mm o más ya cumple como protección: no exige fijo inferior.

Medidas en mm. El alto del vano se mide desde la parte superior del muro (vano libre).
"""

from dataclasses import dataclass, field

from .criterio_tecnico import NormaK4

TRAVESANO_POR_DEFECTO = 1100
TRAVESANO_MIN, TRAVESANO_MAX = 760, 1100
DESNIVEL_PROTECCION = 1000
VIDRIO_BAJO = 500  # K.4.3.9.5.1: recocido a menos de 500 mm del piso, mínimo 5 mm


@dataclass
class Franja:
    tipo: str  # fijo_inferior | ventana | fijo_superior
    desde_mm: float
    hasta_mm: float
    vidrio: str = ""
    referencia: str = ""

    @property
    def alto_mm(self) -> float:
        return self.hasta_mm - self.desde_mm


@dataclass
class Distribucion:
    franjas: list[Franja]
    avisos: list[str] = field(default_factory=list)


def vidrio_bajo_travesano(ancho_mm: float, alto_mm: float, edificacion: str = "vivienda",
                          norma: NormaK4 | None = None) -> tuple[str, str]:
    """Vidrio 'tipo B' de la Tabla K.4.3-7: recocido de 5 mm o más si cabe en la Tabla K.4.3-2."""
    norma = norma or NormaK4()
    tabla = norma.datos["recocido_por_riesgo_impacto"]
    columna = "mediano" if edificacion == "vivienda" else "bajo"  # columna 2 o 3
    area = ancho_mm * alto_mm / 1e6
    for espesor, maxima in zip(tabla["espesores_mm"], tabla[columna]):
        if espesor >= 5 and area <= maxima:
            return (f"Recocido {espesor} mm (área {area:.2f} m² ≤ {maxima} m²), o vidrio de seguridad",
                    f"NSR-10 Tabla K.4.3-7 tipo B y Tabla K.4.3-2 columna {2 if columna == 'mediano' else 3}")
    return ("Vidrio de seguridad (templado o laminado): el área supera la tabla de recocido",
            "NSR-10 Tabla K.4.3-7 tipo B")


def distribuir_vano(
    ancho_mm: float,
    alto_vano_mm: float,
    altura_muro_mm: float = 0,
    desnivel_exterior: bool = True,
    alto_max_ventana_mm: float | None = None,
    fijo_superior_mm: float = 0,
    fijo_inferior_solicitado: bool = False,
    travesano_mm: float = TRAVESANO_POR_DEFECTO,
    edificacion: str = "vivienda",
) -> Distribucion:
    """Reparte el vano en fijo inferior, ventana y fijo superior.

    - desnivel_exterior: True si al otro lado hay una caída de 1000 mm o más (piso alto, balcón).
    - alto_max_ventana_mm: alto máximo de la serie; el sobrante pasa a fijo superior.
    - fijo_superior_mm: fijo superior que pide el cliente (0 = ninguno).
    - fijo_inferior_solicitado: el cliente quiere fijo inferior aunque la norma no lo exija.
    """
    if not TRAVESANO_MIN <= travesano_mm <= TRAVESANO_MAX:
        raise ValueError(f"El travesaño debe estar entre {TRAVESANO_MIN} y {TRAVESANO_MAX} mm (Tabla K.4.3-7)")
    base, tope = altura_muro_mm, altura_muro_mm + alto_vano_mm
    avisos = []

    exige = desnivel_exterior and base < TRAVESANO_MIN
    if exige or (fijo_inferior_solicitado and base < travesano_mm):
        corte_inferior = min(travesano_mm, tope)
        if exige:
            avisos.append(
                f"Desnivel de {DESNIVEL_PROTECCION} mm o más y muro de {base:.0f} mm: la NSR-10 exige "
                f"travesaño de protección; se coloca a {travesano_mm:.0f} mm del piso (fijo inferior)."
            )
    else:
        corte_inferior = base
        if desnivel_exterior:
            avisos.append(
                f"El muro de {base:.0f} mm ya cumple como protección (≥ {TRAVESANO_MIN} mm, Tabla K.4.3-7): "
                "no se exige fijo inferior."
            )

    corte_superior = tope - fijo_superior_mm
    if alto_max_ventana_mm and corte_superior - corte_inferior > alto_max_ventana_mm:
        corte_superior = corte_inferior + alto_max_ventana_mm
        avisos.append(f"La ventana supera el alto máximo de la serie ({alto_max_ventana_mm:.0f} mm): "
                      "el sobrante pasa a fijo superior.")
    if corte_superior <= corte_inferior:
        raise ValueError("No queda alto para la ventana: revise el vano, el muro y los fijos")

    franjas = []
    if corte_inferior > base:
        vidrio, ref = vidrio_bajo_travesano(ancho_mm, corte_inferior - base, edificacion)
        franjas.append(Franja("fijo_inferior", base, corte_inferior, vidrio, ref))
    vidrio_ventana = "Por viento (tipo C, Tabla K.4.3-7)" if desnivel_exterior else "Por viento"
    ref_ventana = "NSR-10 K.4.2"
    if corte_inferior < VIDRIO_BAJO:
        vidrio_ventana += "; recocido de mínimo 5 mm por estar a menos de 500 mm del piso"
        ref_ventana = "NSR-10 K.4.3.9.5.1"
    franjas.append(Franja("ventana", corte_inferior, corte_superior, vidrio_ventana, ref_ventana))
    if tope > corte_superior:
        franjas.append(Franja("fijo_superior", corte_superior, tope, "Por viento", "NSR-10 K.4.2"))
    return Distribucion(franjas, avisos)


# Preguntas que el agente hace al cliente para definir el vano (levantamiento).
PREGUNTAS_VANO = [
    "Ancho y alto del vano libre (sin contar el muro), en cm.",
    "Altura del muro o antepecho existente desde el piso terminado, en cm (0 si el vano llega al piso).",
    "¿En qué piso queda la ventana? ¿Al otro lado hay balcón, vacío o terreno a menos de 1 m?",
    "¿Desea cuerpo fijo inferior? (si el muro es bajo y hay desnivel, la norma lo exige).",
    "¿Desea cuerpo fijo superior? ¿De qué alto?",
    "Tipo de edificación: vivienda, oficina, comercio, colegio u otra.",
]
