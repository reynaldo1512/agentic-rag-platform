"""Plantillas de prompts para los componentes del Adaptive RAG."""
from langchain_core.prompts import ChatPromptTemplate
 
router_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un experto en enrutar preguntas a fuentes de datos correctas.\n"
     "El vectorstore contiene documentos sobre inversiones y perspectivas de Nutmeg.\n"
     "Usa 'vectorstore' para preguntas sobre ese tema.\n"
     "Usa 'web_search' para todo lo demas."),
    ("human", "{question}"),
])
 
retrieval_grader_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Evaluas la relevancia de documentos recuperados para una pregunta.\n"
     "Responde 'yes' si el documento es relevante, 'no' si no lo es."),
    ("human", "Documento:\n\n{document}\n\nPregunta: {question}"),
])
 
generation_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente para responder preguntas usando el contexto dado.\n"
     "Si no sabes la respuesta, dilo. Se conciso (maximo tres oraciones).\n\n"
     "Contexto: {context}"),
    ("human", "{question}"),
])
 
hallucination_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Verificas si una respuesta de LLM esta fundamentada en hechos recuperados.\n"
     "Responde 'yes' si esta fundamentada, 'no' si contiene informacion inventada."),
    ("human", "Hechos:\n\n{documents}\n\nRespuesta: {generation}"),
])
 
answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Determinas si una respuesta resuelve la pregunta del usuario.\n"
     "Responde 'yes' si la resuelve, 'no' si no lo hace."),
    ("human", "Pregunta: {question}\n\nRespuesta: {generation}"),
])
 
rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Optimizas preguntas para busqueda vectorial.\n"
     "Produce SOLO la pregunta reformulada, sin explicacion."),
    ("human", "Pregunta original: {question}\n\nReformula para mejor recuperacion:"),
])
