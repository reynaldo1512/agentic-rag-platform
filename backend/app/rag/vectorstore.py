"""Gestion del vector store con ChromaDB."""
import logging
from functools import lru_cache
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from app.core.config import get_settings
from app.rag.embeddings import get_embeddings
from app.rag.loaders import load_and_split
 
logger = logging.getLogger(__name__)
 
 
@lru_cache
def get_vectorstore() -> Chroma:
    """
    Inicializa ChromaDB.
    Si la coleccion ya existe en disco (chroma_persist_dir), la reutiliza.
    Si esta vacia, indexa los documentos de settings.index_urls.
    """
    settings = get_settings()
    embeddings = get_embeddings()
 
    vs = Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_dir,
    )
 
    if vs._collection.count() == 0:
        logger.info("Coleccion vacia. Indexando documentos de index_urls...")
        splits = load_and_split(settings.index_urls)
        if splits:
            vs.add_documents(splits)
            logger.info("Indexacion completada: %d chunks.", len(splits))
 
    return vs
 
 
def get_retriever() -> VectorStoreRetriever:
    """Retriever de ChromaDB configurado para devolver los 6 documentos mas similares."""
    return get_vectorstore().as_retriever(search_kwargs={"k": 6})
