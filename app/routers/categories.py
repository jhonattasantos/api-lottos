from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryIn, CategoryOut
from app.tasks.categories import process_after_create

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
async def index(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()


@router.get("/{id}", response_model=CategoryOut)
async def show(id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryOut, status_code=201)
async def create(data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = Category(name=data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    process_after_create.delay(category.id)
    return category


@router.put("/{id}", response_model=CategoryOut)
async def update(id: int, data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = data.name
    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/{id}", status_code=204)
async def destroy(id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
