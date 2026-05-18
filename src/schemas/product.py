from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    base_price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    base_price: Optional[float] = None
