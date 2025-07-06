from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StatusTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nombre del estado")
    description: Optional[str] = Field(None, description="Descripción del estado")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría del estado")
    is_active: bool = Field(True, description="Indica si el estado está activo")


class StatusTypeCreate(StatusTypeBase):
    pass


class StatusTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class StatusType(StatusTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 