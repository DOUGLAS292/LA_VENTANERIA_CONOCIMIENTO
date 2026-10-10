"""Interfaz que cumple cualquier motor de cotización (simulado, Sergio u otro)."""

from typing import Protocol

from ..modelos import Catalogo, RespuestaCotizacion, SolicitudCotizacion


class MotorCotizacion(Protocol):
    def obtener_catalogo(self) -> Catalogo:
        """GET /v1/catalogo"""
        ...

    def cotizar(self, solicitud: SolicitudCotizacion) -> RespuestaCotizacion:
        """POST /v1/cotizaciones. Lanza ErrorCotizacion o FallaMotor."""
        ...
