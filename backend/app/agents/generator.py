"""Agente generador: produce la respuesta final y reescribe preguntas."""
import logging
from app.graph import state
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from app.core.config import get_settings
from app.graph.state import GraphState
from app.prompts.templates import generation_prompt, rewrite_prompt
 
logger = logging.getLogger(__name__)
 
 
class GeneratorAgent:
    """Genera respuestas con el LLM y reformula preguntas cuando es necesario."""
 
    def __init__(self) -> None:
        settings = get_settings()
        llm = ChatOpenAI(
            model=settings.model_name, temperature=0, api_key=settings.openai_api_key
        )
        self._rag_chain = generation_prompt | llm | StrOutputParser()
        self._rewrite_chain = rewrite_prompt | llm | StrOutputParser()
 
    def generate(self, state: GraphState) -> GraphState:
        """Genera una respuesta usando los documentos del estado como contexto."""
        question = state["question"]
        documents = state["documents"]
        # Se incrementa cada vez que se entra a generate, sin importar
        # el motivo (primera vez o reintento por alucinación).
        attempts = state.get("generation_attempts", 0) + 1
        context = "\n\n".join(doc.page_content for doc in documents)

        formatted_prompt = generation_prompt.format_messages(context=context, question=question)
        logger.info(
            "[Generator] -> OpenAI (intento %d) | Prompt enviado:\n%s",
            attempts, formatted_prompt,
            )

        generation = self._rag_chain.invoke({"context": context, "question": question})
        logger.info("[Generator] <- OpenAI | Respuesta:\n%s", generation)
        return {
                 "generation": generation,
                "documents": documents,
                "question": question,
                "generation_attempts": attempts,
        }
 
    def transform_query(self, state: GraphState) -> GraphState:
        """Reescribe la pregunta para mejorar la recuperación."""
        question = state["question"]
        retry_count = state.get("retry_count", 0) + 1

        formatted_prompt = rewrite_prompt.format_messages(question=question)
        logger.info("[Generator] -> OpenAI (rewrite) | Prompt:\n%s", formatted_prompt)

        new_question = self._rewrite_chain.invoke({"question": question})
        logger.info(
            "[Generator] Pregunta reformulada (intento %d): '%s'",
            retry_count, new_question,
        )
        return {
            "question": new_question,
            "documents": state["documents"],
            "retry_count": retry_count,
            "generation_attempts": 0,  # nuevo contexto, reinicia el contador
        }