# Endpoints: Categories

## Estrutura

```
app/
├── schemas/
│   └── category.py          # Schemas de entrada e saída
└── routers/
    └── categories.py        # Endpoints CRUD
```

---

## Schemas (`app/schemas/category.py`)

```python
class CategoryIn(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
```

- `CategoryIn` — payload de entrada (POST e PUT)
- `CategoryOut` — payload de saída. `from_attributes=True` permite serializar diretamente a partir do model SQLAlchemy

---

## Endpoints

| Método | Rota | Função | Status |
|---|---|---|---|
| GET | `/categories` | `index` | 200 |
| GET | `/categories/{id}` | `show` | 200 / 404 |
| POST | `/categories` | `create` | 201 |
| PUT | `/categories/{id}` | `update` | 200 / 404 |
| DELETE | `/categories/{id}` | `destroy` | 204 / 404 |

Os nomes das funções seguem a convenção do Rails (`index`, `show`, `create`, `update`, `destroy`).

---

## Implementação

### index — lista todas

```python
@router.get("", response_model=list[CategoryOut])
async def index(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()
```

### show — busca uma por id

```python
@router.get("/{id}", response_model=CategoryOut)
async def show(id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
```

`db.get()` busca por PK diretamente, sem precisar de `select`.

### create — cria

```python
@router.post("", response_model=CategoryOut, status_code=201)
async def create(data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = Category(name=data.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
```

`db.refresh()` recarrega o objeto após o commit para obter o `id` gerado pelo banco.

### update — atualiza

```python
@router.put("/{id}", response_model=CategoryOut)
async def update(id: int, data: CategoryIn, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = data.name
    await db.commit()
    await db.refresh(category)
    return category
```

### destroy — remove

```python
@router.delete("/{id}", status_code=204)
async def destroy(id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
```

204 não retorna body.

---

## Registro no `main.py`

```python
from app.routers import health, categories

app.include_router(health.router)
app.include_router(categories.router)
```

O router é criado com `prefix="/categories"` e `tags=["categories"]`, o que agrupa os endpoints no Swagger UI automaticamente. As rotas de coleção usam path vazio (`""`) em vez de `"/"` para evitar o redirect 307 do FastAPI ao omitir a barra final.
