from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.core.database import Base
import uuid

class User(Base):
    """
    Modelo de usuario del sistema.
    
    Reglas de negocio implementadas:
    - Un usuario puede tener múltiples roles
    - Un usuario puede pertenecer a una institución
    - Un usuario puede ser cuidador de múltiples personas
    - Un usuario puede ser persona bajo cuidado
    - Los usuarios tienen preferencias y configuraciones personalizadas
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    user_type = Column(String(20), default="family")  # 'family', 'caregiver', 'patient', 'admin', 'institution_admin'
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"))
    preferences = Column(JSONB, default=dict)
    notification_settings = Column(JSONB, default=dict)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    institution = relationship("Institution", back_populates="users")
    cared_persons = relationship("CaredPerson", back_populates="user", cascade="all, delete-orphan")
    caregiver_assignments = relationship("CaregiverAssignment", foreign_keys="CaregiverAssignment.caregiver_id", cascade="all, delete-orphan")
    
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
    
    def get_full_name(self) -> str:
        """
        Obtiene el nombre completo del usuario.
        
        Returns:
            str: Nombre completo
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_roles(self) -> list:
        """
        Obtiene los roles del usuario.
        
        Returns:
            list: Lista de roles
        """
        return [user_role.role for user_role in self.roles]
    
    def has_role(self, role_name: str) -> bool:
        """
        Verifica si el usuario tiene un rol específico.
        
        Args:
            role_name: Nombre del rol a verificar
            
        Returns:
            bool: True si tiene el rol, False en caso contrario
        """
        for user_role in self.roles:
            if user_role.role.name == role_name:
                return True
        return False
    
    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el usuario tiene un permiso específico.
        
        Args:
            permission: Permiso a verificar
            
        Returns:
            bool: True si tiene el permiso, False en caso contrario
        """
        for user_role in self.roles:
            if user_role.role.has_permission(permission):
                return True
        return False
    
    def get_preferences(self) -> dict:
        """
        Obtiene las preferencias del usuario.
        
        Returns:
            dict: Preferencias del usuario
        """
        return self.preferences or {}
    
    def set_preference(self, key: str, value: any):
        """
        Establece una preferencia del usuario.
        
        Args:
            key: Clave de la preferencia
            value: Valor de la preferencia
        """
        if not self.preferences:
            self.preferences = {}
        
        self.preferences[key] = value
    
    def get_notification_settings(self) -> dict:
        """
        Obtiene la configuración de notificaciones del usuario.
        
        Returns:
            dict: Configuración de notificaciones
        """
        return self.notification_settings or {}
    
    def set_notification_setting(self, notification_type: str, enabled: bool, channels: list = None):
        """
        Establece una configuración de notificación.
        
        Args:
            notification_type: Tipo de notificación
            enabled: Si está habilitada
            channels: Canales de notificación (email, sms, push, etc.)
        """
        if not self.notification_settings:
            self.notification_settings = {}
        
        self.notification_settings[notification_type] = {
            "enabled": enabled,
            "channels": channels or ["email"]
        }
    
    def get_cared_persons(self) -> list:
        """
        Obtiene las personas bajo cuidado del usuario.
        
        Returns:
            list: Lista de personas bajo cuidado
        """
        return self.cared_persons
    
    def get_caregiver_assignments(self) -> list:
        """
        Obtiene las asignaciones de cuidado del usuario.
        
        Returns:
            list: Lista de asignaciones de cuidado
        """
        return self.caregiver_assignments
    
    @classmethod
    def get_user_types(cls) -> list:
        """
        Retorna los tipos de usuario disponibles.
        
        Returns:
            list: Lista de tipos de usuario
        """
        return [
            {"value": "family", "label": "Familiar", "description": "Miembro de la familia"},
            {"value": "caregiver", "label": "Cuidador", "description": "Cuidador profesional"},
            {"value": "patient", "label": "Paciente", "description": "Persona bajo cuidado"},
            {"value": "admin", "label": "Administrador", "description": "Administrador del sistema"},
            {"value": "institution_admin", "label": "Admin Institución", "description": "Administrador de institución"},
            {"value": "nurse", "label": "Enfermero/a", "description": "Enfermero/a profesional"},
            {"value": "doctor", "label": "Médico", "description": "Médico profesional"},
            {"value": "therapist", "label": "Terapeuta", "description": "Terapeuta especializado"},
            {"value": "volunteer", "label": "Voluntario", "description": "Voluntario"}
        ]
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para este usuario.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Debe tener al menos un rol
        if not self.roles:
            errors.append("El usuario debe tener al menos un rol asignado")
        
        # Regla: Si es paciente, debe tener información de cuidado
        if self.user_type == "patient" and not self.cared_persons:
            errors.append("Un usuario paciente debe tener información de cuidado")
        
        # Regla: Si es cuidador, debe tener asignaciones
        if self.user_type == "caregiver" and not self.caregiver_assignments:
            errors.append("Un cuidador debe tener al menos una asignación")
        
        return errors 