from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class UserRole(Base):
    """
    Modelo de relación muchos a muchos entre usuarios y roles.
    
    Reglas de negocio implementadas:
    - Un usuario puede tener uno o más roles
    - Los roles se asignan con timestamp para auditoría
    - La relación es configurable y extensible
    """
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
    
    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"
    
    @classmethod
    def assign_role_to_user(cls, db, user_id: uuid.UUID, role_name: str) -> bool:
        """
        Asigna un rol a un usuario por nombre de rol.
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            role_name: Nombre del rol a asignar
            
        Returns:
            bool: True si se asignó correctamente, False en caso contrario
        """
        from app.models.role import Role
        
        # Buscar el rol por nombre
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            return False
        
        # Verificar si ya existe la asignación
        existing = db.query(cls).filter(
            cls.user_id == user_id,
            cls.role_id == role.id
        ).first()
        
        if existing:
            return True  # Ya está asignado
        
        # Crear nueva asignación
        user_role = cls(user_id=user_id, role_id=role.id)
        db.add(user_role)
        db.commit()
        
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