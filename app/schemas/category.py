from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
