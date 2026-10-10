import pytest

from cotizador_agente.viento import presion_diseno, region_de_ciudad


def test_region_de_ciudad():
    assert region_de_ciudad("Barranquilla")["region"] == 5
    assert region_de_ciudad("Bogotá")["V_ms"] == 28
    assert region_de_ciudad("Ciudad inexistente") is None


def test_metodo_1_coincide_con_cotizador_excel():
    # Región 3, casa baja, exposición B, ventana de 1 m2 en zona interior:
    # pnet10 = 0.36 -> mínimo normativo 0.40 kN/m2 ≈ 41 kg/m2 (el Excel usa 40).
    p = presion_diseno(region=3, altura_edificio_m=6, area_efectiva_m2=1, exposicion="B", zona=4)
    assert p.metodo == "metodo_1"
    assert p.presion_knm2 == pytest.approx(0.40)
    assert p.presion_kgm2 == pytest.approx(40.8, abs=0.1)


def test_metodo_1_esquina_y_altura():
    # Zona 5, región 5, 1 m2, exposición C, h = 15 m: 1.56 * 0.75
    p = presion_diseno(region=5, altura_edificio_m=15, area_efectiva_m2=1, exposicion="C", zona=5)
    assert p.presion_knm2 == pytest.approx(1.56 * 0.75, abs=1e-3)


def test_metodo_1_area_intermedia_usa_area_menor():
    p3 = presion_diseno(region=3, altura_edificio_m=9, area_efectiva_m2=3, exposicion="B", zona=5)
    p2 = presion_diseno(region=3, altura_edificio_m=9, area_efectiva_m2=2, exposicion="B", zona=5)
    assert p3.presion_knm2 == p2.presion_knm2 == pytest.approx(0.41)


def test_metodo_2_edificio_alto():
    p = presion_diseno(region=3, altura_edificio_m=60, area_efectiva_m2=1, exposicion="B", zona=5)
    qh = 0.613 * 1.20 * 1.0 * 0.85 * 28**2 / 1000
    assert p.metodo == "metodo_2"
    assert p.presion_knm2 == pytest.approx(qh * (1.8 + 0.18), abs=1e-3)


def test_altura_excesiva():
    with pytest.raises(ValueError):
        presion_diseno(region=3, altura_edificio_m=200, area_efectiva_m2=1)


def test_presion_no_baja_al_pasar_de_18_m():
    for region in (1, 2, 3, 4, 5):
        for exp in ("B", "C", "D"):
            p18 = presion_diseno(region, 18, 1, exposicion=exp, zona=4).presion_knm2
            p20 = presion_diseno(region, 20, 1, exposicion=exp, zona=4).presion_knm2
            assert p20 >= p18
            assert p20 >= 0.40


def test_validacion_tabla_alumina_vc744_a_3_m():
    # Tabla de restricciones Alúmina VC744 (zona 4, 3 m): Bogotá 40, Cali 40, Barranquilla 62 kg/m2.
    assert presion_diseno(3, 3, 1, exposicion="B", zona=4).presion_kgm2 == pytest.approx(40.8, abs=0.1)
    assert presion_diseno(5, 3, 1, exposicion="B", zona=4).presion_kgm2 == pytest.approx(62.2, abs=0.1)


def test_region_por_departamento():
    r = region_de_ciudad("Jamundí", "Valle del Cauca")
    assert (r["region"], r["criterio"]) == (3, "departamento")
    assert region_de_ciudad("Soledad", "Atlántico")["region"] == 5
    # La ciudad conocida manda sobre el departamento
    assert region_de_ciudad("Bogotá", "Cundinamarca")["criterio"] == "ciudad"
    assert region_de_ciudad("Pueblo", "Departamento inexistente") is None


def test_todos_los_departamentos_tienen_region():
    from cotizador_agente.viento import DATOS
    deps = {k: v for k, v in DATOS["departamentos"].items() if not k.startswith("_")}
    assert len(deps) == 33  # 32 departamentos + Bogotá D.C.
    assert all(v in (1, 2, 3, 4, 5) for v in deps.values())
