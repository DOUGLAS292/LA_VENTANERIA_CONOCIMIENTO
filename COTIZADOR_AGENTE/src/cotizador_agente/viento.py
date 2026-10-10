"""Presión de viento de diseño para ventanas y fachadas (NSR-10 Capítulo B.6).

- h <= 18 m: Método 1 simplificado, componentes y revestimientos (B.6.4.2.2).
- h > 18 m: Método 2 analítico, componentes y revestimientos (B.6.5.12.4.2).

Criterio conservador: área efectiva entre dos valores tabulados -> se usa el área
menor (Figura B.6.4-3, nota 4); altura entre dos valores -> la altura mayor; en el
Método 2 se usa qh (altura total del edificio) para todo el muro.
"""

import json
import math
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .criterio_tecnico import KG_M2_A_KN_M2

DATOS = json.loads((Path(__file__).parent / "datos" / "nsr10_b6_viento.json").read_text(encoding="utf-8"))


def _normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sin_tildes.lower().replace(",", " ").split())


def region_de_ciudad(ciudad: str) -> dict | None:
    """Región eólica de una ciudad (lectura preliminar del mapa, ver JSON)."""
    datos = DATOS["ciudades"].get(_normalizar(ciudad))
    if datos is None:
        return None
    return {"ciudad": ciudad, **datos, "V_ms": DATOS["regiones"][str(datos["region"])]["V_ms"]}


def _indice_superior(valor: float, pasos: list[float]) -> int:
    for i, paso in enumerate(pasos):
        if paso >= valor - 1e-9:
            return i
    raise ValueError(f"{valor} supera el máximo tabulado {pasos[-1]}")


def _indice_area_menor(area: float, areas: list[float]) -> int:
    indice = 0
    for i, a in enumerate(areas):
        if a <= area + 1e-9:
            indice = i
    return indice


def _interpolar(x: float, xs: list[float], ys: list[float]) -> float:
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise AssertionError


@dataclass
class PresionViento:
    presion_knm2: float
    region: int
    V_ms: int
    metodo: str
    detalle: str

    @property
    def presion_kgm2(self) -> float:
        return self.presion_knm2 / KG_M2_A_KN_M2


def presion_diseno(
    region: int,
    altura_edificio_m: float,
    area_efectiva_m2: float,
    exposicion: str = "B",
    zona: int = 5,
    grupo_uso: str | None = None,
    Kzt: float = 1.0,
) -> PresionViento:
    """Presión neta de diseño (valor absoluto de la más crítica entre presión y succión).

    Sin grupo de uso confirmado se toma I = 1.00: la tabla B.6.5-1 da 0.87 al Grupo I,
    reducción que el agente no aplica hasta que Ingeniería la confirme.
    """
    if zona not in (4, 5):
        raise ValueError("Zona de muro 4 (interior) o 5 (esquina)")
    if exposicion not in ("B", "C", "D"):
        raise ValueError("Exposición B, C o D")
    V = DATOS["regiones"][str(region)]["V_ms"]
    I = DATOS["importancia_I"][grupo_uso] if grupo_uso else 1.0

    if altura_edificio_m <= 18.0:
        m1 = DATOS["metodo_1_componentes"]
        i_area = _indice_area_menor(area_efectiva_m2, m1["areas_m2"])
        positiva, negativa = m1["pnet10"][str(zona)][str(V)][i_area]
        pnet10 = max(positiva, abs(negativa))
        lam = m1["lambda"]
        i_h = _indice_superior(max(altura_edificio_m, lam["alturas_m"][0]), lam["alturas_m"])
        factor = lam[exposicion][i_h]
        p = max(factor * Kzt * I * pnet10, m1["presion_minima"])
        detalle = (
            f"Método 1 (B.6.4.2.2): pnet = λ·Kzt·I·pnet10 = {factor}·{Kzt}·{I}·{pnet10} "
            f"(zona {zona}, área {m1['areas_m2'][i_area]} m², exposición {exposicion}, "
            f"h ≤ {lam['alturas_m'][i_h]} m); mínimo {m1['presion_minima']} kN/m²."
        )
        return PresionViento(round(p, 3), region, V, "metodo_1", detalle)

    m2 = DATOS["metodo_2_componentes_h_mayor_18"]
    kz = m2["Kz_caso1"]
    if altura_edificio_m > kz["alturas_m"][-1]:
        raise ValueError("Altura mayor a 152 m: requiere estudio específico")
    Kz = _interpolar(altura_edificio_m, kz["alturas_m"], kz[exposicion])
    qh = 0.613 * Kz * Kzt * m2["Kd"] * V**2 * I / 1000  # kN/m2
    g = m2["GCp_muros"]
    a = min(max(area_efectiva_m2, g["area_min_m2"]), g["area_max_m2"])
    t = math.log10(a / g["area_min_m2"]) / math.log10(g["area_max_m2"] / g["area_min_m2"])
    gcp_pos = g["positivo_4_5"][0] + t * (g["positivo_4_5"][1] - g["positivo_4_5"][0])
    neg = g[f"negativo_{zona}"]
    gcp_neg = neg[0] + t * (neg[1] - neg[0])
    gcpi = m2["GCpi_cerrado"]
    p = max(qh * (gcp_pos + gcpi), qh * (abs(gcp_neg) + gcpi))
    detalle = (
        f"Método 2 (B.6.5.12.4.2): qh = 0.613·Kz·Kzt·Kd·V²·I = {qh:.3f} kN/m² "
        f"(Kz {Kz:.2f}, exposición {exposicion}); GCp +{gcp_pos:.2f}/{gcp_neg:.2f}, "
        f"GCpi ±{gcpi} (zona {zona}, área {area_efectiva_m2} m²)."
    )
    return PresionViento(round(p, 3), region, V, "metodo_2", detalle)
