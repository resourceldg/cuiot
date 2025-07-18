from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, date
from uuid import UUID

class PackageBase(BaseModel):
    """Base schema for package"""
    package_type: str = Field(..., description="Type of package: individual, professional, institutional")
    name: str = Field(..., min_length=1, max_length=100, description="Package name")
    description: Optional[str] = Field(None, description="Package description")
    price_monthly: int = Field(..., ge=0, description="Monthly price in cents (ARS)")
    price_yearly: Optional[int] = Field(None, ge=0, description="Yearly price in cents (ARS)")
    currency: str = Field(default="ARS", max_length=3, description="Currency code")
    max_users: Optional[int] = Field(None, ge=1, description="Maximum number of users (None for unlimited)")
    max_devices: Optional[int] = Field(None, ge=1, description="Maximum number of devices (None for unlimited)")
    max_storage_gb: Optional[int] = Field(None, ge=1, description="Storage limit in GB")
    features: Optional[Dict[str, Any]] = Field(None, description="JSON with feature list")
    limitations: Optional[Dict[str, Any]] = Field(None, description="JSON with limitations")
    customizable_options: Optional[Dict[str, Any]] = Field(None, description="JSON with customization options")
    add_ons_available: Optional[Dict[str, Any]] = Field(None, description="JSON with available add-ons")
    base_configuration: Optional[Dict[str, Any]] = Field(None, description="JSON with base configuration")
    is_customizable: bool = Field(default=True, description="Whether package can be customized")
    support_level: Optional[str] = Field(None, description="Support level: basic, standard, premium, enterprise")
    response_time_hours: Optional[int] = Field(None, ge=1, description="Support response time in hours")
    is_featured: bool = Field(default=False, description="Whether package is featured")

    @field_validator('package_type')
    def validate_package_type(cls, v):
        valid_types = ["individual", "professional", "institutional"]
        if v not in valid_types:
            raise ValueError(f"Package type must be one of: {valid_types}")
        return v

    @field_validator('support_level')
    def validate_support_level(cls, v):
        if v is not None:
            valid_levels = ["basic", "standard", "premium", "enterprise"]
            if v not in valid_levels:
                raise ValueError(f"Support level must be one of: {valid_levels}")
        return v

    @field_validator('currency')
    def validate_currency(cls, v):
        if v != "ARS":
            raise ValueError("Currently only ARS currency is supported")
        return v


class PackageCreate(PackageBase):
    """Schema for creating a package"""
    pass


class PackageUpdate(BaseModel):
    """Schema for updating a package"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price_monthly: Optional[int] = Field(None, ge=0)
    price_yearly: Optional[int] = Field(None, ge=0)
    max_users: Optional[int] = Field(None, ge=1)
    max_devices: Optional[int] = Field(None, ge=1)
    max_storage_gb: Optional[int] = Field(None, ge=1)
    features: Optional[Dict[str, Any]] = None
    limitations: Optional[Dict[str, Any]] = None
    customizable_options: Optional[Dict[str, Any]] = None
    add_ons_available: Optional[Dict[str, Any]] = None
    base_configuration: Optional[Dict[str, Any]] = None
    is_customizable: Optional[bool] = None
    support_level: Optional[str] = None
    response_time_hours: Optional[int] = Field(None, ge=1)
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

    @field_validator('support_level')
    def validate_support_level(cls, v):
        if v is not None:
            valid_levels = ["basic", "standard", "premium", "enterprise"]
            if v not in valid_levels:
                raise ValueError(f"Support level must be one of: {valid_levels}")
        return v


class PackageResponse(PackageBase):
    """Schema for package response"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PackageAddOnBase(BaseModel):
    """Base schema for package add-on"""
    name: str = Field(..., min_length=1, max_length=100, description="Add-on name")
    description: Optional[str] = Field(None, description="Add-on description")
    add_on_type: str = Field(..., description="Type of add-on: storage, users, devices, features, support, analytics, integration")
    price_monthly: int = Field(..., ge=0, description="Monthly price in cents (ARS)")
    price_yearly: Optional[int] = Field(None, ge=0, description="Yearly price in cents (ARS)")
    configuration: Optional[Dict[str, Any]] = Field(None, description="JSON with add-on configuration")
    limitations: Optional[Dict[str, Any]] = Field(None, description="JSON with limitations")
    compatible_packages: Optional[List[str]] = Field(None, description="Lista de tipos de paquetes compatibles")
    max_quantity: Optional[int] = Field(None, ge=1, description="Maximum quantity allowed")

    @field_validator('add_on_type')
    def validate_add_on_type(cls, v):
        valid_types = ["storage", "users", "devices", "features", "support", "analytics", "integration"]
        if v not in valid_types:
            raise ValueError(f"Add-on type must be one of: {valid_types}")
        return v


class PackageAddOnCreate(PackageAddOnBase):
    """Schema for creating a package add-on"""
    pass


