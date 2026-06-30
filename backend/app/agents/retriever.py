"""Agente recuperador: busca en ChromaDB, en la web, y evalua relevancia."""
import logging
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document
from app.agents.schemas import GradeDocuments
from app.core.config import get_settings
from app.graph.state import GraphState
from app.prompts.templates import retrieval_grader_prompt
from app.rag.vectorstore import get_retriever
 
logger = logging.getLogger(__name__)
 
 
class RetrieverAgent:
    """Recupera documentos de ChromaDB o de la web, y filtra los no relevantes."""
 
    def __init__(self) -> None:
        settings = get_settings()
        llm = ChatOpenAI(
            model=settings.model_name, temperature=0, api_key=settings.openai_api_key
        )
        self._grader_chain = retrieval_grader_prompt | llm.with_structured_output(GradeDocuments)
        self._retriever = get_retriever()
        self._web_tool = TavilySearchResults(
            max_results=3, tavily_api_key=settings.tavily_api_key
        )
 
    def retrieve(self, state: GraphState) -> GraphState:
        """Recupera documentos del vectorstore."""
        question = state["question"]
        docs = self._retriever.invoke(question)
        logger.info("[Retriever] %d documentos recuperados.", len(docs))
        return {"documents": docs, "question": question}
 
    def web_search(self, state: GraphState) -> GraphState:
        """Busca en la web usando Tavily."""
        question = state["question"]
        logger.info("[Retriever] -> Tavily | Query enviada: '%s'", question)
        results = self._web_tool.invoke({"query": question})
        web_docs = [
            Document(page_content=r["content"], metadata={"source": r["url"]})
            for r in results
        ]
        docs = state.get("documents", []) + web_docs
        logger.info("[Retriever] %d documentos de web search.", len(web_docs))
        return {"documents": docs, "question": question}
 
    def grade_documents(self, state: GraphState) -> GraphState:
        """Filtra documentos no relevantes. Activa web_search si no queda ninguno."""
        question = state["question"]
        documents = state["documents"]
        retry_count = state.get("retry_count", 0)
        filtered, web_needed = [], "No"
 
        for i, doc in enumerate(documents):
            formatted_prompt = retrieval_grader_prompt.format_messages(
                document=doc.page_content, question=question
            )
            logger.info(
                "[Retriever] -> OpenAI (grading doc %d/%d) | Prompt:\n%s",
                i + 1, len(documents), formatted_prompt,
            )
            result = self._grader_chain.invoke(
                {"document": doc.page_content, "question": question}
            )
            logger.info("[Retriever] <- OpenAI | Score: %s", result.binary_score)
            
            if result.binary_score == "yes":
                filtered.append(doc)
 
        if not filtered:
            web_needed = "Yes"
            retry_count += 1
            logger.info(
                "[Retriever] Sin docs relevantes -> web_search activado (intento %d).",
                retry_count,
            )
        else:
            logger.info("[Retriever] %d docs relevantes.", len(filtered))
 
        return {
            "documents": filtered,
            "question": question,
            "web_search_needed": web_needed,
            "retry_count": retry_count,
        }