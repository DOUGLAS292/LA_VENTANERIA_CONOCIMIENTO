import pytest

from cotizador_agente.viento import presion_diseno, region_de_ciudad


def test_region_de_ciudad():
    assert region_de_ciudad("Barranquilla")["region"] == 5
    assert region_de_ciudad("Bogotá")["V_ms"] == 28
    assert region_de_ciudad("Ciudad inexistente") is None


def test_metodo_1_coincide_con_cotizador_excel():
    # Región 3, casa baja, exposición B, ventana de 1 m2 en zona interior:
    # pnet10 = 0.36 -> mínimo normativo 0.40 kN/m2 ≈ 41 kg/m2 (el Excel usa 40).
    p = presion_diseno(region=3, altura_edificio_m=6, area_efectiva_m2=1, zona=4)
    assert p.metodo == "metodo_1"
    assert p.presion_knm2 == pytest.approx(0.40)
    assert p.presion_kgm2 == pytest.approx(40.8, abs=0.1)


def test_metodo_1_esquina_y_altura():
    # Zona 5, región 5, 1 m2, exposición C, h = 15 m: 1.56 * 0.75
    p = presion_diseno(region=5, altura_edificio_m=15, area_efectiva_m2=1, exposicion="C", zona=5)
    assert p.presion_knm2 == pytest.approx(1.56 * 0.75, abs=1e-3)


def test_metodo_1_area_intermedia_usa_area_menor():
    p3 = presion_diseno(region=3, altura_edificio_m=9, area_efectiva_m2=3, zona=5)
    p2 = presion_diseno(region=3, altura_edificio_m=9, area_efectiva_m2=2, zona=5)
    assert p3.presion_knm2 == p2.presion_knm2 == pytest.approx(0.41)


def test_metodo_2_edificio_alto():
    p = presion_diseno(region=3, altura_edificio_m=60, area_efectiva_m2=1, exposicion="B", zona=5)
    qh = 0.613 * 1.20 * 1.0 * 0.85 * 28**2 / 1000
    assert p.metodo == "metodo_2"
    assert p.presion_knm2 == pytest.approx(qh * (1.8 + 0.18), abs=1e-3)


def test_altura_excesiva():
    with pytest.raises(ValueError):
        presion_diseno(region=3, altura_edificio_m=200, area_efectiva_m2=1)
