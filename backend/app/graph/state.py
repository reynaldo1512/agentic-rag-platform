"""Estado compartido del grafo de LangGraph."""
from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
 
 
class GraphState(TypedDict):
    """
    Estado centralizado que fluye entre todos los nodos del grafo.

    Atributos:
        question:            Pregunta del usuario (puede reescribirse).
        generation:          Respuesta generada por el LLM.
        web_search_needed:   'Yes' o 'No', indica si se requiere búsqueda web.
        documents:           Documentos recuperados (vectorstore o web).
        retry_count:         Reintentos de RECUPERACIÓN (búsqueda de
                              documentos relevantes y de respuesta útil).
        generation_attempts: Reintentos de GENERACIÓN sobre el MISMO
                              contexto, cuando el LLM alucina. Distinto
                              de retry_count: este no cambia el contexto,
                              solo le da al LLM otra oportunidad de
                              redactar una respuesta fundamentada con lo
                              que ya tiene.
    """
    question: str
    generation: str
    web_search_needed: str
    documents: List[Document]
    retry_count: int
    generation_attempts: int