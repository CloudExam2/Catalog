from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddressType(str, Enum):
    FACTURACION = "FACTURACIÓN"
    ENVIO = "ENVÍO"


class AddressBase(BaseModel):
    domicilio: str
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: AddressType


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    domicilio: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    address_type: Optional[AddressType] = None
