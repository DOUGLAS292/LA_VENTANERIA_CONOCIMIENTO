import pytest

from cotizador_agente.vano import distribuir_vano, vidrio_bajo_travesano


def _altos(d):
    return [(f.tipo, f.alto_mm) for f in d.franjas]


def test_muro_bajo_en_piso_alto_exige_fijo_inferior_hasta_1100():
    # Ejemplo de Dirección General: muro de 40 cm -> fijo inferior de 70 cm
    d = distribuir_vano(1500, 2000, altura_muro_mm=400)
    assert _altos(d) == [("fijo_inferior", 700), ("ventana", 1300)]
    assert d.franjas[1].desde_mm == 1100


def test_muro_de_1_m_ya_protege_y_no_exige_fijo():
    d = distribuir_vano(1500, 1200, altura_muro_mm=1000)
    assert _altos(d) == [("ventana", 1200)]
    assert "no se exige fijo inferior" in d.avisos[0]


def test_cliente_pide_fijo_inferior_con_muro_de_1_m():
    d = distribuir_vano(1500, 1200, altura_muro_mm=1000, fijo_inferior_solicitado=True)
    assert _altos(d) == [("fijo_inferior", 100), ("ventana", 1100)]


def test_primer_piso_sin_desnivel_no_exige_fijo_pero_vidrio_bajo_5mm():
    d = distribuir_vano(1200, 2100, altura_muro_mm=0, desnivel_exterior=False)
    assert _altos(d) == [("ventana", 2100)]
    assert "5 mm" in d.franjas[0].vidrio


def test_ventana_mas_alta_que_la_serie_genera_fijo_superior():
    d = distribuir_vano(1500, 2000, altura_muro_mm=400, alto_max_ventana_mm=1100)
    assert _altos(d) == [("fijo_inferior", 700), ("ventana", 1100), ("fijo_superior", 200)]


def test_fijo_superior_pedido_por_el_cliente():
    d = distribuir_vano(1500, 2000, altura_muro_mm=400, fijo_superior_mm=300)
    assert _altos(d) == [("fijo_inferior", 700), ("ventana", 1000), ("fijo_superior", 300)]


def test_travesano_fuera_de_norma_se_rechaza():
    with pytest.raises(ValueError):
        distribuir_vano(1500, 2000, altura_muro_mm=400, travesano_mm=1200)


def test_vidrio_bajo_travesano_vivienda_y_oficina():
    # 1.50 x 0.70 = 1.05 m2: vivienda (columna 2) admite recocido 5 mm hasta 1.2 m2
    assert vidrio_bajo_travesano(1500, 700)[0].startswith("Recocido 5 mm")
    # 2.40 x 0.70 = 1.68 m2: vivienda pasa a 6 mm; demás edificaciones (columna 3) admite 5 mm
    assert vidrio_bajo_travesano(2400, 700)[0].startswith("Recocido 6 mm")
    assert vidrio_bajo_travesano(2400, 700, "oficina")[0].startswith("Recocido 5 mm")
