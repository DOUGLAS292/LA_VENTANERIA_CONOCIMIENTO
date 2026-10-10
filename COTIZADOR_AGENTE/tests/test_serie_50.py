import pytest

from cotizador_agente.criterio_tecnico import Sistema


@pytest.fixture(scope="module")
def s50():
    return Sistema("alumina_serie_50")


def test_enganche_sencillo_para_ventana_baja(s50):
    r = s50.seleccionar_variante("enganches", 0.80, 1.20, 40)
    assert r["seleccion"]["codigo"] == "sencillo" and r["resiste_kgm2"] == 61


def test_enganche_sube_con_la_altura(s50):
    # Ventana de 1.50 m de alto: sencillo no llega; sencillo + semirreforzado resiste 134 >= 60
    r = s50.seleccionar_variante("enganches", 0.80, 1.50, 60)
    assert r["seleccion"]["codigo"] == "sencillo_semirreforzado"


def test_puerta_alta_en_costa_pide_reforzados(s50):
    # Puerta de 2.40 m, naves de 1.20 m, 100 kg/m2 (Barranquilla en altura)
    r = s50.seleccionar_variante("enganches", 1.20, 2.40, 100)
    assert r["seleccion"]["codigo"] == "reforzados" and r["resiste_kgm2"] == 113


def test_sin_solucion_en_tablas(s50):
    r = s50.seleccionar_variante("enganches", 1.20, 2.60, 120)
    assert r["seleccion"] is None
    assert [e["codigo"] for e in r["evaluadas"]][-1] == "reforzados"


def test_cierre_medio_oxxo(s50):
    r = s50.seleccionar_variante("cierre_medio_OXXO", 1.00, 2.20, 60)
    assert r["seleccion"]["codigo"] == "cierre_medio_reforzado"
