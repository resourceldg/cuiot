from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
import uuid
from sqlalchemy.dialects.postgresql import UUID


class UserRole(BaseModel):
    """
    Modelo de relación muchos a muchos entre usuarios y roles.
    
    Reglas de negocio implementadas:
    - Un usuario puede tener uno o más roles
    - Los roles se asignan con timestamp para auditoría
    - La relación es configurable y extensible
    """
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Who assigned this role
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Role expiration date
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    
    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"
    
    @classmethod
    def assign_role_to_user(cls, db, user_id: uuid.UUID, role_name: str) -> bool:
        """
        Asigna un rol a un usuario por nombre de rol.
        Al asignar un nuevo rol, desactiva todos los roles activos previos del usuario (is_active=False, expires_at=ahora).
        Mantiene historial para auditoría.
        """
        from app.models.role import Role
        from datetime import datetime
        print(f"[LOG] [assign_role_to_user] Buscando rol '{role_name}' para usuario {user_id}")
        role = db.query(Role).filter(Role.name == role_name).first()
        print(f"[LOG] [assign_role_to_user] Rol encontrado: {role}")
        if not role:
            print(f"[LOG] [assign_role_to_user] Rol '{role_name}' no existe")
            return False
        # Desactivar todos los roles activos previos
        print(f"[LOG] [assign_role_to_user] Desactivando roles activos previos para usuario={user_id}")
        active_roles = db.query(cls).filter(
            cls.user_id == user_id,
            cls.is_active == True
        ).all()
        for ar in active_roles:
            ar.is_active = False
            ar.expires_at = datetime.utcnow()
        db.flush()  # Asegura que los cambios estén en la sesión antes de crear el nuevo rol
        # Verificar si ya tiene el rol activo (por si acaso)
        existing = db.query(cls).filter(
            cls.user_id == user_id,
            cls.role_id == role.id,
            cls.is_active == True
        ).first()
        if existing:
            print(f"[LOG] [assign_role_to_user] El usuario ya tiene el rol asignado y activo")
            return True
        print(f"[LOG] [assign_role_to_user] Creando nueva asignación usuario={user_id}, rol={role.id}")
        user_role = cls(user_id=user_id, role_id=role.id, is_active=True)
        db.add(user_role)
        print(f"[LOG] [assign_role_to_user] Antes de commit")
        db.commit()
        print(f"[LOG] [assign_role_to_user] Después de commit")
        return True
    
    @classmethod
    def remove_role_from_user(cls, db, user_id: uuid.UUID, role_name: str) -> bool:
        """
        Remueve un rol de un usuario por nombre de rol.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            role_name: Nombre del rol a remover
            
        Returns:
            bool: True si se removió correctamente, False en caso contrario
        """
        from app.models.role import Role
        
        # Buscar el rol por nombre
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return False
        
        # Buscar y eliminar la asignación
        user_role = db.query(cls).filter(
            cls.user_id == user_id,
            cls.role_id == role.id
        ).first()
        
        if user_role:
            db.delete(user_role)
            db.commit()
            return True
        
        return False
    
    @classmethod
    def get_user_roles(cls, db, user_id: uuid.UUID) -> list:
        """
        Obtiene todos los roles de un usuario.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            
        Returns:
            list: Lista de roles del usuario
        """
        from app.models.role import Role
        
        user_roles = db.query(cls).filter(cls.user_id == user_id).all()
        role_ids = [ur.role_id for ur in user_roles]
        
        roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
        return roles
    
    @classmethod
    def user_has_role(cls, db, user_id: uuid.UUID, role_name: str) -> bool:
        """
        Verifica si un usuario tiene un rol específico.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            role_name: Nombre del rol a verificar
            
        Returns:
            bool: True si tiene el rol, False en caso contrario
        """
        from app.models.role import Role
        
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return False
        
        user_role = db.query(cls).filter(
            cls.user_id == user_id,
            cls.role_id == role.id
        ).first()
        
        return user_role is not None 