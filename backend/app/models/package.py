from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel
import uuid
from datetime import datetime

class Package(BaseModel):
    """Package model - Central business entity for service packages"""
    __tablename__ = "packages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Package identification
    package_type = Column(String(50), nullable=False, index=True)  # individual, professional, institutional
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Pricing
    price_monthly = Column(Integer, nullable=False)  # Price in cents (ARS)
    price_yearly = Column(Integer, nullable=True)  # Price in cents (ARS)
    currency = Column(String(3), default="ARS", nullable=False)
    
    # Base limits and features
    max_users = Column(Integer, nullable=True)  # None for unlimited
    max_devices = Column(Integer, nullable=True)  # None for unlimited
    max_storage_gb = Column(Integer, nullable=True)  # Storage limit in GB
    features = Column(JSONB, nullable=True)  # JSON with feature list
    limitations = Column(JSONB, nullable=True)  # JSON with limitations
    
    # Personalization options
    customizable_options = Column(JSONB, nullable=True)  # JSON with customization options
    add_ons_available = Column(JSONB, nullable=True)  # JSON with available add-ons
    base_configuration = Column(JSONB, nullable=True)  # JSON with base configuration
    is_customizable = Column(Boolean, default=True, nullable=False)  # Whether package can be customized
    
    # Support and service level
    support_level = Column(String(50), nullable=True)  # basic, standard, premium, enterprise
    response_time_hours = Column(Integer, nullable=True)  # Support response time
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)  # For highlighting
    
    # Relationships
    user_packages = relationship("UserPackage", back_populates="package")
    institution_packages = relationship("InstitutionPackage", back_populates="package", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Package(type='{self.package_type}', name='{self.name}', price={self.price_monthly})>"
    
    @property
    def price_monthly_ars(self) -> float:
        """Get monthly price in ARS"""
        return self.price_monthly / 100 if self.price_monthly else 0.0
    
    @property
    def price_yearly_ars(self) -> float:
        """Get yearly price in ARS"""
        return self.price_yearly / 100 if self.price_yearly else 0.0
    
    @property
    def has_unlimited_users(self) -> bool:
        """Check if package has unlimited users"""
        return self.max_users is None
    
    @property
    def has_unlimited_devices(self) -> bool:
        """Check if package has unlimited devices"""
        return self.max_devices is None
    
    @classmethod
    def get_package_types(cls) -> list:
        """Returns available package types"""
        return ["individual", "professional", "institutional"]
    
    @classmethod
    def get_support_levels(cls) -> list:
        """Returns available support levels"""
        return ["basic", "standard", "premium", "enterprise"]
    
    @classmethod
    def get_individual_packages(cls) -> list:
        """Returns individual package types"""
        return ["basic", "familiar", "premium"]
    
    @classmethod
    def get_professional_packages(cls) -> list:
        """Returns professional package types"""
        return ["professional", "professional_plus"]
    
    @classmethod
    def get_institutional_packages(cls) -> list:
        """Returns institutional package types"""
        return ["institutional_basic", "institutional_professional", "institutional_enterprise"]


class PackageAddOn(BaseModel):
    """PackageAddOn model - Add-ons that can be added to packages"""
    __tablename__ = "package_add_ons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Add-on identification
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    add_on_type = Column(String(50), nullable=False, index=True)  # storage, users, devices, features, support
    
    # Pricing
    price_monthly = Column(Integer, nullable=False)  # Price in cents (ARS)
    price_yearly = Column(Integer, nullable=True)  # Price in cents (ARS)
    
    # Configuration
    configuration = Column(JSONB, nullable=True)  # JSON with add-on configuration
    limitations = Column(JSONB, nullable=True)  # JSON with limitations
    
    # Compatibility
    compatible_packages = Column(JSONB, nullable=True)  # JSON with compatible package types
    max_quantity = Column(Integer, nullable=True)  # Maximum quantity allowed
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user_package_add_ons = relationship("UserPackageAddOn", back_populates="add_on")
    
    def __repr__(self):
        return f"<PackageAddOn(name='{self.name}', type='{self.add_on_type}', price={self.price_monthly})>"
    
    @property
    def price_monthly_ars(self) -> float:
        """Get monthly price in ARS"""
        return self.price_monthly / 100 if self.price_monthly else 0.0
    
    @property
    def price_yearly_ars(self) -> float:
        """Get yearly price in ARS"""
        return self.price_yearly / 100 if self.price_yearly else 0.0
    
    @classmethod
    def get_add_on_types(cls) -> list:
        """Returns available add-on types"""
        return ["storage", "users", "devices", "features", "support", "analytics", "integration"]


class UserPackage(BaseModel):
    """UserPackage model - User subscriptions to packages"""
    __tablename__ = "user_packages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Subscription info
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    
    # Subscription period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # None for ongoing subscriptions
    auto_renew = Column(Boolean, default=True, nullable=False)
    
    # Billing
    billing_cycle = Column(String(20), default="monthly", nullable=False)  # monthly, yearly
    current_amount = Column(Integer, nullable=False)  # Current price in cents
    next_billing_date = Column(Date, nullable=False)
    
    # Status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    
    # Personalization
    custom_configuration = Column(JSONB, nullable=True)  # JSON with custom configuration
    selected_features = Column(JSONB, nullable=True)  # JSON with selected features
    custom_limits = Column(JSONB, nullable=True)  # JSON with custom limits
    
    # Legal capacity validation
    legal_capacity_verified = Column(Boolean, default=False, nullable=False)
    legal_representative_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verification_date = Column(DateTime, nullable=True)
    
    # Referral info
    referral_code_used = Column(String(20), nullable=True)
    referral_commission_applied = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="user_packages")
    package = relationship("Package", back_populates="user_packages")
    legal_representative = relationship("User", foreign_keys=[legal_representative_id])
    billing_records = relationship("BillingRecord", back_populates="user_package")
    add_ons = relationship("UserPackageAddOn", back_populates="user_package")
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<UserPackage(user_id={self.user_id}, package_id={self.package_id}, status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        from datetime import date
        today = date.today()
        
        if not self.status_type or self.status_type.name != "active":
            return False
        
        if self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True
    
    @property
    def current_amount_ars(self) -> float:
        """Get current amount in ARS"""
        return self.current_amount / 100 if self.current_amount else 0.0
    
    @property
    def days_until_renewal(self) -> int:
        """Calculate days until next billing"""
        from datetime import date
        today = date.today()
        return (self.next_billing_date - today).days
    
    @property
    def requires_legal_verification(self) -> bool:
        """Check if legal verification is required"""
        return not self.legal_capacity_verified
    
    @property
    def total_add_ons_cost(self) -> int:
        """Calculate total cost of add-ons in cents"""
        total = 0
        for add_on in self.add_ons:
            if add_on.is_active:
                total += add_on.current_amount
        return total
    
    @property
    def total_cost_ars(self) -> float:
        """Get total cost including add-ons in ARS"""
        total_cents = self.current_amount + self.total_add_ons_cost
        return total_cents / 100
    
    @property
    def status(self) -> str:
        """Get status as string for backward compatibility"""
        if self.status_type:
            return self.status_type.name
        return "unknown"
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "suspended", "cancelled", "expired", "pending", "trial"]
    
    @classmethod
    def get_billing_cycles(cls) -> list:
        """Returns available billing cycles"""
        return ["monthly", "yearly"]
    
    def cancel_subscription(self):
        """Cancel the subscription"""
        # Nota: Este método necesita acceso a la sesión de DB para buscar el status_type
        # Se recomienda usar el método del servicio en su lugar
        # Por ahora, mantenemos compatibilidad con el campo legacy
        # No asignamos a status ya que es una propiedad de solo lectura
        self.auto_renew = False
    
    def suspend_subscription(self):
        """Suspend the subscription"""
        # Nota: Este método necesita acceso a la sesión de DB para buscar el status_type
        # Se recomienda usar el método del servicio en su lugar
        # Por ahora, mantenemos compatibilidad con el campo legacy
        # No asignamos a status ya que es una propiedad de solo lectura
        pass
    
    def reactivate_subscription(self):
        """Reactivate the subscription"""
        # Nota: Este método necesita acceso a la sesión de DB para buscar el status_type
        # Se recomienda usar el método del servicio en su lugar
        # Por ahora, mantenemos compatibilidad con el campo legacy
        # No asignamos a status ya que es una propiedad de solo lectura
        pass
    
    def verify_legal_capacity(self, verified_by_user_id: UUID = None):
        """Mark legal capacity as verified"""
        self.legal_capacity_verified = True
        self.verification_date = datetime.utcnow()
        if verified_by_user_id:
            self.legal_representative_id = verified_by_user_id


