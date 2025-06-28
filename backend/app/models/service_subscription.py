from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class ServiceSubscription(Base):
    """
    Modelo para suscripciones de servicios.
    
    Reglas de negocio implementadas:
    - Una persona puede tener múltiples servicios contratados
    - Los servicios tienen diferentes niveles y precios
    - Las suscripciones tienen fechas de inicio y fin
    - Soporte para facturación y pagos
    """
    __tablename__ = "service_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    service_type = Column(String(50), nullable=False, index=True)  # basic, standard, premium, custom
    service_name = Column(String(200), nullable=False)
    description = Column(Text)
    features = Column(JSONB, default=dict)
    pricing = Column(JSONB, default=dict)
    billing_cycle = Column(String(20), default="monthly")  # monthly, quarterly, yearly
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))  # Null para suscripciones indefinidas
    status = Column(String(20), default="active")  # active, suspended, cancelled, expired
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    cared_person = relationship("CaredPerson", back_populates="service_subscriptions")
    billing_records = relationship("BillingRecord", back_populates="subscription", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ServiceSubscription(id={self.id}, service_type='{self.service_type}', cared_person_id={self.cared_person_id})>"
    
    def is_active_subscription(self) -> bool:
        """
        Verifica si la suscripción está activa.
        
        Returns:
            bool: True si está activa, False en caso contrario
        """
        from datetime import datetime
        
        now = datetime.utcnow()
        
        # Verificar fecha de inicio
        if self.start_date and now < self.start_date:
            return False
        
        # Verificar fecha de fin
        if self.end_date and now > self.end_date:
            return False
        
        # Verificar estado
        return self.status == "active"
    
    def get_features(self) -> list:
        """
        Obtiene las características del servicio.
        
        Returns:
            list: Lista de características
        """
        if not self.features:
            return []
        
        return self.features.get("features", [])
    
    def add_feature(self, feature_name: str, description: str = None, is_enabled: bool = True):
        """
        Agrega una característica al servicio.
        
        Args:
            feature_name: Nombre de la característica
            description: Descripción de la característica
            is_enabled: Si está habilitada
        """
        if not self.features:
            self.features = {"features": []}
        
        feature = {
            "name": feature_name,
            "description": description,
            "is_enabled": is_enabled,
            "active": True
        }
        
        self.features["features"].append(feature)
    
    def get_pricing(self) -> dict:
        """
        Obtiene la información de precios del servicio.
        
        Returns:
            dict: Información de precios
        """
        return self.pricing or {}
    
    def set_pricing(self, base_price: float, currency: str = "ARS", 
                   setup_fee: float = 0, discount_percentage: float = 0):
        """
        Establece la información de precios del servicio.
        
        Args:
            base_price: Precio base del servicio
            currency: Moneda (ARS, USD, etc.)
            setup_fee: Cargo de instalación
            discount_percentage: Porcentaje de descuento
        """
        self.pricing = {
            "base_price": base_price,
            "currency": currency,
            "setup_fee": setup_fee,
            "discount_percentage": discount_percentage,
            "final_price": base_price * (1 - discount_percentage / 100) + setup_fee
        }
    
    def get_monthly_price(self) -> float:
        """
        Obtiene el precio mensual del servicio.
        
        Returns:
            float: Precio mensual
        """
        pricing = self.get_pricing()
        base_price = pricing.get("base_price", 0)
        
        if self.billing_cycle == "monthly":
            return base_price
        elif self.billing_cycle == "quarterly":
            return base_price / 3
        elif self.billing_cycle == "yearly":
            return base_price / 12
        
        return base_price
    
    def get_next_billing_date(self) -> datetime:
        """
        Obtiene la fecha del próximo cobro.
        
        Returns:
            datetime: Fecha del próximo cobro
        """
        from datetime import datetime, timedelta
        
        if not self.is_active_subscription():
            return None
        
        # Calcular basado en el ciclo de facturación
        if self.billing_cycle == "monthly":
            return self.start_date + timedelta(days=30)
        elif self.billing_cycle == "quarterly":
            return self.start_date + timedelta(days=90)
        elif self.billing_cycle == "yearly":
            return self.start_date + timedelta(days=365)
        
        return self.start_date + timedelta(days=30)
    
    @classmethod
    def get_service_types(cls) -> list:
        """
        Retorna los tipos de servicio disponibles.
        
        Returns:
            list: Lista de tipos de servicio
        """
        return [
            {
                "value": "basic", 
                "label": "Básico", 
                "description": "Servicio básico de monitoreo",
                "features": ["Monitoreo básico", "Alertas por email", "1 contacto de emergencia"],
                "base_price": 5000
            },
            {
                "value": "standard", 
                "label": "Estándar", 
                "description": "Servicio estándar con más funcionalidades",
                "features": ["Monitoreo avanzado", "Alertas SMS y email", "3 contactos de emergencia", "Reportes básicos"],
                "base_price": 8000
            },
            {
                "value": "premium", 
                "label": "Premium", 
                "description": "Servicio premium con todas las funcionalidades",
                "features": ["Monitoreo completo", "Alertas en tiempo real", "Contactos ilimitados", "Reportes avanzados", "Soporte 24/7"],
                "base_price": 12000
            },
            {
                "value": "institutional", 
                "label": "Institucional", 
                "description": "Servicio para instituciones",
                "features": ["Monitoreo múltiple", "Dashboard institucional", "Reportes personalizados", "API access", "Soporte dedicado"],
                "base_price": 25000
            },
            {
                "value": "custom", 
                "label": "Personalizado", 
                "description": "Servicio personalizado según necesidades",
                "features": ["Características a medida", "Precio personalizado"],
                "base_price": 0
            }
        ]
    
    @classmethod
    def get_billing_cycles(cls) -> list:
        """
        Retorna los ciclos de facturación disponibles.
        
        Returns:
            list: Lista de ciclos de facturación
        """
        return [
            {"value": "monthly", "label": "Mensual", "description": "Facturación mensual"},
            {"value": "quarterly", "label": "Trimestral", "description": "Facturación cada 3 meses"},
            {"value": "yearly", "label": "Anual", "description": "Facturación anual con descuento"}
        ]
    
    @classmethod
    def get_status_options(cls) -> list:
        """
        Retorna las opciones de estado disponibles.
        
        Returns:
            list: Lista de estados
        """
        return [
            {"value": "active", "label": "Activo", "description": "Suscripción activa"},
            {"value": "suspended", "label": "Suspendido", "description": "Suscripción temporalmente suspendida"},
            {"value": "cancelled", "label": "Cancelado", "description": "Suscripción cancelada"},
            {"value": "expired", "label": "Expirado", "description": "Suscripción expirada"},
            {"value": "pending", "label": "Pendiente", "description": "Suscripción pendiente de activación"}
        ]
    
    @classmethod
    def get_active_subscriptions(cls, db, cared_person_id: uuid.UUID) -> list:
        """
        Obtiene las suscripciones activas de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            list: Lista de suscripciones activas
        """
        return db.query(cls).filter(
            cls.cared_person_id == cared_person_id,
            cls.status == "active"
        ).all()
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para esta suscripción.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Fecha de inicio debe ser anterior a fecha de fin (si existe)
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            errors.append("La fecha de inicio debe ser anterior a la fecha de fin")
        
        # Regla: Debe tener al menos una característica
        if not self.get_features():
            errors.append("El servicio debe tener al menos una característica")
        
        # Regla: Debe tener información de precios
        if not self.get_pricing():
            errors.append("El servicio debe tener información de precios")
        
        return errors 