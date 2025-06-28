from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Role(Base):
    """
    Modelo para roles de usuario en el sistema.
    
    Reglas de negocio implementadas:
    - Un usuario puede tener uno o más roles
    - Los roles tienen permisos específicos almacenados en JSONB
    - Los roles son configurables y extensibles
    """
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    permissions = Column(JSONB, nullable=False, default=dict)
    
    # Relaciones
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
    
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
        
        # Buscar en permisos anidados usando notación de punto
        parts = permission.split('.')
        current = self.permissions
        
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
                "name": "patient",
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