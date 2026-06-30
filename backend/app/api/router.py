"""
Router agregador de la versión 1 (v1) de la API.

Centraliza el registro de todos los routers de esta versión.
A medida que el proyecto crezca, cada nuevo dominio (por ejemplo,
`chat`, `documents`, `agents`) deberá registrar aquí su propio router.
"""

from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.debug import router as debug_router
from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(chat_router, prefix="/api/v1")
api_router.include_router(debug_router, prefix="/api/v1")
