
from pydantic import BaseModel, Field


class ProductUpdate(BaseModel):
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class ProductCreate(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
