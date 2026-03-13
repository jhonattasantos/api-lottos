# Setup: FastAPI + uv + Docker Compose + PostgreSQL

## Visão Geral

API de estudos (`api_lottos`) construída com FastAPI, gerenciada pelo `uv`, dockerizada com Docker Compose e banco de dados PostgreSQL.

---

## Stack

| Ferramenta | Versão | Função |
|---|---|---|
| Python | 3.12 | Runtime |
| FastAPI | >=0.115 | Framework web |
| uv | latest | Gerenciador de pacotes e ambiente |
| SQLAlchemy | >=2.0 | ORM (modo async) |
| asyncpg | >=0.29 | Driver async para PostgreSQL |
| Alembic | >=1.13 | Migrações de banco |
| pydantic-settings | >=2.0 | Configuração via variáveis de ambiente |
| PostgreSQL | 16 | Banco de dados |
| Docker Compose | v2 | Orquestração dos serviços |

---

## Estrutura de Arquivos

```
api_lottos/
├── app/
│   ├── __init__.py
│   ├── main.py          # Instância FastAPI, lifespan, inclusão de routers
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # Engine async, sessão e dependência get_db
│   └── routers/
│       ├── __init__.py
│       └── health.py    # GET /health
├── docs/
│   └── setup.md         # Este arquivo
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .python-version      # 3.12
├── .env                 # Variáveis locais (não commitado)
└── .env.example         # Template de variáveis
```

---

## Decisões de Design

### uv como gerenciador
O `uv` substitui `pip` + `venv` + `pip-tools`. O `uv.lock` garante builds reproduzíveis. O Dockerfile usa a imagem oficial `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` que já inclui uv e Python.

### SQLAlchemy async
O engine é criado com `create_async_engine` e o driver `asyncpg`, mantendo compatibilidade total com o event loop do FastAPI. A sessão é injetada nas rotas via dependency injection (`Depends(get_db)`).

### Lifespan
O `lifespan` do FastAPI verifica a conexão com o banco no startup e faz `dispose()` do engine no shutdown, evitando conexões penduradas.

### Health check com validação real
O endpoint `GET /health` executa `SELECT 1` no banco antes de retornar `{"status": "ok"}`, confirmando que a conexão com o PostgreSQL está ativa.

### Docker Compose healthcheck
O serviço `db` expõe um `healthcheck` via `pg_isready`. O serviço `app` usa `condition: service_healthy`, garantindo que a API só sobe após o Postgres estar pronto para aceitar conexões.

### Hot reload em desenvolvimento
O `docker-compose.yml` sobrescreve o `CMD` do Dockerfile com `fastapi dev`, que habilita o watcher de arquivos. O código local é montado via volume (`.:/app`), então qualquer alteração é refletida no container sem precisar rebuildar. Um volume anônimo em `/app/.venv` protege as dependências instaladas no container de serem sobrescritas pela pasta local:

```yaml
command: uv run fastapi dev app/main.py --host 0.0.0.0
volumes:
  - .:/app
  - /app/.venv
```

---

## Variáveis de Ambiente

Copie `.env.example` para `.env` antes de rodar:

```bash
cp .env.example .env
```

| Variável | Descrição | Padrão |
|---|---|---|
| `DATABASE_URL` | URL de conexão async com o Postgres | `postgresql+asyncpg://postgres:postgres@db:5432/api_lottos` |
| `POSTGRES_USER` | Usuário do Postgres | `postgres` |
| `POSTGRES_PASSWORD` | Senha do Postgres | `postgres` |
| `POSTGRES_DB` | Nome do banco | `api_lottos` |

---

## Como Rodar

### Com Docker Compose (recomendado)

```bash
make setup   # primeira vez: configura, sobe, migra e semeia
make up      # demais vezes
```

### Localmente (sem Docker)

Requer Postgres rodando localmente. Ajuste `DATABASE_URL` no `.env` apontando para `localhost`.

```bash
uv sync
uv run fastapi dev app/main.py
```

---

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica status da API e conexão com o banco |
| GET | `/docs` | Swagger UI (gerado automaticamente pelo FastAPI) |
| GET | `/redoc` | ReDoc UI |

### Exemplo de resposta — `/health`

```json
{"status": "ok"}
```

---

## Próximos Passos Sugeridos

- Configurar Alembic para migrações (`alembic init alembic`)
- Criar modelos SQLAlchemy em `app/models/`
- Adicionar schemas Pydantic em `app/schemas/`
- Estruturar routers de domínio em `app/routers/`
- Adicionar autenticação (JWT ou OAuth2)
- Configurar `pytest` + `pytest-asyncio` para testes
