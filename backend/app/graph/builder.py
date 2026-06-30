"""Constructor y compilador del grafo de LangGraph."""
import logging
from functools import lru_cache
from langgraph.graph import StateGraph, END
from app.agents.coordinator import CoordinatorAgent
from app.agents.retriever import RetrieverAgent
from app.agents.generator import GeneratorAgent
from app.agents.evaluator import EvaluatorAgent
from app.graph.state import GraphState
 
logger = logging.getLogger(__name__)
 
MAX_RETRIES = 2  # numero maximo de vueltas a web_search antes de generar igual
 
 
def _decide_after_grading(state: GraphState) -> str:
    """
    Edge condicional tras grade_documents.
 
    - Si hay documentos relevantes -> generate.
    - Si NO hay documentos relevantes y aun quedan reintentos -> web_search.
    - Si NO hay documentos relevantes y se agotaron los reintentos ->
      generate de todas formas, con lo que haya (mejor una respuesta
      imperfecta que un loop infinito).
    """
    if state["web_search_needed"] != "Yes":
        return "generate"
 
    if state["retry_count"] >= MAX_RETRIES:
        logger.warning(
            "[Builder] Limite de %d reintentos alcanzado. Generando con lo disponible.",
            MAX_RETRIES,
        )
        return "generate"
 
    return "web_search"
 
 
@lru_cache
def build_graph():
    """
    Construye y compila el grafo de Adaptive RAG.
    Cacheado: solo se construye una vez durante la vida de la aplicacion.
    """
    coordinator = CoordinatorAgent()
    retriever = RetrieverAgent()
    generator = GeneratorAgent()
    evaluator = EvaluatorAgent()
 
    workflow = StateGraph(GraphState)
 
    workflow.add_node("retrieve", retriever.retrieve)
    workflow.add_node("web_search", retriever.web_search)
    workflow.add_node("grade_documents", retriever.grade_documents)
    workflow.add_node("transform_query", generator.transform_query)
    workflow.add_node("generate", generator.generate)
 
    workflow.set_conditional_entry_point(
        coordinator.route,
        {"vectorstore": "retrieve", "web_search": "web_search"},
    )
 
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_edge("web_search", "grade_documents")
 
    # CORREGIDO: antes faltaba la rama hacia web_search.
    # Ahora: sin docs relevantes -> web_search (con limite) -> grade_documents
    # de nuevo. Si se agota el limite, se genera igual.
    workflow.add_conditional_edges(
        "grade_documents",
        _decide_after_grading,
        {"web_search": "web_search", "generate": "generate"},
    )
 
    workflow.add_conditional_edges(
        "generate",
        evaluator.decide_after_generation,
        {"useful": END, "not_useful": "transform_query", "generate": "generate"},
    )
    workflow.add_edge("transform_query", "retrieve")
 
    graph = workflow.compile()
    logger.info("Grafo de Adaptive RAG compilado correctamente.")
    return graph