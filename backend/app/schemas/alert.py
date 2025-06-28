from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class AlertType(str, Enum):
    """Tipos de alertas disponibles"""
    NO_MOVEMENT = "no_movement"
    SOS = "sos"
    TEMPERATURE = "temperature"
    MEDICATION = "medication"
    FALL = "fall"
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE = "blood_pressure"

class AlertSeverity(str, Enum):
    """Niveles de severidad de alertas"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertBase(BaseModel):
    """Schema base para alertas"""
    elderly_person_id: UUID = Field(..., description="ID del adulto mayor")
    alert_type: AlertType = Field(..., description="Tipo de alerta")
    message: str = Field(..., min_length=1, max_length=1000, description="Mensaje descriptivo de la alerta")
    severity: AlertSeverity = Field(default=AlertSeverity.MEDIUM, description="Nivel de severidad")

class AlertCreate(AlertBase):
    """Schema para crear una nueva alerta"""
    created_by_id: UUID = Field(..., description="ID del usuario que crea la alerta")
    received_by_id: Optional[UUID] = Field(None, description="ID del usuario que recibe la alerta")

class AlertUpdate(BaseModel):
    """Schema para actualizar una alerta"""
    message: Optional[str] = Field(None, min_length=1, max_length=1000)
    severity: Optional[AlertSeverity] = None
    received_by_id: Optional[UUID] = None
    is_resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None

class AlertResponse(AlertBase):
    """Schema para respuesta de alerta"""
    id: UUID
    created_by_id: UUID
    received_by_id: Optional[UUID] = None
    is_resolved: bool
    resolved_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AlertListResponse(BaseModel):
    """Schema para lista de alertas"""
    alerts: list[AlertResponse]
    total: int
    skip: int
    limit: int 