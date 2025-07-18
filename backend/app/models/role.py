from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import uuid
import json

class Role(BaseModel):
    """Role model for user roles and permissions"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    permissions = Column(Text, nullable=True)  # JSON string with permissions
    is_system = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    user_roles = relationship("UserRole", back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"

    @classmethod
    def get_system_roles(cls) -> list:
        return ["admin", "caregiver", "family", "caredperson", "institution_admin"]

    @classmethod
    def get_permissions(cls) -> list:
        return [
            "view_dashboard", "manage_users", "manage_devices", "view_reports",
            "edit_profile", "manage_alerts", "manage_reminders", "manage_billing",
            "manage_protocols", "manage_institutions", "view_audit_log"
        ]

    def has_permission(self, permission: str) -> bool:
        """
        Verifica si el rol tiene un permiso específico.
        
        Args:
            permission: Nombre del permiso a verificar
            
        Returns:
            bool: True si tiene el permiso, False en caso contrario
        """
        if not self.permissions:
            return False
        
        try:
            permissions_dict = json.loads(self.permissions)
        except (json.JSONDecodeError, TypeError):
            return False
        
        # Buscar en permisos anidados usando notación de punto
        parts = permission.split('.')
        current = permissions_dict
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        return bool(current)
    
    def get_permissions(self) -> dict:
        """
        Obtiene todos los permisos del rol.
        
        Returns:
            dict: Diccionario con todos los permisos
        """
        return self.permissions or {}
    
    @classmethod
    def get_default_roles(cls) -> list:
        """
        Retorna los roles por defecto del sistema.
        
        Returns:
            list: Lista de diccionarios con roles por defecto
        """
        return [
            {
                "name": "admin",
                "description": "Administrador del sistema con acceso completo",
                "permissions": {
                    "users": {"read": True, "write": True, "delete": True},
                    "cared_persons": {"read": True, "write": True, "delete": True},
                    "institutions": {"read": True, "write": True, "delete": True},
                    "devices": {"read": True, "write": True, "delete": True},
                    "protocols": {"read": True, "write": True, "delete": True},
                    "reports": {"read": True, "write": True},
                    "system": {"read": True, "write": True, "delete": True}
                }
            },
            {
                "name": "caregiver",
                "description": "Cuidador profesional con acceso a personas bajo su cuidado",
                "permissions": {
                    "cared_persons": {"read": True, "write": True},
                    "devices": {"read": True, "write": True},
                    "protocols": {"read": True, "write": True},
                    "reports": {"read": True},
                    "alerts": {"read": True, "write": True}
                }
            },
            {
                "name": "family",
                "description": "Familiar con acceso limitado a su ser querido",
                "permissions": {
                    "cared_persons": {"read": True},
                    "devices": {"read": True},
                    "alerts": {"read": True},
                    "reports": {"read": True}
                }
            },
            {
                "name": "caredperson",
                "description": "Persona bajo cuidado con acceso a su propia información",
                "permissions": {
                    "self": {"read": True, "write": True},
                    "devices": {"read": True},
                    "alerts": {"read": True}
                }
            },
            {
                "name": "institution_admin",
                "description": "Administrador de institución con acceso a usuarios de su centro",
                "permissions": {
                    "institution_users": {"read": True, "write": True},
                    "institution_devices": {"read": True, "write": True},
                    "institution_reports": {"read": True, "write": True},
                    "protocols": {"read": True, "write": True}
                }
            }
        ] 