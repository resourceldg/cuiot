from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, time
from uuid import UUID
from enum import Enum

class ReminderType(str, Enum):
    """Tipos de recordatorios disponibles"""
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    ACTIVITY = "activity"
    MEAL = "meal"
    EXERCISE = "exercise"
    HYDRATION = "hydration"

class ReminderBase(BaseModel):
    """Schema base para recordatorios"""
    elderly_person_id: UUID = Field(..., description="ID del adulto mayor")
    title: str = Field(..., min_length=1, max_length=200, description="Título del recordatorio")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción opcional")
    reminder_type: ReminderType = Field(..., description="Tipo de recordatorio")
    scheduled_time: time = Field(..., description="Hora programada para el recordatorio")
    days_of_week: Optional[List[int]] = Field(None, description="Días de la semana (1-7, donde 1=Lunes)")

    @validator('days_of_week')
    def validate_days_of_week(cls, v):
        if v is not None:
            for day in v:
                if not 1 <= day <= 7:
                    raise ValueError('Los días de la semana deben estar entre 1 y 7')
        return v

class ReminderCreate(ReminderBase):
    """Schema para crear un nuevo recordatorio"""
    created_by_id: UUID = Field(..., description="ID del usuario que crea el recordatorio")
    received_by_id: Optional[UUID] = Field(None, description="ID del usuario que recibe el recordatorio")

class ReminderUpdate(BaseModel):
    """Schema para actualizar un recordatorio"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    reminder_type: Optional[ReminderType] = None
    scheduled_time: Optional[time] = None
    received_by_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    days_of_week: Optional[List[int]] = None

    @validator('days_of_week')
    def validate_days_of_week(cls, v):
        if v is not None:
            for day in v:
                if not 1 <= day <= 7:
                    raise ValueError('Los días de la semana deben estar entre 1 y 7')
        return v

class ReminderResponse(ReminderBase):
    """Schema para respuesta de recordatorio"""
    id: UUID
    created_by_id: UUID
    received_by_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReminderListResponse(BaseModel):
    """Schema para lista de recordatorios"""
    reminders: list[ReminderResponse]
    total: int
    skip: int
    limit: int 