class UserPackageAddOn(BaseModel):
    """UserPackageAddOn model - Add-ons added to user packages"""
    __tablename__ = "user_package_add_ons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relationship
    user_package_id = Column(UUID(as_uuid=True), ForeignKey("user_packages.id", ondelete="CASCADE"), nullable=False)
    add_on_id = Column(UUID(as_uuid=True), ForeignKey("package_add_ons.id"), nullable=False)
    
    # Configuration
    quantity = Column(Integer, default=1, nullable=False)
    custom_configuration = Column(JSONB, nullable=True)  # JSON with custom configuration
    
    # Billing
    current_amount = Column(Integer, nullable=False)  # Current price in cents
    billing_cycle = Column(String(20), default="monthly", nullable=False)
    
    # Status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user_package = relationship("UserPackage", back_populates="add_ons")
    add_on = relationship("PackageAddOn", back_populates="user_package_add_ons")
    status_type = relationship("StatusType")
    
    def __repr__(self):
        return f"<UserPackageAddOn(user_package_id={self.user_package_id}, add_on_id={self.add_on_id}, quantity={self.quantity})>"
    
    @property
    def is_active(self) -> bool:
        """Check if add-on is active"""
        return self.status_type and self.status_type.name == "active"
    
    @property
    def status(self) -> str:
        """Get status as string for backward compatibility"""
        if self.status_type:
            return self.status_type.name
        return "unknown"
    
    @property
    def current_amount_ars(self) -> float:
        """Get current amount in ARS"""
        return self.current_amount / 100 if self.current_amount else 0.0
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "suspended", "cancelled"] 