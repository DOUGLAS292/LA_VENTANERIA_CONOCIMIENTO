"""Modelos de datos del contrato Agente <-> API (ver CONTRATO_API.md)."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --- Catálogo -------------------------------------------------------------

class Sistema(BaseModel):
    codigo: str
    nombre: str
    ancho_min_mm: int
    ancho_max_mm: int
    alto_min_mm: int
    alto_max_mm: int
    vidrios_permitidos: list[str]
    colores_permitidos: list[str]


class Vidrio(BaseModel):
    codigo: str
    nombre: str


class Catalogo(BaseModel):
    version_precios: str
    sistemas: list[Sistema]
    vidrios: list[Vidrio]


# --- Solicitud ------------------------------------------------------------

class ItemSolicitud(_Estricto):
    sistema: str
    ancho_mm: int = Field(gt=0)
    alto_mm: int = Field(gt=0)
    cantidad: int = Field(ge=1, le=500)
    vidrio: str
    color_perfil: str
    piso: int = Field(ge=1)


class SolicitudCotizacion(_Estricto):
    referencia_cliente: str = Field(min_length=1, max_length=120)
    ciudad: str = Field(min_length=1)
    items: list[ItemSolicitud] = Field(min_length=1, max_length=50)


# --- Respuesta ------------------------------------------------------------

class Material(BaseModel):
    concepto: str
    cantidad: float
    unidad: str
    valor: int


class ItemCotizado(BaseModel):
    indice: int
    descripcion: str
    cantidad: int
    precio_unitario: int
    subtotal: int
    materiales: list[Material] = []


class Alerta(BaseModel):
    codigo: str
    nivel: Literal["informativa", "ingenieria"]
    indice_item: int | None = None
    mensaje: str


class RespuestaCotizacion(BaseModel):
    cotizacion_id: str
    estado: Literal["firme", "preliminar"]
    moneda: Literal["COP"] = "COP"
    version_precios: str
    vigencia_dias: int
    items: list[ItemCotizado]
    subtotal: int
    iva: int
    total: int
    alertas: list[Alerta] = []


# --- Errores --------------------------------------------------------------

class ErrorCotizacion(Exception):
    """Dato inválido que el usuario puede corregir (HTTP 400 del contrato)."""

    def __init__(self, codigo: str, mensaje: str, indice_item: int | None = None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje
        self.indice_item = indice_item


class FallaMotor(Exception):
    """Falla técnica del motor (401, 429, 500, red). No es culpa del usuario."""
