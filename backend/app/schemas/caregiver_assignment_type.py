from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CaregiverAssignmentTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nombre único del tipo de asignación")
    description: Optional[str] = Field(None, max_length=255, description="Descripción del tipo de asignación")
    category: Optional[str] = Field(None, max_length=50, description="Categoría del tipo de asignación")
    is_active: bool = Field(True, description="Si el tipo está activo")

class CaregiverAssignmentTypeCreate(CaregiverAssignmentTypeBase):
    pass

class CaregiverAssignmentTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

class CaregiverAssignmentType(CaregiverAssignmentTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 