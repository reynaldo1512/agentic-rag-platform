"""Schemas del endpoint de chat."""
from typing import List
from pydantic import BaseModel, Field
 
 
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
 	
 
class ChatResponse(BaseModel):
    reply: str = Field(..., description="Respuesta del agente.")
    received_message: str = Field(..., description="Eco del mensaje recibido.")
    sources: List[str] = Field(default=[], description="URLs de las fuentes usadas.")
