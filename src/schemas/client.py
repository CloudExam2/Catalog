
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ClientBase(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13)
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