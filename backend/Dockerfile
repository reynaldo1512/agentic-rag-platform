# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Instala UV (gestor de dependencias y entornos de Python)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copia únicamente los manifiestos primero para aprovechar la cache de capas
COPY pyproject.toml README.md ./

# Instala las dependencias del proyecto (sin instalar el propio paquete todavía)
RUN uv sync --no-install-project

# Copia el resto del código fuente
COPY . .

# Instala el proyecto ya con el código fuente disponible
RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
