# ---------------- Base Layer ----------------
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/root/project/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    make && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /root/project

COPY src src
COPY pyproject.toml uv.lock ./
RUN uv sync --no-reinstall


# ---------------- Production Stage ----------------
FROM base AS prod

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "--max-requests", "100", "--preload"]


# ---------------- Development Stage ----------------
FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
    git iputils-ping openssh-client && rm -rf /var/lib/apt/lists/*

RUN uv sync --only-group dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
