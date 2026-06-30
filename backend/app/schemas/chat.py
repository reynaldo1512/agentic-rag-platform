from pydantic import BaseModel, Field
 
 
class ChatRequest(BaseModel):
    """Cuerpo de la petición POST /api/v1/chat."""
 
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Mensaje enviado por el usuario al agente.",
    )
 
 
class ChatResponse(BaseModel):
    """Respuesta del endpoint POST /api/v1/chat."""
 
    reply: str = Field(..., description="Respuesta del agente.")
    received_message: str = Field(
        ..., description="Eco del mensaje original, para verificar el contrato."
    )
