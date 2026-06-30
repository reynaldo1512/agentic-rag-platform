"""
Punto de entrada de la aplicación FastAPI.

Esta es la primera iteración (bootstrap) de Agentic RAG Platform.
Únicamente expone:

- `GET /`       → metadatos de la aplicación.
- `GET /health` → estado de salud del servicio.

La documentación interactiva queda disponible automáticamente en:

- Swagger UI → /docs
- ReDoc      → /redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.schemas.health import RootResponse

settings = get_settings()
configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Bootstrap de infraestructura de Agentic RAG Platform. "
        "Esta iteración no implementa todavía lógica de Agentic RAG."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get(
    "/",
    response_model=RootResponse,
    tags=["Root"],
    summary="Información general de la aplicación",
)
async def root() -> RootResponse:
    """Devuelve el nombre y la versión actual de la aplicación."""
    return RootResponse(application=settings.app_name, version=settings.app_version)
