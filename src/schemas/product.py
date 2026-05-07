from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    base_price: float

class ProductCreate(ProductBase):
    # This is the link to the Client (Seller)
    client_id: int 

class ProductRead(ProductBase):
    id: int
    client_id: int # Show who owns it when reading
    model_config = ConfigDict(from_attributes=True)
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    base_price: Optional[float] = None