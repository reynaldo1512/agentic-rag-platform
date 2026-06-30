"""Servicio de chat: orquesta el grafo de Adaptive RAG."""
import logging
from app.graph.builder import build_graph
 
logger = logging.getLogger(__name__)
 
 
class ChatService:
    """
    Capa de servicio entre el endpoint FastAPI y el grafo de LangGraph.
    El endpoint solo conoce este servicio; toda la logica de RAG queda
    encapsulada aqui y en los agentes.
    """
 
    def __init__(self) -> None:
        self._graph = build_graph()
 
    def chat(self, message: str) -> dict:
        """
        Ejecuta el grafo con el mensaje del usuario.
 
        Returns:
            dict con 'reply' (respuesta) y 'sources' (URLs de las fuentes).
        """
        logger.info("[ChatService] Pregunta: '%s'", message)
        inputs = {"question": message}
        final_state = None
 
        for output in self._graph.stream(inputs):
            final_state = output
 
        if final_state is None:
            return {"reply": "El agente no pudo generar una respuesta.", "sources": []}
 
        last = list(final_state.values())[-1]
        reply = last.get("generation", "Sin respuesta.")
        sources = list({
            doc.metadata.get("source", "")
            for doc in last.get("documents", [])
            if doc.metadata.get("source")
        })
 
        logger.info("[ChatService] Respuesta generada (%d chars).", len(reply))
        return {"reply": reply, "sources": sources}
