"""PDF de la cotización para el cliente.

Junta dos fuentes sin mezclarlas:
- Precios, totales, IVA y vigencia: vienen tal cual del software de cotización
  (RespuestaCotizacion). El agente nunca los escribe ni los recalcula.
- Especificación técnica: la propuesta del agente (serie, configuración, perfiles,
  distribución del vano, vidrio y normas), verificada con las herramientas.

Identidad (LV-MKT-001): colores corporativos fijos. La tipografía Gilroy y el logo
son activos licenciados que viven en Drive, no en GitHub: se pasan como rutas en
`Empresa`. Sin ellos se usa Helvetica y solo el nombre, y el PDF lo indica para que
Marketing lo valide antes de un uso oficial.
"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .modelos import RespuestaCotizacion

AZUL = colors.HexColor("#04253A")
NARANJA = colors.HexColor("#FF7F00")
AMARILLO = colors.HexColor("#FFAD01")
GRIS_MUY_CLARO = colors.HexColor("#F7F7F7")
GRIS_CLARO = colors.HexColor("#EFEFEF")
OSCURO = colors.HexColor("#1C1C1C")


# --- Datos de entrada --------------------------------------------------------------

class Franja(BaseModel):
    tipo: str  # fijo_inferior | ventana | fijo_superior
    alto_mm: float
    vidrio: str = ""


class FichaTecnicaItem(BaseModel):
    """Especificación técnica de un ítem, tal como la verificó el agente."""
    indice: int = Field(ge=0, description="Índice del ítem en la respuesta del software")
    sistema: str
    configuracion: str = ""
    presion_diseno_kgm2: float | None = None
    perfiles: list[str] = []
    franjas: list[Franja] = []
    vidrio: str = ""
    normas: list[str] = []
    observaciones: list[str] = []


@dataclass
class Empresa:
    """Datos de la empresa. NIT, dirección y condiciones se cargan desde Drive al ejecutar."""
    razon_social: str = "La Ventanería Ingeniería y Diseño S.A.S."
    descriptor: str = "Ingeniería & diseño"
    contacto: list[str] = field(default_factory=list)  # NIT, dirección, teléfono, correo
    condiciones: list[str] = field(default_factory=list)  # condiciones comerciales aprobadas
    logo: Path | None = None
    fuente_regular: Path | None = None  # Gilroy-Regular.ttf
    fuente_negrita: Path | None = None  # Gilroy-Bold.ttf


# --- Formato -------------------------------------------------------------------------

def pesos(valor: int) -> str:
    """Formato colombiano: $ 1.234.567"""
    return "$ " + f"{valor:,}".replace(",", ".")


def _fuentes(empresa: Empresa) -> tuple[str, str, bool]:
    if empresa.fuente_regular and empresa.fuente_negrita:
        pdfmetrics.registerFont(TTFont("Corporativa", str(empresa.fuente_regular)))
        pdfmetrics.registerFont(TTFont("Corporativa-Negrita", str(empresa.fuente_negrita)))
        return "Corporativa", "Corporativa-Negrita", True
    return "Helvetica", "Helvetica-Bold", False


_NOMBRES_FRANJA = {"fijo_inferior": "Fijo inferior", "ventana": "Ventana / puerta", "fijo_superior": "Fijo superior"}


# --- Generación ---------------------------------------------------------------------------

def generar_pdf(respuesta: RespuestaCotizacion, fichas: list[FichaTecnicaItem], destino: Path,
                cliente: str, ciudad: str, empresa: Empresa | None = None, fecha: date | None = None) -> Path:
    empresa = empresa or Empresa()
    fecha = fecha or date.today()
    regular, negrita, corporativa = _fuentes(empresa)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    est = {
        "titulo": ParagraphStyle("titulo", fontName=negrita, fontSize=15, textColor=AZUL, leading=19),
        "sub": ParagraphStyle("sub", fontName=regular, fontSize=9, textColor=NARANJA, leading=12),
        "h2": ParagraphStyle("h2", fontName=negrita, fontSize=12, textColor=AZUL, spaceBefore=10, spaceAfter=4),
        "h3": ParagraphStyle("h3", fontName=negrita, fontSize=10, textColor=OSCURO, spaceBefore=6, spaceAfter=2),
        "txt": ParagraphStyle("txt", fontName=regular, fontSize=9, textColor=OSCURO, leading=12),
        "peq": ParagraphStyle("peq", fontName=regular, fontSize=7.5, textColor=OSCURO, leading=10),
        "der": ParagraphStyle("der", fontName=regular, fontSize=9, textColor=OSCURO, alignment=TA_RIGHT),
        "cel": ParagraphStyle("cel", fontName=regular, fontSize=8.5, textColor=OSCURO, leading=11),
    }
    P = Paragraph
    historia = []

    # Encabezado
    marca = [P(empresa.razon_social, est["titulo"]), P(empresa.descriptor, est["sub"])]
    if empresa.logo and Path(empresa.logo).exists():
        ancho_img, alto_img = ImageReader(str(empresa.logo)).getSize()
        alto = 18 * mm
        marca = [Image(str(empresa.logo), width=alto * ancho_img / alto_img, height=alto)]  # sin deformar
    datos = [
        P(f"<b>COTIZACIÓN N.º {respuesta.cotizacion_id}</b>", est["der"]),
        P(f"Fecha: {fecha.isoformat()}", est["der"]),
        P(f"Vigencia: {respuesta.vigencia_dias} días", est["der"]),
        P(f"Estado: {'PRELIMINAR' if respuesta.estado == 'preliminar' else 'Firme'}", est["der"]),
    ]
    enc = Table([[marca, datos]], colWidths=[110 * mm, 76 * mm])
    enc.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("LINEBELOW", (0, 0), (-1, 0), 2, NARANJA),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    historia += [enc, Spacer(1, 4 * mm)]
    if empresa.contacto:
        historia.append(P(" · ".join(empresa.contacto), est["peq"]))
    historia += [P(f"<b>Cliente:</b> {cliente} &nbsp;&nbsp; <b>Ciudad de la obra:</b> {ciudad}", est["txt"]),
                 Spacer(1, 2 * mm)]
    if respuesta.estado == "preliminar":
        historia.append(P("<font color='#FF7F00'><b>Cotización preliminar:</b></font> valores sujetos a "
                          "confirmación de Ingeniería o de medidas en obra.", est["txt"]))

    # Precios (del software de cotización)
    historia.append(P("Valores", est["h2"]))
    filas = [["#", "Descripción", "Cant.", "Valor unitario", "Subtotal"]]
    for it in respuesta.items:
        filas.append([str(it.indice + 1), P(it.descripcion, est["cel"]), str(it.cantidad),
                      pesos(it.precio_unitario), pesos(it.subtotal)])
    n = len(filas)
    filas += [["", "", "", "Subtotal", pesos(respuesta.subtotal)],
              ["", "", "", "IVA", pesos(respuesta.iva)],
              ["", "", "", "TOTAL", pesos(respuesta.total)]]
    tabla = Table(filas, colWidths=[8 * mm, 92 * mm, 14 * mm, 36 * mm, 36 * mm], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), regular, 8.5),
        ("FONT", (0, 0), (-1, 0), negrita, 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, n - 1), [colors.white, GRIS_MUY_CLARO]),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEABOVE", (3, n), (-1, n), 0.5, AZUL),
        ("FONT", (3, -1), (-1, -1), negrita, 10),
        ("BACKGROUND", (3, -1), (-1, -1), GRIS_CLARO),
        ("TEXTCOLOR", (3, -1), (-1, -1), AZUL),
    ]))
    historia.append(tabla)
    historia.append(P(f"Valores en pesos colombianos (COP). Lista de precios {respuesta.version_precios}.", est["peq"]))

    # Especificación técnica (del agente)
    if fichas:
        historia.append(P("Especificación técnica", est["h2"]))
        descripciones = {it.indice: it.descripcion for it in respuesta.items}
        for f in sorted(fichas, key=lambda x: x.indice):
            bloque = [P(f"Ítem {f.indice + 1}: {descripciones.get(f.indice, f.sistema)}", est["h3"])]
            renglones = [["Sistema", f.sistema]]
            if f.configuracion:
                renglones.append(["Configuración", f.configuracion])
            if f.presion_diseno_kgm2:
                renglones.append(["Presión de viento de diseño", f"{f.presion_diseno_kgm2:.0f} kg/m²"])
            if f.perfiles:
                renglones.append(["Perfiles verificados", ", ".join(f.perfiles)])
            if f.vidrio:
                renglones.append(["Vidrio", f.vidrio])
            for fr in f.franjas:
                texto = f"{fr.alto_mm:.0f} mm" + (f" — {fr.vidrio}" if fr.vidrio else "")
                renglones.append([_NOMBRES_FRANJA.get(fr.tipo, fr.tipo), texto])
            if f.normas:
                renglones.append(["Normas", "; ".join(f.normas)])
            t = Table([[P(a, est["cel"]), P(b, est["cel"])] for a, b in renglones], colWidths=[48 * mm, 138 * mm])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), GRIS_MUY_CLARO),
                                   ("LINEBELOW", (0, 0), (-1, -1), 0.25, GRIS_CLARO),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            bloque.append(t)
            for o in f.observaciones:
                bloque.append(P(f"• {o}", est["cel"]))
            historia.append(KeepTogether(bloque))

    # Alertas del software
    if respuesta.alertas:
        historia.append(P("Observaciones", est["h2"]))
        for a in respuesta.alertas:
            item = f"Ítem {a.indice_item + 1}: " if a.indice_item is not None else ""
            marca_ing = "<font color='#FF7F00'><b>Ingeniería:</b></font> " if a.nivel == "ingenieria" else ""
            historia.append(P(f"• {marca_ing}{item}{a.mensaje}", est["txt"]))

    # Condiciones
    historia.append(P("Condiciones", est["h2"]))
    condiciones = [f"Oferta válida por {respuesta.vigencia_dias} días a partir de la fecha."]
    condiciones += empresa.condiciones
    condiciones.append("Diseño verificado según NSR-10 (Títulos B y K) y las fichas técnicas de los fabricantes.")
    for c in condiciones:
        historia.append(P(f"• {c}", est["txt"]))
    if not corporativa:
        historia.append(Spacer(1, 3 * mm))
        historia.append(P("Tipografía provisional (Helvetica): POR VALIDAR CON MARKETING/DIRECCIÓN.", est["peq"]))

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(NARANJA)
        canvas.setLineWidth(1)
        canvas.line(15 * mm, 14 * mm, LETTER[0] - 15 * mm, 14 * mm)
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(AZUL)
        canvas.drawString(15 * mm, 10 * mm, f"{empresa.razon_social} — {empresa.descriptor}")
        canvas.drawRightString(LETTER[0] - 15 * mm, 10 * mm,
                               f"Cotización {respuesta.cotizacion_id} · Página {doc.page}")
        if respuesta.estado == "preliminar":
            canvas.setFont(negrita, 60)
            canvas.setFillColor(AMARILLO, alpha=0.12)
            canvas.translate(LETTER[0] / 2, LETTER[1] / 2)
            canvas.rotate(35)
            canvas.drawCentredString(0, 0, "PRELIMINAR")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(destino), pagesize=LETTER, leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=20 * mm,
                            title=f"Cotización {respuesta.cotizacion_id}", author=empresa.razon_social)
    doc.build(historia, onFirstPage=pie, onLaterPages=pie)
    return destino
