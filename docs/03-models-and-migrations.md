# Models e Migrations

## Visão Geral

Models SQLAlchemy com `DeclarativeBase` + Alembic configurado para engine assíncrona (`asyncpg`).

---

## Estrutura

```
app/
└── models/
    ├── __init__.py      # Re-exporta Base e todos os models
    ├── base.py          # DeclarativeBase compartilhada
    └── category.py      # Model Category

alembic/
├── env.py               # Configuração do Alembic (async)
├── script.py.mako       # Template de migration
└── versions/
    └── 20260312201734_create_categories_table.py

alembic.ini              # Configuração geral do Alembic
```

---

## Model: `Category`

```python
# app/models/category.py
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
```

Usa a API moderna do SQLAlchemy 2.0 com `Mapped` e `mapped_column` para type hints nativos.

---

## Base Declarativa

```python
# app/models/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

A `Base` é compartilhada por todos os models. O Alembic lê `Base.metadata` para detectar as tabelas no autogenerate.

---

## `app/models/__init__.py`

```python
from app.models.base import Base
from app.models.category import Category
```

Importar todos os models aqui garante que o Alembic consiga detectá-los via `Base.metadata` quando o `env.py` faz `from app.models import Base`.

---

## Configuração do Alembic

### `alembic.ini`

Duas configurações relevantes. A `sqlalchemy.url` fica em branco — a URL é injetada no `env.py` via `pydantic-settings`. O `file_template` define o formato de data no nome dos arquivos, igual ao padrão do Rails:

```ini
sqlalchemy.url =
file_template = %%(year)d%%(month).2d%%(day).2d%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s
```

Resultado: `20260312201734_create_categories_table.py`.

### `alembic/env.py`

Configurado para rodar com engine assíncrona usando `async_engine_from_config` + `asyncio.run`:

```python
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

async def run_migrations_online() -> None:
    connectable = async_engine_from_config(..., poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

asyncio.run(run_migrations_online())
```

`NullPool` é usado para que o Alembic abra e feche a conexão sem manter um pool, o que é o comportamento correto para migrações.

---

## Migrations

### Criar uma nova migration manualmente

```bash
uv run alembic revision -m "nome_da_migration"
```

### Criar com autogenerate (requer banco disponível)

```bash
uv run alembic revision --autogenerate -m "nome_da_migration"
```

> O autogenerate compara `Base.metadata` com o schema atual do banco e gera o diff automaticamente. Requer que o banco esteja acessível — dentro do Docker ou com `DATABASE_URL` apontando para um Postgres local.

### Aplicar migrations

```bash
# Dentro do container ou com Postgres local acessível
uv run alembic upgrade head
```

### Reverter a última migration

```bash
uv run alembic downgrade -1
```

### Ver histórico

```bash
uv run alembic history
uv run alembic current
```

---

## Fluxo com Docker

Para rodar as migrations no ambiente Docker:

```bash
# Subir apenas o banco
docker compose up db -d

# Rodar as migrations (com DATABASE_URL apontando para localhost)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/api_lottos \
  uv run alembic upgrade head

# Ou dentro do container da app
docker compose run --rm app uv run alembic upgrade head
```

---

## Adicionando Novos Models

1. Criar `app/models/novo_model.py` com a classe herdando de `Base`
2. Importar no `app/models/__init__.py`
3. Rodar `uv run alembic revision --autogenerate -m "descricao"`
4. Revisar o arquivo gerado em `alembic/versions/`
5. Aplicar com `uv run alembic upgrade head`
