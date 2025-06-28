from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base
import uuid


class BillingRecord(Base):
    """
    Modelo para registros de facturación.
    
    Reglas de negocio implementadas:
    - Cada suscripción genera registros de facturación
    - Los registros tienen estados de pago específicos
    - Soporte para diferentes métodos de pago
    - Historial completo de transacciones
    """
    __tablename__ = "billing_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("service_subscriptions.id"), nullable=False)
    billing_period_start = Column(DateTime(timezone=True), nullable=False)
    billing_period_end = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="ARS")
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), default="pending")  # pending, paid, failed, refunded
    payment_method = Column(String(50))  # credit_card, debit_card, bank_transfer, cash
    payment_date = Column(DateTime(timezone=True))
    invoice_number = Column(String(50), unique=True)
    payment_details = Column(JSONB, default=dict)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    subscription = relationship("ServiceSubscription", back_populates="billing_records")
    
    def __repr__(self):
        return f"<BillingRecord(id={self.id}, subscription_id={self.subscription_id}, amount={self.amount})>"
    
    def is_paid(self) -> bool:
        """
        Verifica si el registro está pagado.
        
        Returns:
            bool: True si está pagado, False en caso contrario
        """
        return self.payment_status == "paid"
    
    def is_overdue(self) -> bool:
        """
        Verifica si el registro está vencido.
        
        Returns:
            bool: True si está vencido, False en caso contrario
        """
        from datetime import datetime
        
        if self.is_paid():
            return False
        
        now = datetime.utcnow()
        return now > self.billing_period_end
    
    def get_days_overdue(self) -> int:
        """
        Obtiene los días de atraso.
        
        Returns:
            int: Días de atraso, 0 si no está vencido
        """
        from datetime import datetime
        
        if not self.is_overdue():
            return 0
        
        now = datetime.utcnow()
        delta = now - self.billing_period_end
        return delta.days
    
    def get_payment_details(self) -> dict:
        """
        Obtiene los detalles del pago.
        
        Returns:
            dict: Detalles del pago
        """
        return self.payment_details or {}
    
    def set_payment_details(self, payment_method: str, transaction_id: str = None, 
                           card_last4: str = None, bank_account: str = None):
        """
        Establece los detalles del pago.
        
        Args:
            payment_method: Método de pago
            transaction_id: ID de la transacción
            card_last4: Últimos 4 dígitos de la tarjeta
            bank_account: Cuenta bancaria
        """
        self.payment_details = {
            "payment_method": payment_method,
            "transaction_id": transaction_id,
            "card_last4": card_last4,
            "bank_account": bank_account,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None
        }
    
    def calculate_total(self):
        """
        Calcula el monto total del registro.
        """
        self.total_amount = self.amount + self.tax_amount - self.discount_amount
    
    def mark_as_paid(self, payment_date=None, payment_method=None):
        """
        Marca el registro como pagado.
        
        Args:
            payment_date: Fecha del pago
            payment_method: Método de pago
        """
        from datetime import datetime
        
        self.payment_status = "paid"
        self.payment_date = payment_date or datetime.utcnow()
        
        if payment_method:
            self.payment_method = payment_method
    
    def mark_as_failed(self, reason: str = None):
        """
        Marca el registro como fallido.
        
        Args:
            reason: Razón del fallo
        """
        self.payment_status = "failed"
        if reason:
            self.notes = f"Pago fallido: {reason}"
    
    def refund(self, refund_amount: float = None, reason: str = None):
        """
        Procesa un reembolso.
        
        Args:
            refund_amount: Monto del reembolso
            reason: Razón del reembolso
        """
        self.payment_status = "refunded"
        if refund_amount:
            self.discount_amount = refund_amount
            self.calculate_total()
        
        if reason:
            self.notes = f"Reembolso: {reason}"
    
    @classmethod
    def get_payment_statuses(cls) -> list:
        """
        Retorna los estados de pago disponibles.
        
        Returns:
            list: Lista de estados de pago
        """
        return [
            {"value": "pending", "label": "Pendiente", "description": "Pago pendiente"},
            {"value": "paid", "label": "Pagado", "description": "Pago completado"},
            {"value": "failed", "label": "Fallido", "description": "Pago fallido"},
            {"value": "refunded", "label": "Reembolsado", "description": "Pago reembolsado"},
            {"value": "cancelled", "label": "Cancelado", "description": "Pago cancelado"}
        ]
    
    @classmethod
    def get_payment_methods(cls) -> list:
        """
        Retorna los métodos de pago disponibles.
        
        Returns:
            list: Lista de métodos de pago
        """
        return [
            {"value": "credit_card", "label": "Tarjeta de Crédito", "description": "Pago con tarjeta de crédito"},
            {"value": "debit_card", "label": "Tarjeta de Débito", "description": "Pago con tarjeta de débito"},
            {"value": "bank_transfer", "label": "Transferencia Bancaria", "description": "Transferencia bancaria"},
            {"value": "cash", "label": "Efectivo", "description": "Pago en efectivo"},
            {"value": "check", "label": "Cheque", "description": "Pago con cheque"},
            {"value": "digital_wallet", "label": "Billetera Digital", "description": "Pago con billetera digital"},
            {"value": "crypto", "label": "Criptomoneda", "description": "Pago con criptomoneda"}
        ]
    
    @classmethod
    def get_overdue_records(cls, db, days_overdue: int = 1) -> list:
        """
        Obtiene registros vencidos.
        
        Args:
            db: Sesión de base de datos
            days_overdue: Días de atraso mínimo
            
        Returns:
            list: Lista de registros vencidos
        """
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_overdue)
        
        return db.query(cls).filter(
            cls.payment_status == "pending",
            cls.billing_period_end < cutoff_date
        ).all()
    
    @classmethod
    def get_pending_records(cls, db, subscription_id: uuid.UUID = None) -> list:
        """
        Obtiene registros pendientes de pago.
        
        Args:
            db: Sesión de base de datos
            subscription_id: ID de la suscripción (opcional)
            
        Returns:
            list: Lista de registros pendientes
        """
        query = db.query(cls).filter(cls.payment_status == "pending")
        
        if subscription_id:
            query = query.filter(cls.subscription_id == subscription_id)
        
        return query.all()
    
    @classmethod
    def generate_invoice_number(cls, db) -> str:
        """
        Genera un número de factura único.
        
        Args:
            db: Sesión de base de datos
            
        Returns:
            str: Número de factura único
        """
        from datetime import datetime
        
        # Formato: INV-YYYYMMDD-XXXX
        date_prefix = datetime.utcnow().strftime("%Y%m%d")
        
        # Buscar el último número para hoy
        last_invoice = db.query(cls).filter(
            cls.invoice_number.like(f"INV-{date_prefix}-%")
        ).order_by(cls.invoice_number.desc()).first()
        
        if last_invoice:
            # Extraer el número y incrementar
            last_number = int(last_invoice.invoice_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"INV-{date_prefix}-{new_number:04d}"
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para este registro.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Fecha de inicio debe ser anterior a fecha de fin
        if self.billing_period_start >= self.billing_period_end:
            errors.append("La fecha de inicio del período debe ser anterior a la fecha de fin")
        
        # Regla: Monto total debe ser positivo
        if self.total_amount <= 0:
            errors.append("El monto total debe ser mayor a cero")
        
        # Regla: Si está pagado, debe tener fecha de pago
        if self.payment_status == "paid" and not self.payment_date:
            errors.append("Un registro pagado debe tener fecha de pago")
        
        # Regla: Si está pagado, debe tener método de pago
        if self.payment_status == "paid" and not self.payment_method:
            errors.append("Un registro pagado debe tener método de pago")
        
        return errors 