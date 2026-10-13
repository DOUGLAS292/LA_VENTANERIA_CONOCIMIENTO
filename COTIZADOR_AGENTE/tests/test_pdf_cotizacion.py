"""PDF de la cotización. Los valores son ficticios, solo de prueba (no son precios reales)."""

from datetime import date

from pypdf import PdfReader

from cotizador_agente import herramientas
from cotizador_agente.modelos import Alerta, ItemCotizado, RespuestaCotizacion
from cotizador_agente.pdf_cotizacion import FichaTecnicaItem, Franja, generar_pdf, pesos

RESPUESTA = RespuestaCotizacion(
    cotizacion_id="PRUEBA-001", estado="preliminar", version_precios="prueba", vigencia_dias=15,
    items=[ItemCotizado(indice=0, descripcion="Ventana corrediza OX 2000 x 1300", cantidad=2,
                        precio_unitario=1000, subtotal=2000)],
    subtotal=2000, iva=380, total=2380,
    alertas=[Alerta(codigo="MEDIDA", nivel="ingenieria", indice_item=0, mensaje="Confirmar medidas en obra.")],
)

FICHA = FichaTecnicaItem(
    indice=0, sistema="Koncept 70 (Alúmina)", configuracion="OX", presion_diseno_kgm2=171,
    perfiles=["Enganches liso + reforzado (NAVE1754 + NAVE1904)"],
    franjas=[Franja(tipo="fijo_inferior", alto_mm=700, vidrio="Recocido 6 mm"),
             Franja(tipo="ventana", alto_mm=1300, vidrio="Laminado 6 mm")],
    normas=["NSR-10 B.6", "NSR-10 K.4.3.9.7"],
)


def _texto(ruta):
    return "\n".join(p.extract_text() for p in PdfReader(str(ruta)).pages)


def test_formato_pesos_colombianos():
    assert pesos(1234567) == "$ 1.234.567"


def test_pdf_lleva_precios_del_software_y_ficha_tecnica(tmp_path):
    ruta = generar_pdf(RESPUESTA, [FICHA], tmp_path / "c.pdf", "Constructora Prueba", "Barranquilla",
                       fecha=date(2026, 10, 13))
    texto = _texto(ruta)
    for esperado in ["PRUEBA-001", "Constructora Prueba", "Barranquilla", "$ 2.380", "$ 380",
                     "Koncept 70", "171 kg/m²", "Fijo inferior", "NSR-10 K.4.3.9.7",
                     "Confirmar medidas en obra", "Oferta válida por 15 días", "2026-10-13"]:
        assert esperado in texto, esperado
    assert "POR VALIDAR CON MARKETING" in texto  # sin Gilroy, se avisa


class MotorDePrueba:
    def obtener_catalogo(self):
        raise NotImplementedError

    def cotizar(self, solicitud):
        return RESPUESTA


SOLICITUD = {"referencia_cliente": "Apto 502", "ciudad": "Barranquilla", "items": [{
    "sistema": "K70", "ancho_mm": 2000, "alto_mm": 2000, "cantidad": 2,
    "vidrio": "LAM6", "color_perfil": "blanco", "piso": 10}]}


def test_pdf_sin_cotizar_no_se_genera(tmp_path):
    r = herramientas.ejecutar("generar_pdf_cotizacion", {"cliente": "X", "fichas_tecnicas": []},
                              herramientas.Sesion(carpeta_pdf=tmp_path))
    assert "Primero hay que cotizar" in r["error"]


def test_flujo_cotizar_y_generar_pdf(tmp_path):
    sesion = herramientas.Sesion(motor=MotorDePrueba(), carpeta_pdf=tmp_path)
    assert herramientas.ejecutar("enviar_a_cotizar", {"solicitud": SOLICITUD}, sesion)["estado"] == "cotizada"
    r = herramientas.ejecutar("generar_pdf_cotizacion",
                              {"cliente": "Constructora Prueba", "fichas_tecnicas": [FICHA.model_dump()]}, sesion)
    assert r["estado"] == "pdf_generado" and r["total"] == 2380
    assert "Constructora Prueba" in _texto(r["archivo"])


def test_ficha_con_indice_inexistente_se_rechaza(tmp_path):
    sesion = herramientas.Sesion(motor=MotorDePrueba(), carpeta_pdf=tmp_path)
    herramientas.ejecutar("enviar_a_cotizar", {"solicitud": SOLICITUD}, sesion)
    r = herramientas.ejecutar("generar_pdf_cotizacion",
                              {"cliente": "X", "fichas_tecnicas": [{"indice": 5, "sistema": "K70"}]}, sesion)
    assert "5" in r["error"]
