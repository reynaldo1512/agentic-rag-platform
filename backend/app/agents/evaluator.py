"""Agente evaluador: verifica alucinaciones y utilidad de la respuesta."""
import logging
from langchain_openai import ChatOpenAI
from app.agents.schemas import GradeHallucinations, GradeAnswer
from app.core.config import get_settings
from app.graph.state import GraphState
from app.prompts.templates import hallucination_prompt, answer_prompt
 
logger = logging.getLogger(__name__)
 
MAX_RETRIES = 2  # debe coincidir con el limite usado en graph/builder.py
 
 
class EvaluatorAgent:
    """Evalua si la respuesta generada esta fundamentada y es util."""
 
    def __init__(self) -> None:
        settings = get_settings()
        llm = ChatOpenAI(
            model=settings.model_name, temperature=0, api_key=settings.openai_api_key
        )
        self._hall_chain = hallucination_prompt | llm.with_structured_output(GradeHallucinations)
        self._ans_chain = answer_prompt | llm.with_structured_output(GradeAnswer)
 
    def decide_after_generation(self, state: GraphState) -> str:
        """
        Edge condicional post-generacion.
        Retorna: 'useful' | 'not_useful' | 'generate'

        Diseño óptimo para RAG: si la respuesta no está fundamentada,
        primero se le da al LLM una segunda oportunidad de regenerar
        CON EL MISMO contexto (generation_attempts), por si fue un
        error puntual de redacción. Si ya se agotó esa oportunidad y
        sigue alucinando, el problema es el contexto en sí -> se manda
        a transform_query para buscar mejor contexto, no a seguir
        generando con lo mismo (eso sí sería un loop sin sentido).

        Como red de seguridad final, retry_count (compartido con el
        ciclo de recuperación) sigue limitando el total de vueltas
        del grafo completo, sin importar por qué motivo se reintenta.
        """
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        retry_count = state.get("retry_count", 0)
        generation_attempts = state.get("generation_attempts", 0)
        docs_text = "\n\n".join(doc.page_content for doc in documents)

        formatted_hall_prompt = hallucination_prompt.format_messages(
            documents=docs_text, generation=generation
        )
        logger.info("[Evaluator] -> OpenAI (hallucination) | Prompt:\n%s", formatted_hall_prompt)
        hall = self._hall_chain.invoke({"documents": docs_text, "generation": generation})
        logger.info("[Evaluator] <- OpenAI | Fundamentada: %s", hall.binary_score)

        if hall.binary_score != "yes":
            # Límite global absoluto: nunca seguir sin importar el motivo.
            if retry_count >= MAX_RETRIES:
                logger.warning(
                    "[Evaluator] Limite global de %d reintentos alcanzado. "
                    "Entregando respuesta de todas formas.",
                    MAX_RETRIES,
                )
                return "useful"

            # Primer fallo sobre este contexto: una segunda oportunidad
            # de regenerar, sin gastar una vuelta de retrieval todavia.
            if generation_attempts < 2:
                logger.info(
                    "[Evaluator] Respuesta no fundamentada (intento %d). "
                    "Reintentando generacion con el mismo contexto.",
                    generation_attempts,
                )
                return "generate"

            # Ya se le dio una segunda oportunidad y sigue alucinando:
            # el contexto en si es insuficiente, hay que cambiarlo.
            logger.info(
                "[Evaluator] El contexto actual no permite una respuesta "
                "fundamentada tras %d intentos. Reformulando pregunta.",
                generation_attempts,
            )
            return "not_useful"  # reutiliza el edge existente -> transform_query

        formatted_ans_prompt = answer_prompt.format_messages(
            question=question, generation=generation
        )
        logger.info("[Evaluator] -> OpenAI (answer check) | Prompt:\n%s", formatted_ans_prompt)
        ans = self._ans_chain.invoke({"question": question, "generation": generation})
        logger.info("[Evaluator] <- OpenAI | Util: %s", ans.binary_score)

        if ans.binary_score == "yes":
            return "useful"

        if retry_count >= MAX_RETRIES:
            logger.warning(
                "[Evaluator] Limite de %d reintentos alcanzado. "
                "Entregando la mejor respuesta disponible aunque no sea optima.",
                MAX_RETRIES,
            )
            return "useful"

        return "not_useful"
    