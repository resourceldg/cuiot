from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseResponse, BaseCreate, BaseUpdate

class InstitutionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    institution_type: str = Field(..., max_length=50)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=200)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tax_id: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=50)
    capacity: Optional[int] = Field(None, ge=0)
    is_verified: bool = False

class InstitutionCreate(InstitutionBase, BaseCreate):
    pass

class InstitutionUpdate(InstitutionBase, BaseUpdate):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    institution_type: Optional[str] = Field(None, max_length=50)
    is_verified: Optional[bool] = None

class InstitutionResponse(InstitutionBase, BaseResponse):
    pass

class InstitutionInDB(InstitutionBase, BaseResponse):
    pass
