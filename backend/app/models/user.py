from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class User(Base):
    """Modelo de usuario (familiar o empleado)"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    user_type = Column(String(20), default="family")  # 'family', 'employee'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    elderly_persons = relationship("ElderlyPerson", back_populates="user", cascade="all, delete-orphan")
    
    # Relaciones con reportes creados
    events_created = relationship("Event", foreign_keys="Event.created_by_id", back_populates="created_by")
    alerts_created = relationship("Alert", foreign_keys="Alert.created_by_id", back_populates="created_by")
    reminders_created = relationship("Reminder", foreign_keys="Reminder.created_by_id", back_populates="created_by")
    
    # Relaciones con reportes recibidos
    events_received = relationship("Event", foreign_keys="Event.received_by_id", back_populates="received_by")
    alerts_received = relationship("Alert", foreign_keys="Alert.received_by_id", back_populates="received_by")
    reminders_received = relationship("Reminder", foreign_keys="Reminder.received_by_id", back_populates="received_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', type='{self.user_type}')>" 