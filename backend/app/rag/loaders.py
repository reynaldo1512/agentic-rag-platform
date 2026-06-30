
"""Carga documentos desde URLs y los divide en chunks."""
import logging
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
 
logger = logging.getLogger(__name__)
 
# Etiquetas HTML donde normalmente vive el contenido real de un articulo,
# a diferencia de <nav>, <header>, <footer> que solo traen menus y enlaces.
_CONTENT_TAGS = ["article", "main"]
 
# Si ninguna de las etiquetas anteriores existe en la pagina (sitios mal
# estructurados), se usa este selector de respaldo basado en clases CSS
# comunes para el cuerpo de un articulo.
_FALLBACK_CLASSES = ["article-content", "post-content", "content-body"]
 
 
def _build_bs_strainer() -> bs4.SoupStrainer:
    """
    Construye un SoupStrainer que le dice a BeautifulSoup que SOLO
    parsee las etiquetas de contenido principal, ignorando todo el
    resto del HTML (nav, header, footer, scripts).
    """
    return bs4.SoupStrainer(_CONTENT_TAGS)
 
 
def load_and_split(
    urls: list[str], chunk_size: int = 500, chunk_overlap: int = 50
) -> list[Document]:
    """
    Descarga documentos desde las URLs dadas, extrae solo su contenido
    principal (descartando menus y pies de pagina) y los divide en chunks.
    Las URLs que fallen se omiten con un warning, sin detener el proceso.
    """
    docs: list[Document] = []
 
    for url in urls:
        try:
            loader = WebBaseLoader(
                url,
                bs_kwargs={"parse_only": _build_bs_strainer()},
            )
            loaded = loader.load()
 
            # Si el filtro de <article>/<main> no encontro nada (la
            # pagina no usa esas etiquetas), reintenta sin filtro para
            # no perder el documento por completo.
            if not loaded or not loaded[0].page_content.strip():
                logger.warning(
                    "No se encontro <article>/<main> en %s. "
                    "Cargando pagina completa sin filtrar.",
                    url,
                )
                loader = WebBaseLoader(url)
                loaded = loader.load()
 
            docs.extend(loaded)
            logger.info(
                "Documento cargado: %s (%d caracteres)",
                url, len(loaded[0].page_content) if loaded else 0,
            )
        except Exception as exc:
            logger.warning("No se pudo cargar %s: %s", url, exc)
 
    if not docs:
        logger.warning("No se cargo ningun documento. El vectorstore quedara vacio.")
        return []
 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = splitter.split_documents(docs)
    logger.info("%d chunks generados desde %d documentos.", len(splits), len(docs))
 
    # Diagnostico: muestra una muestra del contenido real extraido por
    # cada fuente, para confirmar visualmente que ya no es menu/footer.
    seen_sources = set()
    for doc in splits:
        source = doc.metadata.get("source", "desconocido")
        if source in seen_sources:
            continue
        seen_sources.add(source)
        preview = doc.page_content[:200].replace("\n", " ")
        logger.info("[LoaderDebug] %s -> %s", source, preview)
 
    return splits