class PackageAddOnUpdate(BaseModel):
    """Schema for updating a package add-on"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price_monthly: Optional[int] = Field(None, ge=0)
    price_yearly: Optional[int] = Field(None, ge=0)
    configuration: Optional[Dict[str, Any]] = None
    limitations: Optional[Dict[str, Any]] = None
    compatible_packages: Optional[List[str]] = None
    max_quantity: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class PackageAddOnResponse(PackageAddOnBase):
    """Schema for package add-on response"""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPackageBase(BaseModel):
    """Base schema for user package subscription"""
    package_id: UUID = Field(..., description="Package ID")
    billing_cycle: str = Field(default="monthly", description="Billing cycle: monthly, yearly")
    auto_renew: bool = Field(default=True, description="Whether to auto-renew")
    legal_representative_id: Optional[UUID] = Field(None, description="Legal representative ID for delegated care")
    custom_configuration: Optional[Dict[str, Any]] = Field(None, description="JSON with custom configuration")
    selected_features: Optional[Union[List[str], Dict[str, Any]]] = Field(None, description="JSON with selected features (list or dict)")
    custom_limits: Optional[Dict[str, Any]] = Field(None, description="JSON with custom limits")

    @field_validator('billing_cycle')
    def validate_billing_cycle(cls, v):
        valid_cycles = ["monthly", "yearly"]
        if v not in valid_cycles:
            raise ValueError(f"Billing cycle must be one of: {valid_cycles}")
        return v


class UserPackageCreate(UserPackageBase):
    """Schema for creating a user package subscription"""
    referral_code: Optional[str] = Field(None, max_length=20, description="Referral code if used")
    add_ons: Optional[List[Dict[str, Any]]] = Field(None, description="List of add-ons to include")


class UserPackageUpdate(BaseModel):
    """Schema for updating a user package subscription"""
    auto_renew: Optional[bool] = None
    status: Optional[str] = None
    legal_representative_id: Optional[UUID] = None
    custom_configuration: Optional[Dict[str, Any]] = None
    selected_features: Optional[Dict[str, Any]] = None
    custom_limits: Optional[Dict[str, Any]] = None

    @field_validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["active", "suspended", "cancelled", "expired", "pending", "trial"]
            if v not in valid_statuses:
                raise ValueError(f"Status must be one of: {valid_statuses}")
        return v


class UserPackageAddOnBase(BaseModel):
    """Base schema for user package add-on"""
    add_on_id: UUID = Field(..., description="Add-on ID")
    quantity: int = Field(default=1, ge=1, description="Quantity of add-on")
    custom_configuration: Optional[Dict[str, Any]] = Field(None, description="JSON with custom configuration")
    billing_cycle: str = Field(default="monthly", description="Billing cycle: monthly, yearly")

    @field_validator('billing_cycle')
    def validate_billing_cycle(cls, v):
        valid_cycles = ["monthly", "yearly"]
        if v not in valid_cycles:
            raise ValueError(f"Billing cycle must be one of: {valid_cycles}")
        return v


class UserPackageAddOnCreate(UserPackageAddOnBase):
    """Schema for creating a user package add-on"""
    pass


class UserPackageAddOnResponse(UserPackageAddOnBase):
    """Schema for user package add-on response"""
    id: UUID
    user_package_id: UUID
    current_amount: int
    status: str
    added_at: datetime
    add_on: PackageAddOnResponse

    class Config:
        from_attributes = True


class UserPackageResponse(UserPackageBase):
    """Schema for user package response"""
    id: UUID
    user_id: UUID
    start_date: date
    end_date: Optional[date]
    current_amount: int
    next_billing_date: date
    status: str
    legal_capacity_verified: bool
    verification_date: Optional[datetime]
    referral_code_used: Optional[str]
    referral_commission_applied: bool
    created_at: datetime
    updated_at: datetime
    
    # Package details
    package: PackageResponse
    # Add-ons
    add_ons: List[UserPackageAddOnResponse] = []

    class Config:
        from_attributes = True


class PackageCustomization(BaseModel):
    """Schema for package customization options"""
    package_id: UUID
    custom_configuration: Dict[str, Any]
    selected_features: List[str]
    custom_limits: Dict[str, Any]
    add_ons: List[UserPackageAddOnCreate]


class PackageRecommendationRequest(BaseModel):
    """Schema for package recommendation request"""
    user_type: str = Field(..., description="Type of user: individual, professional, institutional")
    needs: List[str] = Field(..., description="List of user needs")
    budget_monthly: Optional[int] = Field(None, ge=0, description="Monthly budget in cents")
    budget_yearly: Optional[int] = Field(None, ge=0, description="Yearly budget in cents")
    required_features: Optional[List[str]] = Field(None, description="Required features")
    preferred_add_ons: Optional[List[str]] = Field(None, description="Preferred add-ons")


class LegalCapacityVerification(BaseModel):
    """Schema for legal capacity verification"""
    user_id: UUID = Field(..., description="User ID to verify")
    legal_representative_id: Optional[UUID] = Field(None, description="Legal representative ID")
    verification_notes: Optional[str] = Field(None, description="Verification notes")


class LegalCapacityResponse(BaseModel):
    """Schema for legal capacity verification response"""
    user_id: UUID
    can_contract: bool
    requires_representative: bool
    legal_representative_id: Optional[UUID]
    verification_status: str  # verified, pending, required
    message: str


class PackageComparison(BaseModel):
    """Schema for package comparison"""
    package_id: UUID
    name: str
    price_monthly_ars: float
    price_yearly_ars: Optional[float]
    features: List[str]
    limitations: List[str]
    is_recommended: bool = False


class PackageRecommendation(BaseModel):
    """Schema for package recommendation"""
    user_type: str
    recommended_package: Optional[PackageResponse] = None
    alternative_packages: List[PackageResponse] = []
    reasoning: str
    customization_suggestions: Optional[Dict[str, Any]] = None


class PackageStatisticsResponse(BaseModel):
    total_packages: int
    total_subscriptions: int
    total_revenue_ars: float
    # Puedes agregar más campos si el servicio retorna más métricas 