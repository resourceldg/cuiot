"""
Validaciones para el sistema de reportes
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.models.user import User
from app.schemas.user import UserType

def validate_user_can_create_reports(user: User) -> bool:
    """
    Validar que el usuario puede crear reportes (debe ser family o employee)
    
    Args:
        user: Usuario a validar
        
    Returns:
        bool: True si puede crear reportes
        
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    if user.user_type not in [UserType.FAMILY, UserType.EMPLOYEE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo familiares y empleados pueden crear reportes"
        )
    return True

def validate_user_exists(db: Session, user_id: UUID) -> User:
    """
    Validar que el usuario existe en la base de datos
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario a validar
        
    Returns:
        User: Usuario encontrado
        
    Raises:
        HTTPException: Si el usuario no existe
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

def validate_user_can_access_report(user: User, report_created_by_id: UUID, report_received_by_id: Optional[UUID] = None) -> bool:
    """
    Validar que el usuario puede acceder a un reporte específico
    
    Args:
        user: Usuario que intenta acceder
        report_created_by_id: ID del usuario que creó el reporte
        report_received_by_id: ID del usuario que recibió el reporte (opcional)
        
    Returns:
        bool: True si puede acceder
        
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    # El usuario puede acceder si:
    # 1. Es el creador del reporte
    # 2. Es el receptor del reporte
    # 3. Es un empleado (acceso administrativo)
    
    if user.id == report_created_by_id:
        return True
    
    if report_received_by_id and user.id == report_received_by_id:
        return True
    
    if user.user_type == UserType.EMPLOYEE:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para acceder a este reporte"
    )

def validate_user_can_modify_report(user: User, report_created_by_id: UUID) -> bool:
    """
    Validar que el usuario puede modificar un reporte específico
    
    Args:
        user: Usuario que intenta modificar
        report_created_by_id: ID del usuario que creó el reporte
        
    Returns:
        bool: True si puede modificar
        
    Raises:
        HTTPException: Si el usuario no tiene permisos
    """
    # El usuario puede modificar si:
    # 1. Es el creador del reporte
    # 2. Es un empleado (acceso administrativo)
    
    if user.id == report_created_by_id:
        return True
    
    if user.user_type == UserType.EMPLOYEE:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Solo el creador del reporte o un empleado pueden modificarlo"
    )

def validate_user_type_for_operation(user: User, required_types: list[UserType]) -> bool:
    """
    Validar que el usuario tiene el tipo requerido para una operación
    
    Args:
        user: Usuario a validar
        required_types: Lista de tipos de usuario permitidos
        
    Returns:
        bool: True si tiene el tipo requerido
        
    Raises:
        HTTPException: Si el usuario no tiene el tipo requerido
    """
    if user.user_type not in required_types:
        allowed_types = ", ".join([t.value for t in required_types])
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Esta operación requiere uno de los siguientes tipos de usuario: {allowed_types}"
        )
    return True 