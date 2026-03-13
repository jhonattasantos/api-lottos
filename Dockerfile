FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --all-groups

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY seeds/ ./seeds/

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0"]
