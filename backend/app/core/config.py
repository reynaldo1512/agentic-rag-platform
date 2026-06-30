from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
 
 
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8",
        case_sensitive=False, extra="ignore",
    )
 
    app_name: str = "Agentic RAG Platform"
    app_version: str = "1.0.0"
 
    openai_api_key: str | None = None
    tavily_api_key: str | None = None
    model_name: str = "gpt-4o-mini"
 
    # ChromaDB  <- NUEVO
    chroma_collection: str = "agentic_rag"
    chroma_persist_dir: str = "./data/chroma"
 
    # Documentos a indexar  <- NUEVO
    index_urls: list[str] = [
        "https://www.nutmeg.com/nutmegonomics/our-2025-investment-outlook",
        "https://www.nutmeg.com/nutmegonomics/nutmeg-investor-update-december-2024",
        "https://www.nutmeg.com/nutmegonomics/nutmeg-investor-update-november-2024",
        "https://www.nutmeg.com/nutmegonomics/nutmeg-investor-update-october-2024"
    ]
 
    log_level: str = "INFO"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173"]
 
 
@lru_cache
def get_settings() -> Settings:
    return Settings()
