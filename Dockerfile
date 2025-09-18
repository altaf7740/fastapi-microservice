# ---------------- Base Layer ----------------
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/root/project/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    make && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /root/project

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-reinstall  


# ---------------- Production Stage ----------------
FROM base AS prod

COPY src .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ---------------- Development Stage ----------------
FROM base AS dev

RUN apt-get update && apt-get install -y --no-install-recommends \
    git iputils-ping openssh-client && rm -rf /var/lib/apt/lists/*

# Install dev deps on top of base deps
RUN uv sync --only-group dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]