import pytest

from cotizador_agente.criterio_tecnico import NormaK4, Sistema, evaluar, kgm2_a_knm2


@pytest.fixture(scope="module")
def norma():
    return NormaK4()


@pytest.fixture(scope="module")
def s35():
    return Sistema("superior_serie_35")


def test_evaluar_formulas():
    assert evaluar("A - 20", A=1000) == 980
    assert evaluar("A/2 - 46", A=1600) == 754
    assert evaluar("4*A + 4*H", A=1000, H=500) == 6000
    with pytest.raises(ValueError):
        evaluar("__import__('os')", A=1)


def test_area_maxima_toma_renglon_de_presion_mayor(norma):
    # 0.6 kN/m2 cae entre 0.50 y 0.75: se usa 0.75 (conservador).
    assert norma.area_maxima_por_viento("recocido", 5, 0.6) == 5.76
    assert norma.area_maxima_por_viento("recocido", 5, 0.75) == 5.76
    assert norma.area_maxima_por_viento("templado", 6, 2.0) == 12.18
    assert norma.area_maxima_por_viento("recocido", 5, 8.0) is None


def test_verificar_vidrio_por_viento(norma):
    v = norma.verificar_vidrio_por_viento("recocido", 4, 1500, 1200, 1.0)  # 1.8 m2 <= 3.03
    assert v.cumple is True
    v = norma.verificar_vidrio_por_viento("recocido", 4, 1500, 1200, 2.0)  # 1.8 m2 > 1.08
    assert v.cumple is False
    v = norma.verificar_vidrio_por_viento("recocido", 6, 3000, 1000, 1.0)  # relación 3 > 2
    assert v.cumple is None


def test_espesor_minimo(norma):
    assert norma.espesor_minimo_por_viento("recocido", 1500, 1200, 2.0) == 6


def test_seguridad(norma):
    assert norma.verificar_seguridad("division_bano", "recocido", 0).cumple is False
    assert norma.verificar_seguridad("division_bano", "templado", 0).cumple is True
    assert norma.verificar_seguridad("ventana", "recocido", 900).cumple is True
    assert norma.verificar_seguridad("ventana", "recocido", 700, "escuela").cumple is False


def test_presion_resistente_redondea_hacia_arriba(s35):
    assert s35.presion_resistente("proyectante_XO", 0.80, 1.20) == 298
    # 0.85 x 1.15 -> se usa 0.90 x 1.20
    assert s35.presion_resistente("proyectante_XO", 0.85, 1.15) == 279
    assert s35.presion_resistente("proyectante_XO", 0.80, 2.10) is None
    assert s35.presion_resistente("proyectante_XO", 1.40, 2.00) is None  # celda vacía


def test_verificar_presion(s35):
    assert s35.verificar_presion("fijo_OO", 1.6, 1.5, 40).cumple is True
    assert s35.verificar_presion("fijo_OO", 1.6, 1.5, 60).cumple is False
    assert s35.verificar_presion("fijo_O", 1.0, 1.0, 40).cumple is None


def test_despiece_proyectante(s35):
    d = s35.despiece("proyectante_X", 5, A=1000, H=600)
    medidas = {(p["descripcion"]): p["medida_mm"] for p in d["perfiles"]}
    assert medidas["Nave horizontal"] == 980
    assert medidas["Nave vertical"] == 580
    vidrio = d["vidrios"][0]
    assert (vidrio["ancho_mm"], vidrio["alto_mm"]) == (888, 488)
    empaque_u = next(a for a in d["accesorios"] if "Empaque U" in a["descripcion"])
    assert empaque_u["ref"] == "17196"
    assert d["brazo"]["codigo"] == "17116"  # nave 580 de alto > 550 -> brazo 16"


def test_kgm2_a_knm2():
    assert kgm2_a_knm2(100) == pytest.approx(0.981, abs=1e-3)
