from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class UserType(str, Enum):
    """Tipos de usuario disponibles"""
    FAMILY = "family"
    EMPLOYEE = "employee"

class UserBase(BaseModel):
    """Esquema base para usuarios"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    user_type: UserType = Field(default=UserType.FAMILY, description="Tipo de usuario: family o employee")

class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    user_type: Optional[UserType] = None

class UserInDB(UserBase):
    """Esquema para usuario en base de datos"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    """Esquema para respuesta de usuario"""
    pass

class UserLogin(BaseModel):
    """Esquema para login de usuario"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Esquema para token de autenticación"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Esquema para datos del token"""
    email: Optional[str] = None 