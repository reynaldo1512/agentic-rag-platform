"""Endpoint de chat - conectado al grafo real de Adaptive RAG."""
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
 
router = APIRouter(tags=["Chat"])
_service = ChatService()
 
 
@router.post(
    "/chat", response_model=ChatResponse,
    summary="Envia un mensaje al agente Adaptive RAG",
)
async def send_message(payload: ChatRequest) -> ChatResponse:
    """
    Procesa el mensaje del usuario a traves del grafo de LangGraph:
    routing -> retrieval -> grading -> generation -> evaluation.
    """
    try:
        result = _service.chat(payload.message)
        return ChatResponse(
            reply=result["reply"],
            received_message=payload.message,
            sources=result["sources"],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
