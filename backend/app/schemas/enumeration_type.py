from typing import Optional
from pydantic import BaseModel, UUID4

class EnumerationTypeBase(BaseModel):
    type_name: str
    description: Optional[str] = None
    is_system: bool = False

class EnumerationTypeCreate(EnumerationTypeBase):
    pass

class EnumerationTypeUpdate(BaseModel):
    type_name: Optional[str] = None
    description: Optional[str] = None
    is_system: Optional[bool] = None

class EnumerationType(EnumerationTypeBase):
    id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
