.PHONY: setup up up-d down logs shell migrate migration seed worker flower worker-logs test

# Setup completo: limpa tudo, sobe os serviços, migra e semeia
setup:
	cp -n .env.example .env || true
	uv sync
	docker compose down -v
	docker compose up --build -d
	docker compose run --rm app uv run alembic upgrade head
	docker compose run --rm app uv run python -m seeds.runner
	@echo "Sistema disponível em http://localhost:8000"

# Sobe todos os serviços
up:
	docker compose up --build

# Sobe em background
up-d:
	docker compose up --build -d

# Derruba os serviços
down:
	docker compose down

# Logs em tempo real
logs:
	docker compose logs -f

# Shell dentro do container da app
shell:
	docker compose run --rm app bash

# Aplica todas as migrations pendentes
migrate:
	docker compose run --rm app uv run alembic upgrade head

# Cria uma nova migration: make migration name=create_users_table
migration:
	uv run alembic revision -m "$(name)"

# Roda os seeds no banco
seed:
	docker compose run --rm app uv run python -m seeds.runner

# Sobe o worker Celery
worker:
	docker compose up worker --build

# Sobe o Flower (monitoramento)
flower:
	docker compose --profile monitoring up flower --build

# Logs do worker em tempo real
worker-logs:
	docker compose logs -f worker

# Roda os testes localmente
test:
	uv run pytest -v
