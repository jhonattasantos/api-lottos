from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category, PrizeRule
from app.utils.slug import make_slug

LOTERIAS = [
    {
        "name": "Mega-Sena",
        "min_number": 1,
        "max_number": 60,
        "picks": 6,
        "draws": 6,
        "prize_rules": [
            {"label": "Sena", "hits": 6},
            {"label": "Quina", "hits": 5},
            {"label": "Quadra", "hits": 4},
        ],
    },
    {
        "name": "Quina",
        "min_number": 1,
        "max_number": 80,
        "picks": 5,
        "draws": 5,
        "prize_rules": [
            {"label": "Quina", "hits": 5},
            {"label": "Quadra", "hits": 4},
            {"label": "Terno", "hits": 3},
            {"label": "Duque", "hits": 2},
        ],
    },
    {
        "name": "Lotofácil",
        "min_number": 1,
        "max_number": 25,
        "picks": 15,
        "draws": 15,
        "prize_rules": [
            {"label": "15 acertos", "hits": 15},
            {"label": "14 acertos", "hits": 14},
            {"label": "13 acertos", "hits": 13},
            {"label": "12 acertos", "hits": 12},
            {"label": "11 acertos", "hits": 11},
        ],
    },
    {
        "name": "Lotomania",
        "min_number": 0,
        "max_number": 99,
        "picks": 50,
        "draws": 20,
        "prize_rules": [
            {"label": "20 acertos", "hits": 20},
            {"label": "19 acertos", "hits": 19},
            {"label": "18 acertos", "hits": 18},
            {"label": "17 acertos", "hits": 17},
            {"label": "16 acertos", "hits": 16},
            {"label": "15 acertos", "hits": 15},
            {"label": "0 acertos", "hits": 0},
        ],
    },
    {
        "name": "Dupla Sena",
        "min_number": 1,
        "max_number": 50,
        "picks": 6,
        "draws": 6,
        "prize_rules": [
            {"label": "Sena", "hits": 6},
            {"label": "Quina", "hits": 5},
            {"label": "Quadra", "hits": 4},
        ],
    },
    {
        "name": "Dia de Sorte",
        "min_number": 1,
        "max_number": 31,
        "picks": 7,
        "draws": 7,
        "prize_rules": [
            {"label": "7 acertos", "hits": 7},
            {"label": "6 acertos", "hits": 6},
            {"label": "5 acertos", "hits": 5},
            {"label": "4 acertos", "hits": 4},
        ],
    },
    {
        "name": "Super Sete",
        "min_number": 0,
        "max_number": 9,
        "picks": 7,
        "draws": 7,
        "prize_rules": [
            {"label": "7 colunas", "hits": 7},
            {"label": "6 colunas", "hits": 6},
            {"label": "5 colunas", "hits": 5},
            {"label": "4 colunas", "hits": 4},
            {"label": "3 colunas", "hits": 3},
        ],
    },
    {
        "name": "Timemania",
        "min_number": 1,
        "max_number": 80,
        "picks": 10,
        "draws": 7,
        "prize_rules": [
            {"label": "7 acertos", "hits": 7},
            {"label": "6 acertos", "hits": 6},
            {"label": "5 acertos", "hits": 5},
            {"label": "4 acertos", "hits": 4},
            {"label": "3 acertos", "hits": 3},
        ],
    },
    {
        "name": "+Milionária",
        "min_number": 1,
        "max_number": 50,
        "picks": 6,
        "draws": 6,
        "prize_rules": [
            {"label": "6 acertos", "hits": 6},
            {"label": "5 acertos", "hits": 5},
            {"label": "4 acertos", "hits": 4},
            {"label": "3 acertos", "hits": 3},
            {"label": "2 acertos", "hits": 2},
        ],
    },
    {
        "name": "Loteca",
        "min_number": 1,
        "max_number": 14,
        "picks": 14,
        "draws": 14,
        "prize_rules": [
            {"label": "14 acertos", "hits": 14},
            {"label": "13 acertos", "hits": 13},
            {"label": "0 acertos", "hits": 0},
        ],
    },
]


async def seed(session: AsyncSession) -> None:
    count_new = 0
    count_updated = 0

    for data in LOTERIAS:
        slug = make_slug(data["name"])
        result = await session.execute(
            select(Category).where(Category.slug == slug)
        )
        category = result.scalar_one_or_none()

        if category is None:
            category = Category(
                name=data["name"],
                slug=slug,
                min_number=data["min_number"],
                max_number=data["max_number"],
                picks=data["picks"],
                draws=data["draws"],
            )
            session.add(category)
            await session.flush()
            count_new += 1
        else:
            category.slug = slug
            category.min_number = data["min_number"]
            category.max_number = data["max_number"]
            category.picks = data["picks"]
            category.draws = data["draws"]
            category.prize_rules = []
            await session.flush()
            count_updated += 1

        for rule in data["prize_rules"]:
            session.add(PrizeRule(
                category_id=category.id,
                label=rule["label"],
                hits=rule["hits"],
            ))

    total_rules = sum(len(d["prize_rules"]) for d in LOTERIAS)
    print(f"  -> categories: {count_new} inseridas, {count_updated} atualizadas")
    print(f"  -> prize_rules: {total_rules} registros ok")
