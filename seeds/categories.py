from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category

LOTERIAS = [
    "Mega-Sena",
    "Quina",
    "Lotofácil",
    "Lotomania",
    "Timemania",
    "Dupla Sena",
    "Loteca",
    "Dia de Sorte",
    "+Milionária",
    "Super Sete",
]


async def seed(session: AsyncSession) -> None:
    for name in LOTERIAS:
        session.add(Category(name=name))
    print(f"  -> categories: {len(LOTERIAS)} registros ok")
