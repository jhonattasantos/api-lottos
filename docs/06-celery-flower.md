# Celery + Flower

## Visão Geral

Processamento de tarefas assíncronas com Celery, Redis como broker e result backend, e Flower para monitoramento.

---

## Stack

| Ferramenta | Versão | Função |
|---|---|---|
| `celery[redis]` | >=5.4 | Task queue |
| `redis` | >=5.0 | Cliente Redis (broker + result backend) |
| `flower` | >=2.0 | UI de monitoramento do Celery |
| Redis | 7 | Broker (DB 0) e result backend (DB 1) |

`celery` e `redis` são dependências de produção. `flower` fica no grupo `monitoring`:

```toml
[project]
dependencies = [
    ...
    "celery[redis]>=5.4.0",
    "redis>=5.0.0",
]

[dependency-groups]
monitoring = [
    "flower>=2.0.1",
]
```

---

## Arquitetura

```
POST /categories/
      |
  FastAPI endpoint
      |
  db.commit()          ← persiste no Postgres
      |
  .delay(id)           ← serializa task como mensagem JSON
      |
      ▼
  Redis DB 0           ← broker (fila)
      |
      ▼
  Celery Worker        ← consome a mensagem
      |
  asyncio.run()        ← cria event loop isolado
      |
  AsyncSessionLocal    ← nova sessão SQLAlchemy
      |
  await session.get()  ← query no Postgres
      |
      ▼
  Redis DB 1           ← result backend (resultado da task)
      |
      ▼
  Flower               ← monitora filas e resultados
```

---

## Estrutura de Arquivos

```
app/
├── worker.py           # Instância Celery + configuração
└── tasks/
    ├── __init__.py
    └── categories.py   # Tasks do domínio de categorias
```

---

## `app/worker.py`

Instância central do Celery. Lê a configuração via `settings` e registra os módulos de tasks via `autodiscover_tasks`:

```python
celery_app = Celery("api_lottos")

celery_app.config_from_object({
    "broker_url": settings.CELERY_BROKER_URL,
    "result_backend": settings.CELERY_RESULT_BACKEND,
    "task_track_started": True,   # Flower mostra tasks em execução
    "task_acks_late": True,        # re-enfileira se o worker morrer
    "worker_prefetch_multiplier": 1,
})

celery_app.autodiscover_tasks(["app.tasks"])
```

---

## Tasks com SQLAlchemy Async

Celery workers são síncronos por padrão (pool `prefork`). Para acessar o banco com `asyncpg`, cada task cria um event loop isolado com `asyncio.run()` e uma nova sessão SQLAlchemy:

```python
def run_async(coro):
    return asyncio.run(coro)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_after_create(self, category_id: int):
    async def _run():
        async with AsyncSessionLocal() as session:
            category = await session.get(Category, category_id)
            return {"status": "processed", "id": category_id}

    try:
        return run_async(_run())
    except Exception as exc:
        raise self.retry(exc=exc)
```

**Regras importantes:**

| Regra | Motivo |
|---|---|
| Passar apenas IDs primitivos (`int`, `str`) | Objetos ORM não são serializáveis para JSON |
| Criar nova `AsyncSessionLocal()` por task | Nunca reutilizar a sessão do FastAPI |
| Usar `asyncio.run()`, nunca `get_event_loop()` | `get_event_loop()` está deprecated no Python 3.12 |
| Tasks idempotentes | Com `task_acks_late=True` uma task pode rodar mais de uma vez |

---

## Disparando Tasks nos Endpoints

```python
from app.tasks.categories import process_after_create

@router.post("/", response_model=CategoryOut, status_code=201)
async def create(data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = Category(name=data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    process_after_create.delay(category.id)  # não bloqueia a resposta
    return category
```

`.delay(id)` serializa a task como mensagem JSON e a enfileira no Redis. A resposta HTTP é retornada imediatamente — o processamento acontece em background no worker.

---

## Variáveis de Ambiente

```bash
CELERY_BROKER_URL=redis://redis:6379/0      # DB 0 = fila de tasks
CELERY_RESULT_BACKEND=redis://redis:6379/1  # DB 1 = resultados
FLOWER_USER=admin
FLOWER_PASSWORD=admin
```

Redis DBs separados evitam colisão de chaves entre broker e result backend.

---

## Docker Compose

Todos os serviços (`app`, `worker`, `flower`) usam a mesma imagem — o `command` é sobrescrito em cada serviço:

```yaml
worker:
  build: .
  command: uv run celery -A app.worker.celery_app worker --loglevel=info --concurrency=2
  depends_on:
    redis:
      condition: service_healthy
    db:
      condition: service_healthy

flower:
  build: .
  command: >
    uv run celery -A app.worker.celery_app
    --broker=${CELERY_BROKER_URL}
    flower --port=5555
    --basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}
  profiles:
    - monitoring
```

O Flower usa `profiles: monitoring` — só sobe quando explicitamente solicitado, sem impactar o ambiente padrão.

---

## Comandos

```bash
make setup        # sobe tudo incluindo o worker
make worker       # sobe apenas o worker
make worker-logs  # acompanha os logs do worker em tempo real
make flower       # sobe o Flower em http://localhost:5555
```

---

## Adicionando Novas Tasks

1. Criar `app/tasks/novo_dominio.py` seguindo o padrão:

```python
from app.worker import celery_app
from app.database import AsyncSessionLocal

@celery_app.task(name="tasks.novo_dominio.minha_task")
def minha_task(entity_id: int):
    async def _run():
        async with AsyncSessionLocal() as session:
            # lógica aqui
            pass
    return asyncio.run(_run())
```

2. O `autodiscover_tasks(["app.tasks"])` em `worker.py` registra o módulo automaticamente — não é necessário nenhuma alteração no `worker.py`.
