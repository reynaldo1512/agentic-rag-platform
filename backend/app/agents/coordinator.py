"""Agente coordinador: enruta preguntas a vectorstore o web search."""
import logging
from langchain_openai import ChatOpenAI
from app.agents.schemas import RouteQuery
from app.core.config import get_settings
from app.graph.state import GraphState
from app.prompts.templates import router_prompt
 
logger = logging.getLogger(__name__)
 
 
class CoordinatorAgent:
    """Decide si una pregunta debe resolverse con el vectorstore o con web search."""
 
    def __init__(self) -> None:
        settings = get_settings()
        llm = ChatOpenAI(
            model=settings.model_name, temperature=0, api_key=settings.openai_api_key
        )
        self._chain = router_prompt | llm.with_structured_output(RouteQuery)
 
    def route(self, state: GraphState) -> str:
        """Retorna 'vectorstore' o 'web_search' según la pregunta."""
        question = state["question"]
        formatted_prompt = router_prompt.format_messages(question=question)
        logger.info("[Coordinator] -> OpenAI | Prompt enviado:\n%s", formatted_prompt)

        result = self._chain.invoke({"question": question})
        logger.info("[Coordinator] <- OpenAI | Resultado: %s", result.datasource)
        return result.datasource