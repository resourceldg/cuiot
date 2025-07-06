from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class AlertBase(BaseModel):
    alert_type_id: int = Field(..., description="ID del tipo de alerta")
    alert_subtype: Optional[str] = Field(None, max_length=50)
    severity: str = Field(default="medium", max_length=20)
    title: str = Field(..., min_length=1, max_length=200)
    message: Optional[str] = None
    alert_data: Optional[str] = None  # JSON string
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    priority: int = Field(default=5, ge=1, le=10)
    escalation_level: int = Field(default=0, ge=0, le=5)
    user_id: Optional[UUID] = None
    cared_person_id: Optional[UUID] = None
    device_id: Optional[UUID] = None
    event_id: Optional[UUID] = None

class AlertCreate(AlertBase, BaseCreate):
    pass

class AlertUpdate(AlertBase, BaseUpdate):
    alert_type_id: Optional[int] = Field(None, description="ID del tipo de alerta")
    alert_subtype: Optional[str] = Field(None, max_length=50)
    severity: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    priority: Optional[int] = Field(None, ge=1, le=10)
    escalation_level: Optional[int] = Field(None, ge=0, le=5)

class AlertResponse(AlertBase, BaseResponse):
    is_active: bool
    is_critical: bool

class AlertInDB(AlertBase, BaseResponse):
    pass
