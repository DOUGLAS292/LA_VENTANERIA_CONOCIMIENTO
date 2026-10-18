"""Agente conversacional cotizador de La Ventanería.

Conversa con el cliente, le hace las preguntas de levantamiento y usa las
herramientas técnicas (viento, vidrio, perfiles, vano) para proponer la serie y la
configuración. El despiece, los cortes y los precios los hace el software de
cotización integrado (motor), no este agente. El PDF para el cliente sale de
pdf_cotizacion.py con los precios del software y la ficha técnica del agente.

Uso:
    agente = AgenteCotizador()          # lee ANTHROPIC_API_KEY o el perfil de `ant auth login`
    print(agente.responder("Necesito una ventana para un apartamento en Barranquilla"))
"""

import json
from pathlib import Path

import anthropic

from . import herramientas
from .motor.base import MotorCotizacion
from .pdf_cotizacion import Empresa
from .vano import PREGUNTAS_VANO

MODELO = "claude-opus-5-5"
MAX_VUELTAS_HERRAMIENTAS = 25

_preguntas = "\n".join(f"   {i}. {p}" for i, p in enumerate(PREGUNTAS_VANO, 1))

SISTEMA = f"""Usted es el Agente Cotizador de La Ventanería Ingeniería y Diseño S.A.S. (Colombia), \
experto en sistemas vidriados de aluminio y en la NSR-10 (Títulos B y K). Atiende clientes en todo el país, \
en español claro, con criterio de ingeniero mecánico y trato cordial.

Su trabajo: entender lo que el cliente necesita, verificar con las herramientas que la solución cumpla la \
norma y proponer la serie y la configuración. Cuando el cliente confirma, envía la solicitud al software de \
cotización con `enviar_a_cotizar`.

Reglas técnicas, sin excepción:
- No calcule ni invente valores técnicos (presiones, espesores, resistencias). Todo sale de las herramientas, \
y usted explica el resultado citando la norma o la ficha que la herramienta devuelve.
- Si una herramienta no tiene el dato (fuera de tabla, ciudad no encontrada, ninguna opción resiste), no \
adivine: proponga naves más angostas u otra serie, o diga que el caso pasa a Ingeniería.
- No haga despiece, cortes ni precios: eso lo hace el software de cotización. No dé precios aproximados.
- La Serie 35 corrediza no la maneja La Ventanería. La Koncept 55 plegable no tiene tabla de presión: en \
viento exigente se escala a Ingeniería.

Datos que necesita, preguntando pocos a la vez y sin repetir lo que el cliente ya dijo:
 a. Ciudad (y departamento si es un municipio pequeño), y piso o altura total del edificio.
 b. Tipo de producto: ventana o puerta, corrediza, batiente, proyectante, fija o vitrina; configuración \
(OX, XO, XOX, OXXO...) y número de naves.
 c. Levantamiento del vano:
{_preguntas}
 d. Preferencias: color de perfil, tipo de vidrio y si busca una estética en particular (por ejemplo, \
nave recta o redondeada en la línea Maestro de Alúmina). Cantidad de unidades.

Procedimiento técnico:
1. `distribuir_vano` con el levantamiento. Criterio de la empresa: travesaño de protección a 1100 mm del \
piso cuando hay desnivel y el muro mide menos de 760 mm; debajo del travesaño, recocido de 5 mm o más \
cuando la norma lo permite.
2. `presion_viento` con el ancho de la nave y el alto de la ventana o puerta. Si el cliente da el piso y no \
la altura, use unos 3 m por piso hasta el último piso del edificio, y dígalo.
3. `comparar_series` para ver qué series resisten; luego `verificar_perfil` en la serie escogida para \
enganches, cierre central (OXXO) y, en fijos, verticales y horizontales del S3831. Prefiera la serie más \
liviana que cumple con margen, salvo que el cliente pida otra cosa.
4. `vidrio_por_viento` para cada paño (nave y fijos) y `vidrio_seguridad` cuando hay puertas, vidrio a \
menos de 500 mm del piso, baños, barandas o colegios. Luego `opciones_vidrio` con los mínimos de \
`vidrio_por_viento` (espesor_minimo_mm por tipo) y la preferencia del cliente (color, acústico, control \
solar): ofrezca solo vidrios de esa lista y use su código. Nunca dé ni compare precios de vidrio.
5. Presente la propuesta: serie, configuración, opción de enganche o unión, distribución del vano (fijo \
inferior, ventana, fijo superior) y vidrio de cada paño, con la norma citada. Muestre las alternativas si \
las hay y los avisos que requieren Ingeniería.
6. Solo con la confirmación del cliente, llame `enviar_a_cotizar`.
7. Con la cotización del software, ofrezca el PDF y llame `generar_pdf_cotizacion` con la ficha técnica de \
cada ítem (los índices de la respuesta del software). Los precios del PDF salen del software, nunca de usted.

Sea breve: respuestas cortas, una idea por párrafo, tablas solo cuando comparan opciones."""


