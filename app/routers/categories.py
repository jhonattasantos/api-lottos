from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryIn, CategoryOut
from app.tasks.categories import process_after_create
from app.utils.slug import make_slug

router = APIRouter(prefix="/categories", tags=["categories"])

_WITH_RULES = select(Category).options(selectinload(Category.prize_rules))


@router.get("", response_model=list[CategoryOut])
async def index(db: AsyncSession = Depends(get_db)):
    result = await db.execute(_WITH_RULES)
    return result.scalars().all()


@router.get("/{id}", response_model=CategoryOut)
async def show(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(_WITH_RULES.where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryOut, status_code=201)
async def create(data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = Category(**data.model_dump(), slug=make_slug(data.name))
    db.add(category)
    await db.commit()
    result = await db.execute(_WITH_RULES.where(Category.id == category.id))
    category = result.scalar_one()
    process_after_create.delay(category.id)
    return category


@router.put("/{id}", response_model=CategoryOut)
async def update(id: int, data: CategoryIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(_WITH_RULES.where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in data.model_dump().items():
        setattr(category, key, value)
    category.slug = make_slug(data.name)
    await db.commit()
    result = await db.execute(_WITH_RULES.where(Category.id == id))
    return result.scalar_one()


@router.delete("/{id}", status_code=204)
async def destroy(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
