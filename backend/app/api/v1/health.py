"""
Endpoints relacionados con el estado de salud del servicio.
"""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verifica el estado de salud del servicio",
)
async def health_check() -> HealthResponse:
    """
    Devuelve el estado de salud del Backend.

    Utilizado por el Frontend (Dashboard) y por herramientas de
    orquestación (por ejemplo, healthchecks de Docker) para verificar
    que el servicio está operativo.
    """
    return HealthResponse(status="ok")
