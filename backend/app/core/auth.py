from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.services.auth import AuthService

# Configurar OAuth2 scheme para JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtener el usuario actual basado en el token JWT
    
    Args:
        token: Token JWT del header Authorization
        db: Sesión de base de datos
        
    Returns:
        User: Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verificar token
    payload = AuthService.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # Obtener usuario
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    try:
        user_uuid = UUID(user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
    except ValueError:
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Obtener el usuario actual activo
    
    Args:
        current_user: Usuario actual obtenido del token
        
    Returns:
        User: Usuario activo
        
    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def require_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Requerir que el usuario tenga el rol 'admin'.
    
    Args:
        current_user: Usuario actual obtenido del token
        db: Sesión de base de datos
        
    Returns:
        User: Usuario administrador
        
    Raises:
        HTTPException: Si el usuario no tiene el rol 'admin'
    """
    from app.models.role import Role
    from app.models.user_role import UserRole
    
    # Obtener los roles del usuario
    user_roles = db.query(UserRole).filter(UserRole.user_id == current_user.id, UserRole.is_active == True).all()
    role_names = []
    for ur in user_roles:
        role = db.query(Role).filter(Role.id == ur.role_id).first()
        if role:
            role_names.append(role.name)
            
    if "admin" not in role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user 