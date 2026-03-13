from pydantic import BaseModel


class PrizeRuleOut(BaseModel):
    id: int
    label: str
    hits: int

    model_config = {"from_attributes": True}


class CategoryIn(BaseModel):
    name: str
    min_number: int
    max_number: int
    picks: int
    draws: int


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    min_number: int
    max_number: int
    picks: int
    draws: int
    prize_rules: list[PrizeRuleOut] = []

    model_config = {"from_attributes": True}
