"""Tablas de enganche de todas las series corredizas cargadas.

Controles de calidad de la extracción de las fichas y casos de selección por viento.
"""

import json

import pytest

from cotizador_agente.criterio_tecnico import DATOS, Sistema
from cotizador_agente.viento import presion_diseno, region_de_ciudad

SERIES = ["alumina_serie_33", "alumina_serie_50", "alumina_serie_80", "koncept_50"]


def _grupos(codigo):
    datos = json.loads((DATOS / "sistemas" / f"{codigo}.json").read_text(encoding="utf-8"))
    return {nombre: g["orden"] for nombre, g in datos.items() if isinstance(g, dict) and "orden" in g}


@pytest.mark.parametrize("codigo", SERIES)
def test_tablas_decrecen_con_ancho_y_altura(codigo):
    for grupo, variantes in _grupos(codigo).items():
        for v in variantes:
            filas = v["tabla"]["filas"]
            alturas = sorted(filas, key=float)
            for h in alturas:
                fila = [x for x in filas[h] if x is not None]
                assert fila == sorted(fila, reverse=True), (grupo, v["codigo"], h)
            for c in range(len(v["tabla"]["columnas_m"])):
                col = [filas[h][c] for h in alturas if filas[h][c] is not None]
                assert col == sorted(col, reverse=True), (grupo, v["codigo"], c)


@pytest.mark.parametrize("codigo", SERIES)
def test_cada_combinacion_resiste_al_menos_la_anterior(codigo):
    for grupo, variantes in _grupos(codigo).items():
        for a, b in zip(variantes, variantes[1:]):
            comunes = set(a["tabla"]["filas"]) & set(b["tabla"]["filas"])
            for h in comunes:
                for va, vb in zip(a["tabla"]["filas"][h], b["tabla"]["filas"][h]):
                    if va is not None:
                        assert vb is not None and vb >= va, (grupo, a["codigo"], b["codigo"], h)


def test_serie_33_ventana_baja_usa_el_enganche_liviano():
    r = Sistema("alumina_serie_33").seleccionar_variante("enganches", 0.60, 0.90, 40)
    assert r["seleccion"]["codigo"] == "1968_1964" and r["resiste_kgm2"] == 56


def test_serie_33_ventana_de_1_50_necesita_el_mas_resistente():
    # 1968+1965 da 47 kg/m2 con naves de 0.60 m: no llega a 60
    r = Sistema("alumina_serie_33").seleccionar_variante("enganches", 0.60, 1.50, 60)
    assert r["seleccion"]["codigo"] == "1968_1966" and r["resiste_kgm2"] == 84


def test_serie_80_puerta_en_barranquilla_alta():
    # Puerta de 2.40 m con naves de 1.20 m en un piso 10 (30 m) de Barranquilla
    region = region_de_ciudad("Barranquilla")["region"]
    p = presion_diseno(region, 30, area_efectiva_m2=1.2 * 2.4).presion_kgm2
    r = Sistema("alumina_serie_80").seleccionar_variante("enganches", 1.20, 2.40, p)
    assert r["seleccion"]["codigo"] == "2282_2250"
    assert r["resiste_kgm2"] >= p


def test_serie_80_puerta_de_bogota_casa():
    p = presion_diseno(region_de_ciudad("Bogotá")["region"], 6, area_efectiva_m2=2.0).presion_kgm2
    r = Sistema("alumina_serie_80").seleccionar_variante("enganches", 1.00, 2.20, p)
    assert r["seleccion"]["codigo"] == "2282_2249"


def test_koncept_50_sin_enganche_que_resista_escala():
    r = Sistema("koncept_50").seleccionar_variante("enganches", 1.00, 1.50, 60)
    assert r["seleccion"] is None
