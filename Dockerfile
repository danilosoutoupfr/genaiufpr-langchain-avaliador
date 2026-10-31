# Build stage
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_PREFERENCE=only-system

COPY src/pyproject.toml src/uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY src/ .
RUN uv sync --frozen --no-dev

# Runtime stage
FROM python:3.14-slim

# Cria um grupo e usuário sem privilégios de root para segurança
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup --no-create-home appuser

WORKDIR /app

# Copia os arquivos da aplicação com permissão para o usuário não-root
COPY --from=builder --chown=appuser:appgroup /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]