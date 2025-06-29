from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)

class BaseResponse(BaseSchema):
    """Base response schema with common fields"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

class BaseCreate(BaseSchema):
    """Base create schema"""
    pass

class BaseUpdate(BaseSchema):
    """Base update schema"""
    is_active: Optional[bool] = None
