"""
Schemas de la API relacionados con el estado general de la aplicación.
"""

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Respuesta del endpoint raíz `GET /`."""

    application: str = Field(..., description="Nombre de la aplicación.")
    version: str = Field(..., description="Versión actual de la aplicación.")


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud `GET /health`."""

    status: str = Field(..., description="Estado de salud del servicio.")
