"""Schemas para el endpoint temporal de diagnostico del vectorstore."""
from typing import List
from pydantic import BaseModel, Field
 
 
class DocumentSample(BaseModel):
    source: str = Field(..., description="URL de origen del chunk.")
    content_preview: str = Field(..., description="Primeros 300 caracteres del chunk.")
    content_length: int = Field(..., description="Longitud total del chunk en caracteres.")
 
 
class VectorstoreDebugResponse(BaseModel):
    total_documents: int = Field(..., description="Numero total de chunks indexados en ChromaDB.")
    query_used: str = Field(..., description="Query de prueba usada para la busqueda.")
    samples: List[DocumentSample] = Field(..., description="Muestra de los documentos recuperados.")
