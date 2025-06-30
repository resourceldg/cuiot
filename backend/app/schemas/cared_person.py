from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class CaredPersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    identification_number: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    emergency_contact: Optional[str] = Field(None, max_length=100)
    emergency_phone: Optional[str] = Field(None, max_length=20)
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None
    blood_type: Optional[str] = Field(None, max_length=10)
    care_level: Optional[str] = Field(None, max_length=50)
    special_needs: Optional[str] = None
    mobility_level: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    user_id: Optional[UUID] = None
    institution_id: Optional[UUID] = None
    medical_contact_name: Optional[str] = Field(None, max_length=100)
    medical_contact_phone: Optional[str] = Field(None, max_length=20)
    family_contact_name: Optional[str] = Field(None, max_length=100)
    family_contact_phone: Optional[str] = Field(None, max_length=20)
    medical_notes: Optional[str] = None

class CaredPersonCreate(CaredPersonBase, BaseCreate):
    pass

class CaredPersonUpdate(CaredPersonBase, BaseUpdate):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)

class CaredPersonResponse(CaredPersonBase, BaseResponse):
    age: Optional[int] = None
    full_name: str

class CaredPersonInDB(CaredPersonBase, BaseResponse):
    pass
