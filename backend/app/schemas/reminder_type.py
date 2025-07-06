from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReminderTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Unique name for the reminder type")
    description: Optional[str] = Field(None, max_length=255, description="Description of the reminder type")
    category: Optional[str] = Field(None, max_length=50, description="Category of the reminder type")
    icon_name: Optional[str] = Field(None, max_length=50, description="Icon name for UI display")
    color_code: Optional[str] = Field(None, max_length=7, description="Color code for UI display")
    is_active: bool = Field(True, description="Whether the reminder type is active")

class ReminderTypeCreate(ReminderTypeBase):
    pass

class ReminderTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    icon_name: Optional[str] = Field(None, max_length=50)
    color_code: Optional[str] = Field(None, max_length=7)
    is_active: Optional[bool] = None

class ReminderType(ReminderTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 