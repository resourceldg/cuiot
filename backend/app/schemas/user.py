from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from .base import BaseResponse, BaseCreate, BaseUpdate

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = Field(None, max_length=20)
    professional_license: Optional[str] = Field(None, max_length=50)
    specialization: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0)
    is_freelance: bool = False
    hourly_rate: Optional[int] = Field(None, ge=0)  # Rate in cents
    availability: Optional[str] = None  # JSON string
    is_verified: bool = False
    institution_id: Optional[int] = None

class UserCreate(UserBase, BaseCreate):
    password: str = Field(..., min_length=8)

class UserUpdate(UserBase, BaseUpdate):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase, BaseResponse):
    last_login: Optional[datetime] = None

class UserInDB(UserBase, BaseResponse):
    password_hash: str
    last_login: Optional[datetime] = None

class UserPackageResponse(BaseModel):
    id: str
    package_id: str
    package_name: str
    status_type_id: Optional[int] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True

class UserWithRoles(UserResponse):
    roles: List[str] = []  # List of role names
    package_subscriptions: List[UserPackageResponse] = []  # List of user packages
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
