# Testes

## Stack de testes

| Pacote | Versão | Função |
|---|---|---|
| `pytest` | >=8.0 | Runner principal |
| `pytest-asyncio` | >=0.24 | Suporte a testes `async/await` |
| `httpx` | >=0.27 | Cliente HTTP assíncrono para testar a API |

Todos como dependências de desenvolvimento em `[dependency-groups] dev`.

---

## Configuração

Em `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- `asyncio_mode = "auto"` — todo teste `async def` é reconhecido automaticamente pelo pytest-asyncio, sem precisar de `@pytest.mark.asyncio` em cada um.
- `testpaths` — pytest busca testes apenas dentro de `tests/`.

---

## Estrutura

```
tests/
├── __init__.py
├── conftest.py      # Fixtures compartilhadas
└── test_health.py   # Testes do endpoint /health
```

---

## Fixtures (`conftest.py`)

### `client`

Fixture principal. Sobe a aplicação em memória com `httpx.AsyncClient` + `ASGITransport` (sem porta, sem rede real) e injeta duas dependências mockadas:

**Override de `get_db`**

Substitui a dependência real do banco por um `AsyncMock`, isolando os testes de qualquer conexão com PostgreSQL:

```python
async def override_get_db():
    yield mock_session

app.dependency_overrides[get_db] = override_get_db
```

**Mock do engine no lifespan**

O `lifespan` do FastAPI chama `engine.connect()` e `engine.dispose()` no startup/shutdown. Como `AsyncEngine.connect` é um atributo read-only (não pode ser patchado diretamente), o engine inteiro é substituído por um `MagicMock`:

```python
mock_engine = MagicMock()
mock_engine.connect.return_value = AsyncMock()  # async context manager
mock_engine.dispose = AsyncMock()               # awaitable

with patch("app.main.engine", mock_engine):
    ...
```

A fixture retorna `(ac, mock_session)` para que os testes possam verificar chamadas ao banco.

---

## Testes do `/health`

| Teste | O que valida |
|---|---|
| `test_health_returns_200` | Status HTTP 200 |
| `test_health_returns_ok` | Body `{"status": "ok"}` |
| `test_health_executes_db_query` | `session.execute()` foi chamado (query no banco) |

---

## Como rodar

```bash
# Todos os testes
uv run pytest

# Com saída detalhada
uv run pytest -v

# Um arquivo específico
uv run pytest tests/test_health.py
```

---

## Decisões de Design

### Testes unitários, não de integração
Os testes mocam o banco de dados intencionalmente. Isso torna a suite rápida e independente de infraestrutura (não precisa de Postgres rodando).

Para testes de integração (que acessam um banco real), a abordagem recomendada é usar um banco PostgreSQL dedicado para testes, configurado via variável de ambiente `TEST_DATABASE_URL`, e gerenciar as migrations com Alembic antes de cada sessão de testes.

### `ASGITransport` vs `TestClient`
O `httpx.AsyncClient` com `ASGITransport` permite testar endpoints assíncronos sem subir um servidor HTTP real, mantendo o event loop do pytest-asyncio.
