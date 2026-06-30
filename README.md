# Agentic RAG Platform

> Bootstrap de infraestructura para una plataforma de Retrieval-Augmented Generation orientada a agentes.

## Descripción

**Agentic RAG Platform** es la base sobre la que se construirá, en iteraciones futuras, un sistema de **Agentic RAG**: un workflow donde distintos agentes (coordinador, recuperador, generador, evaluador) colaboran —apoyados en LangGraph, un modelo de lenguaje y herramientas de búsqueda— para responder preguntas con contexto recuperado de una base documental propia.

Esta primera entrega **no implementa todavía esa lógica**. Su único propósito es dejar lista una infraestructura sólida, limpia y verificable:

- Un Backend en FastAPI que arranca, expone `/health` y documenta su propia API.
- Un Frontend en React que consulta ese Backend y refleja su estado en un Dashboard.
- Ambos servicios orquestados con Docker Compose, listos para ejecutarse con un solo comando.
- El esqueleto de carpetas y clases que ocupará el futuro pipeline de Agentic RAG, ya creado pero deliberadamente vacío.

Si puedes clonar este repositorio, levantarlo con Docker y ver el Dashboard reportando `🟢 Online`, el bootstrap cumplió su objetivo.

## Tecnologías

**Backend**

| Tecnología | Rol |
|---|---|
| Python 3.11 | Lenguaje base |
| FastAPI | Framework web y API |
| UV | Gestor de dependencias y entornos |
| Pydantic v2 | Validación de datos y configuración |
| LangGraph / LangChain | Dependencias preparadas para el futuro workflow de agentes |
| OpenAI SDK | Dependencia preparada para el futuro LLM |
| Tavily | Dependencia preparada para la futura búsqueda web |

**Frontend**

| Tecnología | Rol |
|---|---|
| React 18 + TypeScript | UI y tipado estático |
| Vite | Servidor de desarrollo y bundler |
| TailwindCSS | Estilos |
| Axios | Cliente HTTP |

**Infraestructura**

| Tecnología | Rol |
|---|---|
| Docker / Docker Compose | Orquestación de ambos servicios |

## Arquitectura

El proyecto sigue una separación clara entre Backend y Frontend, cada uno organizado por capas y responsabilidades. Dentro del Backend, el código de la aplicación convive con la estructura ya preparada para el futuro Agentic RAG (`graph/`, `agents/`, `rag/`), aislada del resto para que su implementación posterior no afecte lo ya construido.

```
agentic-rag-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/            # Endpoints HTTP (routers versionados)
│   │   │   └── v1/
│   │   ├── core/           # Configuración, logging y transversales
│   │   ├── graph/          # [vacío] Estado y construcción del grafo (LangGraph)
│   │   ├── agents/         # [vacío] Coordinador, retriever, generator, evaluator
│   │   ├── rag/            # [vacío] Retriever, vector store, embeddings, loaders
│   │   ├── prompts/        # [vacío] Plantillas de prompts
│   │   ├── services/       # [vacío] Lógica de orquestación / casos de uso
│   │   ├── models/         # [vacío] Modelos de dominio
│   │   ├── schemas/        # Contratos Pydantic de entrada/salida de la API
│   │   ├── utils/          # [vacío] Utilidades transversales
│   │   └── main.py         # Punto de entrada de FastAPI
│   ├── tests/               # Tests automatizados (pytest)
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/             # Cliente Axios base
│   │   ├── services/        # Capa de servicios (única autorizada a llamar a Axios)
│   │   ├── components/      # Componentes de presentación reutilizables
│   │   ├── pages/           # Páginas (en esta iteración, solo el Dashboard)
│   │   ├── types/           # Tipos TypeScript compartidos
│   │   └── utils/           # Hooks y utilidades
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
│
├── docs/                    # Documentación técnica adicional (futuras iteraciones)
├── data/                    # Fuente de documentos para el futuro pipeline de ingesta
├── docker-compose.yml
├── LICENSE
└── README.md
```

**Decisiones de diseño**

- La API está versionada desde el inicio (`api/v1/`) para no romper contratos cuando se agreguen nuevos endpoints.
- `schemas/` (contratos de la API) se mantiene separado de `models/` (futuro dominio interno), evitando que ambos conceptos se mezclen a medida que el proyecto crezca.
- El Frontend nunca llama a Axios directamente desde un componente: toda petición HTTP pasa por `services/`, lo que permite cambiar la implementación de red sin tocar la UI.
- Las carpetas del futuro Agentic RAG existen ya, pero contienen únicamente clases base sin lógica, para que la siguiente iteración tenga dónde escribir sin necesidad de reorganizar el proyecto.

