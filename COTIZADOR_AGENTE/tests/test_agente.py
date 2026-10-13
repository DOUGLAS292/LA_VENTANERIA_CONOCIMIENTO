"""Agente conversacional: herramientas técnicas y ciclo con la API (simulada, sin red)."""

import json

import anthropic
import httpx2 as httpx

from cotizador_agente import herramientas
from cotizador_agente.agente import MODELO, AgenteCotizador
from cotizador_agente.modelos import RespuestaCotizacion

# --- Herramientas ------------------------------------------------------------------


def test_presion_usa_el_mayor_entre_nsr10_y_tabla_alumina():
    # Bogotá a 30 m: la NSR-10 (región 3, exposición C) da más que la tabla de Alúmina
    p = herramientas.presion_viento("Bogotá", 30, 1.0, 1.5)
    assert p["presion_diseno_kgm2"] == max(p["presion_nsr10_kgm2"], p["presion_tabla_alumina_kgm2"])
    # Ciudad sin tabla del fabricante: solo NSR-10
    q = herramientas.presion_viento("Bucaramanga", 6, 1.0, 1.5)
    assert "presion_tabla_alumina_kgm2" not in q and q["presion_diseno_kgm2"] == q["presion_nsr10_kgm2"]


def test_ciudad_desconocida_no_se_adivina():
    assert "error" in herramientas.presion_viento("Pueblo Inventado", 6, 1, 1)


def test_comparar_series_en_barranquilla_descarta_las_livianas():
    p = herramientas.presion_viento("Barranquilla", 30, 1.0, 1.5)["presion_diseno_kgm2"]
    filas = {f["sistema"]: f for f in herramientas.comparar_series(1.0, 1.5, p)["series"]}
    assert not filas["alumina_serie_33"]["resiste"]
    assert filas["alumina_serie_50"]["opcion"] == "semirreforzados"
    assert "koncept_40" not in filas  # batiente: no tiene enganches


def test_verificar_perfil_grupo_inexistente_explica_los_grupos():
    r = herramientas.verificar_perfil("alumina_s3831", "enganches", 1.0, 1.5, 50)
    assert "vertical" in r["error"]


def test_listar_sistemas_trae_todas_las_series_y_lo_que_no_se_maneja():
    r = herramientas.listar_sistemas()
    codigos = {s["codigo"] for s in r["sistemas"]}
    assert {"koncept_70", "alumina_vc8025", "alumina_s3831"} <= codigos
    assert "serie 35 corrediza" in r["fuera_de_alcance"]


SOLICITUD = {"referencia_cliente": "Apto 502", "ciudad": "Cali", "items": [{
    "sistema": "K70", "ancho_mm": 2000, "alto_mm": 1500, "cantidad": 2,
    "vidrio": "INC5", "color_perfil": "blanco", "piso": 5}]}


class MotorDePrueba:
    def __init__(self):
        self.recibido = None

    def obtener_catalogo(self):
        raise NotImplementedError

    def cotizar(self, solicitud):
        self.recibido = solicitud
        return RespuestaCotizacion(cotizacion_id="T-1", estado="preliminar", version_precios="prueba",
                                   vigencia_dias=15, items=[], subtotal=0, iva=0, total=0)


def test_enviar_a_cotizar_sin_motor_deja_la_solicitud_lista():
    r = herramientas.enviar_a_cotizar(herramientas.Sesion(), SOLICITUD)
    assert r["estado"] == "pendiente_motor" and r["solicitud"]["items"][0]["cantidad"] == 2


def test_enviar_a_cotizar_pasa_la_solicitud_al_motor():
    motor = MotorDePrueba()
    r = herramientas.ejecutar("enviar_a_cotizar", {"solicitud": SOLICITUD}, herramientas.Sesion(motor=motor))
    assert r["estado"] == "cotizada" and motor.recibido.ciudad == "Cali"


def test_enviar_a_cotizar_rechaza_datos_invalidos():
    malo = {**SOLICITUD, "items": []}
    assert "error" in herramientas.enviar_a_cotizar(herramientas.Sesion(), malo)


# --- Ciclo del agente con la API simulada ----------------------------------------------

def _mensaje(contenido, stop_reason):
    return {"id": "msg_x", "type": "message", "role": "assistant", "model": MODELO,
            "content": contenido, "stop_reason": stop_reason, "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 10}}


def _cliente(respuestas):
    """Cliente real del SDK con transporte simulado: valida que el SDK acepte la petición."""
    peticiones = []

    def manejar(request: httpx.Request):
        peticiones.append({"headers": request.headers, "body": json.loads(request.content)})
        return httpx.Response(200, json=respuestas[len(peticiones) - 1])

    cliente = anthropic.Anthropic(api_key="prueba", max_retries=0,
                                  http_client=httpx.Client(transport=httpx.MockTransport(manejar)))
    return cliente, peticiones


def test_agente_llama_herramienta_y_responde():
    cliente, peticiones = _cliente([
        _mensaje([{"type": "tool_use", "id": "tu_1", "name": "presion_viento",
                   "input": {"ciudad": "Barranquilla", "altura_edificio_m": 30, "ancho_m": 1.0, "alto_m": 1.5}}],
                 "tool_use"),
        _mensaje([{"type": "text", "text": "La presión de diseño es 171 kg/m²."}], "end_turn"),
    ])
    agente = AgenteCotizador(cliente=cliente)
    assert agente.responder("Ventana en Barranquilla, piso 10") == "La presión de diseño es 171 kg/m²."

    primera, segunda = peticiones
    assert primera["body"]["model"] == "claude-opus-5-5"
    assert primera["body"]["thinking"] == {"type": "adaptive"}
    assert primera["body"]["fallbacks"] == "default"
    assert "server-side-fallback-2026-07-01" in primera["headers"]["anthropic-beta"]
    assert {t["name"] for t in primera["body"]["tools"]} >= {"presion_viento", "distribuir_vano", "enviar_a_cotizar"}
    resultado = segunda["body"]["messages"][-1]["content"][0]
    assert resultado["type"] == "tool_result" and resultado["tool_use_id"] == "tu_1"
    assert json.loads(resultado["content"])["presion_diseno_kgm2"] == 171
    # El historial solo crece: usuario, asistente, resultados, asistente
    assert [m["role"] for m in agente.mensajes] == ["user", "assistant", "user", "assistant"]


def test_error_de_herramienta_vuelve_al_modelo_para_corregir():
    cliente, peticiones = _cliente([
        _mensaje([{"type": "tool_use", "id": "tu_1", "name": "distribuir_vano",
                   "input": {"ancho_mm": 1500, "alto_vano_mm": 1200, "travesano_mm": 1500}}], "tool_use"),
        _mensaje([{"type": "text", "text": "Ajusto el travesaño."}], "end_turn"),
    ])
    AgenteCotizador(cliente=cliente).responder("vano de 1.50 x 1.20")
    resultado = peticiones[1]["body"]["messages"][-1]["content"][0]
    assert resultado["is_error"] is True and "760" in resultado["content"]


def test_rechazo_del_modelo_se_informa_al_cliente():
    cliente, _ = _cliente([_mensaje([], "refusal")])
    assert "No puedo ayudar" in AgenteCotizador(cliente=cliente).responder("...")
