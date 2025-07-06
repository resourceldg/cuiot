from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class ReminderBase(BaseModel):
    reminder_type_id: int = Field(..., description="ID del tipo de recordatorio normalizado")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_time: datetime
    due_date: Optional[date] = None
    repeat_pattern: Optional[str] = Field(None, max_length=100)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")
    completed_at: Optional[datetime] = None
    completed_by: Optional[UUID] = None
    priority: int = Field(default=5, ge=1, le=10)
    is_important: bool = False
    reminder_data: Optional[str] = None  # JSON string
    notes: Optional[str] = None
    user_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None

class ReminderCreate(ReminderBase, BaseCreate):
    pass

class ReminderUpdate(ReminderBase, BaseUpdate):
    reminder_type_id: Optional[int] = Field(None, description="ID del tipo de recordatorio normalizado")
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    scheduled_time: Optional[datetime] = None
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")
    priority: Optional[int] = Field(None, ge=1, le=10)
    is_important: Optional[bool] = None

class ReminderResponse(ReminderBase, BaseResponse):
    is_overdue: bool
    is_completed: bool

class ReminderInDB(ReminderBase, BaseResponse):
    pass
