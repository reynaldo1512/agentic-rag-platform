"""
Configuración central de la aplicación.

Este módulo define la clase `Settings`, responsable de leer y validar
las variables de entorno del Backend mediante Pydantic Settings.

En esta iteración (bootstrap) las variables relacionadas con proveedores
externos (OpenAI, Tavily) y con el modelo LLM se declaran y se cargan,
pero todavía NO se utilizan en ninguna lógica de negocio.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde variables de entorno.

    Los valores se leen desde un archivo `.env` en la raíz del backend
    (ver `.env.example`) o directamente desde el entorno de ejecución
    (por ejemplo, variables inyectadas por Docker Compose).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Metadatos de la aplicación
    app_name: str = "Agentic RAG Platform"
    app_version: str = "1.0.0"

    # Proveedores externos (uso futuro: Agentic RAG)
    openai_api_key: str | None = None
    tavily_api_key: str | None = None

    # Modelo LLM (uso futuro: nodos del grafo)
    model_name: str = "gpt-4o-mini"

    # Aplicación
    log_level: str = "INFO"
    api_port: int = 8000

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    """
    Devuelve una instancia única (cacheada) de `Settings`.

    El uso de `lru_cache` evita volver a leer y validar las variables
    de entorno en cada inyección de dependencia.
    """
    return Settings()
