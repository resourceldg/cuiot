from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from uuid import UUID
from .base import BaseResponse, BaseCreate, BaseUpdate

class ServiceSubscriptionBase(BaseModel):
    service_type_id: int = Field(..., description="ID del tipo de servicio normalizado")
    service_name: str = Field(..., max_length=100)
    description: Optional[str] = None
    features: Optional[str] = None  # JSON string
    limitations: Optional[str] = None  # JSON string
    price_per_month: Optional[int] = Field(None, ge=0)  # Price in cents
    price_per_year: Optional[int] = Field(None, ge=0)  # Price in cents
    currency: str = Field(default="USD", max_length=3)
    start_date: date
    end_date: Optional[date] = None
    auto_renew: bool = True
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")
    user_id: Optional[UUID] = None
    institution_id: Optional[int] = None

class ServiceSubscriptionCreate(ServiceSubscriptionBase, BaseCreate):
    pass

class ServiceSubscriptionUpdate(ServiceSubscriptionBase, BaseUpdate):
    service_type_id: Optional[int] = Field(None, description="ID del tipo de servicio normalizado")
    service_name: Optional[str] = Field(None, max_length=100)
    price_per_month: Optional[int] = Field(None, ge=0)
    price_per_year: Optional[int] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    start_date: Optional[date] = None
    auto_renew: Optional[bool] = None
    status_type_id: Optional[int] = Field(None, description="ID del tipo de status normalizado")

class ServiceSubscriptionResponse(ServiceSubscriptionBase, BaseResponse):
    is_active: bool

class ServiceSubscriptionInDB(ServiceSubscriptionBase, BaseResponse):
    pass 