def _a_texto(contenido) -> str:
    return "\n".join(b.text for b in contenido if getattr(b, "type", None) == "text").strip()


class AgenteCotizador:
    def __init__(self, cliente: anthropic.Anthropic | None = None, motor: MotorCotizacion | None = None,
                 modelo: str = MODELO, esfuerzo: str = "high", carpeta_pdf: Path = Path("cotizaciones"),
                 empresa: Empresa | None = None, catalogo_vidrios: Path | None = None):
        self.cliente = cliente or anthropic.Anthropic()
        self.sesion = herramientas.Sesion(motor=motor, carpeta_pdf=Path(carpeta_pdf), empresa=empresa,
                                          ruta_catalogo_vidrios=catalogo_vidrios)
        self.modelo = modelo
        self.esfuerzo = esfuerzo
        self.mensajes: list[dict] = []  # solo se agrega al final: nunca se edita el historial

    def _llamar(self):
        return self.cliente.beta.messages.create(
            model=self.modelo,
            max_tokens=16000,
            system=[{"type": "text", "text": SISTEMA, "cache_control": {"type": "ephemeral"}}],
            tools=herramientas.DEFINICIONES,
            messages=self.mensajes,
            thinking={"type": "adaptive"},
            output_config={"effort": self.esfuerzo},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )

    def _resultado(self, bloque) -> dict:
        try:
            salida = herramientas.ejecutar(bloque.name, dict(bloque.input), self.sesion)
            return {"type": "tool_result", "tool_use_id": bloque.id,
                    "content": json.dumps(salida, ensure_ascii=False)}
        except Exception as e:  # dato inválido del modelo: se le devuelve para que corrija
            return {"type": "tool_result", "tool_use_id": bloque.id, "is_error": True,
                    "content": f"{type(e).__name__}: {e}"}

    def responder(self, texto: str) -> str:
        """Agrega el mensaje del cliente, resuelve las herramientas y devuelve la respuesta del agente."""
        self.mensajes.append({"role": "user", "content": texto})
        for _ in range(MAX_VUELTAS_HERRAMIENTAS):
            respuesta = self._llamar()
            self.mensajes.append({"role": "assistant", "content": respuesta.content})

            if respuesta.stop_reason == "refusal":
                return "No puedo ayudar con esa solicitud. Si es un tema de cotización, por favor reformúlelo."
            if respuesta.stop_reason == "max_tokens":
                return _a_texto(respuesta.content) + "\n\n[Respuesta cortada por longitud.]"
            if respuesta.stop_reason != "tool_use":
                return _a_texto(respuesta.content)

            usos = [b for b in respuesta.content if b.type == "tool_use"]
            self.mensajes.append({"role": "user", "content": [self._resultado(b) for b in usos]})
        return "La consulta requirió demasiados pasos. Por favor resuma lo que necesita y lo retomo."
