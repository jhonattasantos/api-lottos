import asyncio

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.category import Category
from app.worker import celery_app


def run_async(coro):
    return asyncio.run(coro)


@celery_app.task(
    name="tasks.categories.process_after_create",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def process_after_create(self, category_id: int):
    async def _run():
        async with AsyncSessionLocal() as session:
            category = await session.get(Category, category_id)
            if not category:
                return {"status": "not_found", "id": category_id}
            # Exemplo: lógica pós-criação (notificação, cache, etc.)
            return {"status": "processed", "id": category_id, "name": category.name}

    try:
        return run_async(_run())
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(name="tasks.categories.rebuild_cache")
def rebuild_cache():
    async def _run():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Category))
            categories = result.scalars().all()
            return {"status": "ok", "count": len(categories)}

    return run_async(_run())
