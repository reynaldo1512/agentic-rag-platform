from fastapi import APIRouter
 
from app.schemas.chat import ChatRequest, ChatResponse
 
router = APIRouter(tags=["Chat"])
 
PLACEHOLDER_REPLY = (
    "Soy un agente de demostración. Todavía no tengo lógica de Agentic RAG "
    "implementada: esta es una respuesta fija de bootstrap."
)
 
 
@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Envía un mensaje al agente (placeholder)",
)
async def send_message(payload: ChatRequest) -> ChatResponse:
    """Recibe un mensaje y devuelve una respuesta fija (sin IA real todavía)."""
    return ChatResponse(reply=PLACEHOLDER_REPLY, received_message=payload.message)
