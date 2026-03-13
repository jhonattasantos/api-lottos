import asyncio

from app.database import AsyncSessionLocal
from seeds import categories


async def run() -> None:
    print("Rodando seeds...")
    async with AsyncSessionLocal() as session:
        await categories.seed(session)
        await session.commit()
    print("Seeds aplicados com sucesso.")


asyncio.run(run())
