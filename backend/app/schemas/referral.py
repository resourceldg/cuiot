from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ReferralBase(BaseModel):
    """Base schema for referrals"""
    referral_type_id: int = Field(..., description="ID del tipo de derivación normalizado")
    referral_code: str = Field(..., description="Unique referral code")
    referrer_type: str = Field(..., description="Type of referrer: caregiver, institution, family, cared_person")
    referrer_id: UUID = Field(..., description="ID of the referrer")
    referred_email: EmailStr = Field(..., description="Email of the referred person")
    referred_name: Optional[str] = Field(None, description="Name of the referred person")
    referred_phone: Optional[str] = Field(None, description="Phone of the referred person")
    source: Optional[str] = Field(None, description="Source of referral: email, whatsapp, phone, in_person")
    notes: Optional[str] = Field(None, description="Additional notes about the referral")
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado normalizado")

class ReferralCreate(ReferralBase):
    """Schema for creating a new referral"""
    pass

class ReferralUpdate(BaseModel):
    """Schema for updating a referral"""
    referral_type_id: Optional[int] = Field(None, description="ID del tipo de derivación normalizado")
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    notes: Optional[str] = Field(None, description="Additional notes")
    commission_amount: Optional[float] = Field(None, description="Commission amount when converted")

class ReferralInDB(ReferralBase):
    """Schema for referral in database"""
    id: UUID
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    registered_at: Optional[datetime] = None
    converted_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    commission_amount: Optional[float] = None
    commission_paid: bool = False
    commission_paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReferralResponse(ReferralInDB):
    """Schema for referral response"""
    days_since_created: int = Field(..., description="Days since referral was created")
    is_expirable: bool = Field(..., description="Whether referral can expire")
    total_commissions: float = Field(0.0, description="Total commissions generated")

class ReferralCommissionBase(BaseModel):
    """Base schema for referral commissions"""
    referral_id: UUID = Field(..., description="ID of the referral")
    recipient_type: str = Field(..., description="Type of recipient: caregiver, institution, family")
    recipient_id: UUID = Field(..., description="ID of the recipient")
    amount: float = Field(..., description="Commission amount")
    commission_type: str = Field(..., description="Type: first_month, recurring, bonus")
    percentage: float = Field(..., description="Commission percentage")

class ReferralCommissionCreate(ReferralCommissionBase):
    """Schema for creating a new commission"""
    pass

class ReferralCommissionUpdate(BaseModel):
    """Schema for updating a commission"""
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")

class ReferralCommissionInDB(ReferralCommissionBase):
    """Schema for commission in database"""
    id: UUID
    status_type_id: Optional[int] = Field(None, description="ID del tipo de estado")
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReferralCommissionResponse(ReferralCommissionInDB):
    """Schema for commission response"""
    pass

class ReferralStats(BaseModel):
    """Schema for referral statistics"""
    total_referrals: int = Field(..., description="Total referrals created")
    pending_referrals: int = Field(..., description="Pending referrals")
    registered_referrals: int = Field(..., description="Registered referrals")
    converted_referrals: int = Field(..., description="Converted referrals")
    expired_referrals: int = Field(..., description="Expired referrals")
    conversion_rate: float = Field(..., description="Conversion rate percentage")
    total_commissions_paid: float = Field(..., description="Total commissions paid")
    total_commissions_pending: float = Field(..., description="Total commissions pending")
    avg_commission_amount: float = Field(..., description="Average commission amount")

class ReferralSummary(BaseModel):
    """Schema for referral summary"""
    referral: ReferralResponse
    commissions: List[ReferralCommissionResponse] = Field(default_factory=list)
    stats: ReferralStats

class ReferralCodeGenerate(BaseModel):
    """Schema for generating referral codes"""
    referrer_type: str = Field(..., description="Type of referrer")
    referrer_id: UUID = Field(..., description="ID of the referrer")
    custom_code: Optional[str] = Field(None, description="Custom referral code (optional)")

class ReferralCodeResponse(BaseModel):
    """Schema for referral code response"""
    referral_code: str = Field(..., description="Generated referral code")
    referrer_type: str = Field(..., description="Type of referrer")
    referrer_id: UUID = Field(..., description="ID of the referrer")
    commission_rates: dict = Field(..., description="Commission rates for this referrer type")
    expiry_days: int = Field(30, description="Days until referral expires")
    usage_count: int = Field(0, description="Number of times this code has been used")
    total_earnings: float = Field(0.0, description="Total earnings from this code")

class ReferralValidation(BaseModel):
    """Schema for validating referral codes"""
    referral_code: str = Field(..., description="Referral code to validate")
    referred_email: EmailStr = Field(..., description="Email of the person being referred")

class ReferralValidationResponse(BaseModel):
    """Schema for referral validation response"""
    is_valid: bool = Field(..., description="Whether the referral code is valid")
    referrer_name: Optional[str] = Field(None, description="Name of the referrer")
    referrer_type: Optional[str] = Field(None, description="Type of referrer")
    commission_info: Optional[dict] = Field(None, description="Commission information")
    error_message: Optional[str] = Field(None, description="Error message if invalid") 