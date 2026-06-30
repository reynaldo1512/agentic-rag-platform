"""Schemas Pydantic para las salidas estructuradas de los agentes."""
from typing import Literal
from pydantic import BaseModel, Field
 
 
class GradeDocuments(BaseModel):
    binary_score: str = Field(
        description="El documento es relevante para la pregunta? 'yes' o 'no'."
    )
 
class GradeHallucinations(BaseModel):
    binary_score: str = Field(
        description="La respuesta esta fundamentada en los documentos? 'yes' o 'no'."
    )
 
class GradeAnswer(BaseModel):
    binary_score: str = Field(
        description="La respuesta resuelve la pregunta? 'yes' o 'no'."
    )
 
class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "web_search"] = Field(
        description="Fuente de datos: 'vectorstore' o 'web_search'."
    )
