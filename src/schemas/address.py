from pydantic import BaseModel, ConfigDict
from typing import Optional
    
class AddressBase(BaseModel):
    domicilio: str
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: Optional[str] = None


class AddressCreate(AddressBase):
    client_id: int # Link this address to a specific Client ID
    pass


class AddressRead(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
class AddressUpdate(BaseModel):
    domicilio: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: Optional[str] = None