# Seeds

## Visão Geral

Padrão de seeds inspirado no Ruby on Rails para popular o banco com dados iniciais de forma organizada e idempotente. Os dados são gerados com a biblioteca `faker`.

## Dependência

`faker` é instalado como dependência de desenvolvimento:

```bash
uv add --group dev faker
```

O Dockerfile usa `--all-groups` para garantir que as deps de dev sejam instaladas no container:

```dockerfile
RUN uv sync --frozen --all-groups
```

---

## Estrutura

```
seeds/
├── __init__.py
├── runner.py       # Entrada principal — orquestra a ordem dos seeds
└── categories.py   # Seed de categorias
```

---

## Como Funciona

### `seeds/runner.py`

Equivalente ao `db/seeds.rb` do Rails. Abre uma sessão async com o banco e chama cada seed em ordem:

```python
async def run() -> None:
    async with AsyncSessionLocal() as session:
        await categories.seed(session)
        await session.commit()
```

Executado via:

```bash
uv run python -m seeds.runner
```

### `seeds/categories.py`

Cada entidade tem seu próprio arquivo com uma função `seed(session)`. Os dados são gerados com a biblioteca `faker` usando o locale `pt_BR`:

```python
from faker import Faker

fake = Faker("pt_BR")

async def seed(session: AsyncSession, count: int = 10) -> None:
    for _ in range(count):
        session.add(Category(name=fake.word().capitalize()))
    print(f"  -> categories: {count} registros ok")
```

`session.add()` sem `id` explícito — o Postgres gerencia a sequence automaticamente, sem risco de conflito de PK ao inserir registros via API depois.

---

## Rodando os Seeds

```bash
make seed
```

Executa `uv run python -m seeds.runner` dentro do container Docker, com o banco já disponível.

---

## Adicionando um Novo Seed

1. Criar `seeds/novo_model.py` com a função `seed`:

```python
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.novo_model import NovoModel

fake = Faker("pt_BR")

async def seed(session: AsyncSession, count: int = 10) -> None:
    for _ in range(count):
        session.add(NovoModel(name=fake.word().capitalize()))
    print(f"  -> novo_model: {count} registros ok")
```

2. Importar e chamar no `runner.py`:

```python
from seeds import categories, novo_model

async def run() -> None:
    async with AsyncSessionLocal() as session:
        await categories.seed(session)
        await novo_model.seed(session)
        await session.commit()
```

A ordem importa quando há dependências entre tabelas (ex: FK). Sempre seede a tabela pai antes da filha.
