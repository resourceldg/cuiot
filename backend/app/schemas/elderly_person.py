from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class EmergencyContact(BaseModel):
    """Esquema para contacto de emergencia"""
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=20)
    relationship: str = Field(..., min_length=1, max_length=50)

class MedicalCondition(BaseModel):
    condition: str = Field(..., min_length=1, max_length=100)
    severity: str = Field(..., min_length=1, max_length=50)
    medication: Optional[str] = None

class Medication(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    dosage: str = Field(..., min_length=1, max_length=50)
    frequency: str = Field(..., min_length=1, max_length=50)
    time: str = Field(..., min_length=1, max_length=50)

class ElderlyPersonBase(BaseModel):
    """Esquema base para adultos mayores"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    address: Optional[str] = None
    emergency_contacts: Optional[List[EmergencyContact]] = []
    medical_conditions: Optional[List[MedicalCondition]] = []
    medications: Optional[List[Medication]] = []

class ElderlyPersonCreate(ElderlyPersonBase):
    """Esquema para crear adulto mayor"""
    user_id: Optional[UUID] = None  # Se asignará automáticamente desde el token JWT

class ElderlyPersonUpdate(BaseModel):
    """Esquema para actualizar adulto mayor"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    address: Optional[str] = None
    emergency_contacts: Optional[List[EmergencyContact]] = None
    medical_conditions: Optional[List[MedicalCondition]] = None
    medications: Optional[List[Medication]] = None
    is_active: Optional[bool] = None

class ElderlyPersonInDB(ElderlyPersonBase):
    """Esquema para adulto mayor en base de datos"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_deleted: bool = False

    class Config:
        from_attributes = True

class ElderlyPerson(ElderlyPersonInDB):
    """Esquema para respuesta de adulto mayor"""
    pass

class ElderlyPersonWithDevices(ElderlyPerson):
    """Esquema para adulto mayor con dispositivos"""
    devices: List[Dict[str, Any]] = [] 