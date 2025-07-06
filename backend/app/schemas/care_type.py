from pydantic import BaseModel, Field
from typing import Optional

class CareTypeBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = True

class CareTypeCreate(CareTypeBase):
    pass

class CareTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class CareTypeResponse(CareTypeBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True 