## Requisitos

Para ejecutar el proyecto con Docker (recomendado):

- Docker Engine ≥ 24
- Docker Compose v2

Para ejecutar el proyecto en local (sin Docker):

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) instalado (`pip install uv` o ver su guía de instalación)
- Node.js ≥ 20 y npm

## Instalación

Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd agentic-rag-platform
```

## Variables de entorno

Cada servicio define su propio archivo de variables. Cópialos antes de ejecutar el proyecto:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**Backend (`backend/.env`)**

| Variable | Descripción | Uso en esta iteración |
|---|---|---|
| `OPENAI_API_KEY` | Clave de API de OpenAI | Declarada, no consumida |
| `TAVILY_API_KEY` | Clave de API de Tavily | Declarada, no consumida |
| `MODEL_NAME` | Nombre del modelo LLM a usar | Declarada, no consumida |
| `LOG_LEVEL` | Nivel de logging (`INFO`, `DEBUG`, ...) | Activa |
| `API_PORT` | Puerto en el que escucha el Backend | Activa |

**Frontend (`frontend/.env`)**

| Variable | Descripción |
|---|---|
| `VITE_API_URL` | URL base del Backend, consumida por la capa de servicios |

> En esta iteración, `OPENAI_API_KEY`, `TAVILY_API_KEY` y `MODEL_NAME` solo se cargan en la configuración de la aplicación; ninguna lógica de negocio las utiliza todavía.

## Ejecución local

**Backend**

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

**Frontend** (en otra terminal)

```bash
cd frontend
npm install
npm run dev
```

## Ejecución con Docker

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Esto construye y levanta ambos servicios. Para detenerlos:

```bash
docker compose down
```

## Acceso a la aplicación

| Recurso | URL |
|---|---|
| Frontend (Dashboard) | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

## Estructura del proyecto

| Carpeta | Responsabilidad |
|---|---|
| `backend/app/api/` | Define los endpoints HTTP expuestos por la API, organizados por versión. |
| `backend/app/core/` | Configuración de la aplicación (lectura de variables de entorno) y logging. |
| `backend/app/graph/` | Estado y construcción del futuro grafo de LangGraph. |
| `backend/app/agents/` | Agentes del futuro workflow (coordinador, retriever, generator, evaluator). |
| `backend/app/rag/` | Componentes del futuro pipeline de RAG (retriever, vector store, embeddings, loaders). |
| `backend/app/prompts/` | Plantillas de prompts para el futuro LLM. |
| `backend/app/services/` | Lógica de orquestación y casos de uso de la aplicación. |
| `backend/app/models/` | Modelos de dominio interno. |
| `backend/app/schemas/` | Contratos Pydantic de entrada/salida de la API. |
| `backend/app/utils/` | Utilidades transversales del Backend. |
| `backend/tests/` | Tests automatizados. |
| `frontend/src/api/` | Cliente Axios base, configurado mediante variables de entorno. |
| `frontend/src/services/` | Capa de servicios: única responsable de comunicarse con el Backend. |
| `frontend/src/components/` | Componentes de presentación reutilizables del Dashboard. |
| `frontend/src/pages/` | Páginas de la aplicación. |
| `frontend/src/types/` | Tipos TypeScript compartidos entre servicios, hooks y componentes. |
| `frontend/src/utils/` | Hooks y utilidades del Frontend. |
| `docs/` | Documentación técnica adicional del proyecto. |
| `data/` | Documentos fuente para el futuro pipeline de ingesta del RAG. |

## Próximos pasos

Esta iteración corresponde únicamente al bootstrap de infraestructura. Las siguientes iteraciones implementarán, sobre esta misma base:

- [ ] Integración real con LangGraph para orquestar el workflow de agentes.
- [ ] Integración con OpenAI como motor de generación.
- [ ] Integración con Tavily para búsqueda web complementaria.
- [ ] Pipeline de Retrieval sobre documentos propios.
- [ ] Generación de Embeddings y carga en un Vector Store.
- [ ] Implementación de los agentes: coordinador, retriever, generator y evaluator.
- [ ] Construcción del workflow completo de Agentic RAG y su exposición vía API.

## Licencia

Este proyecto se distribuye bajo licencia [MIT](./LICENSE).
