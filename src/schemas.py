
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ClientBase(BaseModel):
    rfc: str
    razon_social: str
    email: str
    comercial_name: Optional[str] = None
    telefono: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class ClientUpdate(BaseModel):
    # Every field is now optional with a default of None
    rfc: Optional[str] = None
    razon_social: Optional[str] = None
    email: Optional[str] = None
    comercial_name: Optional[str] = None
    telefono: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    base_price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AddressBase(BaseModel):
    domicilio: str
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)