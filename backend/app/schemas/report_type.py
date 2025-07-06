from pydantic import BaseModel, Field
from typing import Optional

class ReportTypeBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = True

class ReportTypeCreate(ReportTypeBase):
    pass

class ReportTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class ReportTypeResponse(ReportTypeBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True 