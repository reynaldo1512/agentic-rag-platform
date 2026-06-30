"""
Endpoint TEMPORAL de diagnostico del vectorstore.
 
ADVERTENCIA: este endpoint expone contenido interno de ChromaDB.
Util solo durante el desarrollo. Eliminar antes de produccion
(ver instrucciones de limpieza en la guia de diagnostico).
"""
from fastapi import APIRouter, Query
from app.rag.vectorstore import get_vectorstore
from app.schemas.debug import DocumentSample, VectorstoreDebugResponse
 
router = APIRouter(tags=["Debug (temporal)"])
 
 
@router.get(
    "/debug/vectorstore",
    response_model=VectorstoreDebugResponse,
    summary="[TEMPORAL] Inspecciona el contenido real indexado en ChromaDB",
)
async def debug_vectorstore(
    query: str = Query(
        default="Nutmeg investment outlook 2025",
        description="Query de prueba para la busqueda de similitud.",
    ),
    k: int = Query(default=5, ge=1, le=20, description="Numero de resultados a mostrar."),
) -> VectorstoreDebugResponse:
    """
    Muestra cuantos documentos hay indexados y como se ve su contenido
    real, para diagnosticar si el problema es de indexacion (loader)
    o de filtrado (grader).
    """
    vs = get_vectorstore()
    total = vs._collection.count()
 
    results = vs.similarity_search(query, k=k)
    samples = [
        DocumentSample(
            source=doc.metadata.get("source", "desconocido"),
            content_preview=doc.page_content[:300],
            content_length=len(doc.page_content),
        )
        for doc in results
    ]
 
    return VectorstoreDebugResponse(
        total_documents=total,
        query_used=query,
        samples=samples,
    )
