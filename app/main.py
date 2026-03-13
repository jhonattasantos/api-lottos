from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.routers import health, categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify DB connection on startup
    async with engine.connect() as conn:
        await conn.close()
    yield
    await engine.dispose()


app = FastAPI(title="API Lottos", lifespan=lifespan)

app.include_router(health.router)
app.include_router(categories.router)
