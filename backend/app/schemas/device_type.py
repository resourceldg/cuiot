from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Device type name")
    description: Optional[str] = Field(None, max_length=255, description="Device type description")
    category: Optional[str] = Field(None, max_length=50, description="Device category")
    icon_name: Optional[str] = Field(None, max_length=50, description="Icon name for UI")
    color_code: Optional[str] = Field(None, max_length=7, description="Hex color code for UI")
    is_active: bool = Field(True, description="Whether the device type is active")

class DeviceTypeCreate(DeviceTypeBase):
    pass

class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    icon_name: Optional[str] = Field(None, max_length=50)
    color_code: Optional[str] = Field(None, max_length=7)
    is_active: Optional[bool] = None

class DeviceType(DeviceTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 