from typing import Optional
from pydantic import BaseModel, UUID4

class EnumerationValueBase(BaseModel):
    value_name: str
    description: Optional[str] = None
    sort_order: int
    is_default: bool = False

class EnumerationValueCreate(EnumerationValueBase):
    enumeration_type_id: UUID4

class EnumerationValueUpdate(BaseModel):
    value_name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_default: Optional[bool] = None

class EnumerationValue(EnumerationValueBase):
    id: UUID4
    enumeration_type_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
