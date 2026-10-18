"""Catálogo de vidrios: lectura sin precios y filtro por NSR-10 y serie (catálogo de prueba, no el real)."""

import json

import pytest
from openpyxl import Workbook

from cotizador_agente import catalogo_vidrios, herramientas

ENCABEZADO = ["Código", "Descripción", "Familia", "Tipo NSR-10", "Lámina 1 (mm)", "Lámina 2 (mm)", "Interlayer (mm)",
              "Cámara (mm)", "Color / tono", "Prestación", "Precio m² (COP)", "Estado", "Por revisar"]
FILAS = [
    ("803", "Incoloro 4 mm", "Monolítico", "recocido", 4, None, None, None, "Incoloro", None, 999, "Activo", None),
    ("801", "Incoloro 6 mm", "Monolítico", "recocido", 6, None, None, None, "Incoloro", None, 999, "Activo", None),
    ("303", "Laminado 4+4 PVB 0,38", "Laminado", "laminado_pvb", 4, 4, 0.38, None, "Incoloro", None, 999, "Activo", None),
    ("305", "Laminado 6+4 acústico", "Laminado", "laminado_pvb", 6, 4, 0.76, None, "Incoloro", "Acústico", 999, "Activo", None),
    ("4043", "Laminado Low-E 6+6", "Laminado", "laminado_pvb", 6, 6, 0.76, None, "Low-E", "Control solar", 999, "Activo", None),
    ("202", "Templado 6 mm", "Templado", "templado", 6, None, None, None, "Incoloro", None, 999, "Por revisar", "Precio a verificar"),
    ("401", "DVH 6-13-6", "Insulado (DVH)", "especial", 6, 6, None, 13, "Low-E", None, 999, "Activo", None),
    ("1001", "Espejo 4 mm", "Espejo", None, 4, None, None, None, "Espejo", None, 999, "Activo", None),
    ("9", "Bronce 4 mm (descontinuado)", "Monolítico", "recocido", 4, None, None, None, "Bronce", None, 999, "Inactivo", None),
]


@pytest.fixture
def ruta(tmp_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Catálogo"
    ws.append(ENCABEZADO)
    for f in FILAS:
        ws.append(list(f))
    ws.append([None] * len(ENCABEZADO))  # fila vacía al final, como en la plantilla
    r = tmp_path / "catalogo.xlsx"
    wb.save(r)
    return r


def test_lee_espesores_y_nunca_el_precio(ruta):
    vidrios = {v.codigo: v for v in catalogo_vidrios.cargar(ruta)}
    assert vidrios["303"].espesor_nominal_mm == 8 and vidrios["303"].espesor_total_mm == 8.38
    assert vidrios["401"].espesor_total_mm == 25
    assert "999" not in json.dumps([v.__dict__ for v in vidrios.values()])


def test_serie_50_laminado_minimo_5_mm(ruta):
    r = catalogo_vidrios.opciones(catalogo_vidrios.cargar(ruta), "alumina_serie_50", {"laminado_pvb": 5})
    codigos = [o["codigo"] for o in r["opciones"]]
    assert codigos == ["303", "305"]  # el 6+6 (12 mm) no cabe en la Serie 50 (4 a 10 mm)
    assert r["rango_serie_mm"] == (4.0, 10.0) and r["insulados_y_blindados_a_ingenieria"] == ["401"]


def test_serie_80_acepta_el_6_mas_6(ruta):
    r = catalogo_vidrios.opciones(catalogo_vidrios.cargar(ruta), "alumina_serie_80", {"laminado_pvb": 5})
    assert "4043" in [o["codigo"] for o in r["opciones"]]


def test_seguridad_descarta_recocido_y_respeta_preferencias(ruta):
    vidrios = catalogo_vidrios.cargar(ruta)
    minimos = {"recocido": 4, "templado": 4, "laminado_pvb": 5}
    seguros = [o["codigo"] for o in catalogo_vidrios.opciones(vidrios, "alumina_serie_50", minimos, exige_seguridad=True)["opciones"]]
    assert "803" not in seguros and "801" not in seguros and "202" in seguros
    acustico = catalogo_vidrios.opciones(vidrios, "alumina_serie_50", minimos, prestacion="acústico")["opciones"]
    assert [o["codigo"] for o in acustico] == ["305"]


def test_inactivos_y_espejos_no_se_ofrecen(ruta):
    r = catalogo_vidrios.opciones(catalogo_vidrios.cargar(ruta), "alumina_serie_50", {"recocido": 4})
    codigos = [o["codigo"] for o in r["opciones"]]
    assert "9" not in codigos and "1001" not in codigos and codigos == ["803", "801"]


def test_herramienta_sin_catalogo_no_inventa(monkeypatch):
    monkeypatch.delenv(catalogo_vidrios.ENV_RUTA, raising=False)
    r = herramientas.ejecutar("opciones_vidrio", {"sistema": "alumina_serie_50", "minimos_mm": {"recocido": 4}},
                              herramientas.Sesion())
    assert "No hay catálogo" in r["error"]


def test_herramienta_con_catalogo(ruta):
    sesion = herramientas.Sesion(ruta_catalogo_vidrios=ruta)
    r = herramientas.ejecutar("opciones_vidrio", {"sistema": "alumina_serie_80", "minimos_mm": {"templado": 6},
                                                   "exige_seguridad": True}, sesion)
    assert [o["codigo"] for o in r["opciones"]] == ["202"]
    assert r["opciones"][0]["por_revisar"] == "Precio a verificar"
