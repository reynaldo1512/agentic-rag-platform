"""Proveedor de embeddings usando OpenAI."""
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings
 
 
@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    """Instancia unica de OpenAIEmbeddings (cacheada)."""
    settings = get_settings()
    return OpenAIEmbeddings(api_key=settings.openai_api_key)
