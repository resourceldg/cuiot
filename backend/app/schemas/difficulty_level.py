from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DifficultyLevelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Difficulty level name")
    description: Optional[str] = Field(None, max_length=255, description="Difficulty level description")
    color_code: Optional[str] = Field(None, max_length=7, description="Hex color code for UI")
    is_active: bool = Field(True, description="Whether the difficulty level is active")

class DifficultyLevelCreate(DifficultyLevelBase):
    pass

class DifficultyLevelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    color_code: Optional[str] = Field(None, max_length=7)
    is_active: Optional[bool] = None

class DifficultyLevel(DifficultyLevelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 