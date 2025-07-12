from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials

from app.core.database import get_db
from app.services.auth import AuthService, security
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithRoles
from app.schemas.role import RoleAssign, RoleBase, RoleUpdate
from app.models.role import Role
from app.models.user import User

router = APIRouter()

# === ROLES ENDPOINTS (deben ir antes de cualquier endpoint con /{user_id}) ===

@router.get("/roles", response_model=List[dict])
def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Obtener lista de todos los roles del sistema"""
    if not current_user.has_permission("users.read", db):
        raise HTTPException(status_code=403, detail="No tiene permisos para ver roles")
    roles = db.query(Role).offset(skip).limit(limit).all()
    return [
        {
            "id": str(role.id),
            "name": role.name,
            "description": role.description,
            "permissions": role.permissions,
            "is_system": role.is_system,
            "created_at": role.created_at.isoformat() if role.created_at else None,
            "updated_at": role.updated_at.isoformat() if role.updated_at else None,
            "is_active": role.is_active
        }
        for role in roles
    ]

@router.post("/roles", status_code=201)
def create_role(
    role_data: RoleBase,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Crear un nuevo rol (solo admin, excepto el primero)."""
    from app.models.role import Role
    role_count = db.query(Role).count()
    if role_count == 0:
        # Permitir crear el primer rol sin autenticación
        pass
    else:
        # Si ya hay roles, exigir autenticación y permiso
        auth_header = request.headers.get("authorization") if request else None
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Not authenticated")
        token = auth_header.split(" ", 1)[1]
        current_user = AuthService.get_current_user_from_token(db, token)
        if not current_user or not current_user.has_permission("users.write", db):
            raise HTTPException(status_code=403, detail="No tiene permisos para crear roles")
        if not current_user.has_role("admin"):
            raise HTTPException(status_code=403, detail="Solo administradores pueden crear roles")
    # Verificar si ya existe
    existing = db.query(Role).filter_by(name=role_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    import json
    from datetime import datetime
    # Serializar permissions si es dict
    permissions = role_data.permissions
    if isinstance(permissions, dict):
        permissions = json.dumps(permissions)
    role = Role(
        name=role_data.name,
        description=role_data.description,
        permissions=permissions,
        is_system=role_data.is_system,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"message": "Rol creado exitosamente", "role_id": str(role.id)}

@router.delete("/roles/{role_id}")
def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.require_permission("users.write"))
):
    """Eliminar un rol por id (solo admin)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar roles")
    role = db.query(Role).filter_by(id=role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(role)
    db.commit()
    return {"message": "Rol eliminado exitosamente", "role_id": role_id}

@router.get("/roles/{role_name}")
def get_role(role_name: str, db: Session = Depends(get_db)):
    """Obtener un rol por nombre."""
    from app.models.role import Role
    role = db.query(Role).filter_by(name=role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {
        "id": str(role.id),
        "name": role.name,
        "description": role.description,
        "permissions": role.permissions,
        "is_system": role.is_system,
        "created_at": role.created_at.isoformat() if role.created_at else None,
        "updated_at": role.updated_at.isoformat() if role.updated_at else None,
        "is_active": role.is_active
    }

@router.put("/roles/{role_id}")
def update_role(
    role_id: str,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.require_permission("users.write"))
):
    """Actualizar un rol existente (solo admin)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden actualizar roles")
    role = db.query(Role).filter_by(id=role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    # No permitir cambiar el nombre de roles de sistema
    if role.is_system and role_data.name and role_data.name != role.name:
        raise HTTPException(status_code=400, detail="No se puede cambiar el nombre de un rol de sistema")
    # Actualizar campos
    if role_data.name:
        role.name = role_data.name
    if role_data.description is not None:
        role.description = role_data.description
    if role_data.permissions is not None:
        import json
        role.permissions = json.dumps(role_data.permissions) if isinstance(role_data.permissions, dict) else role_data.permissions
    if role_data.is_system is not None:
        role.is_system = role_data.is_system
    from datetime import datetime
    role.updated_at = datetime.now()
    db.commit()
    db.refresh(role)
    return {
        "message": "Rol actualizado exitosamente",
        "role_id": str(role.id)
    }

@router.get("/", response_model=List[UserWithRoles])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    institution_id: int = Query(None),
    is_freelance: bool = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get list of users"""
    users = UserService.get_users_with_roles(
        db, 
        skip=skip, 
        limit=limit,
        institution_id=institution_id,
        is_freelance=is_freelance
    )
    return users

@router.get("/{user_id}", response_model=UserWithRoles)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get user by ID with roles"""
    user = UserService.get_user_with_roles(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    from app.models.user import User
    user_count = db.query(User).count()
    if user_count == 0:
        # Permitir crear el primer usuario sin autenticación
        return UserService.create_user(db, user_data)
    # Si ya hay usuarios, exigir autenticación y permiso
    auth_header = request.headers.get("authorization") if request else None
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Not authenticated")
    token = auth_header.split(" ", 1)[1]
    current_user = AuthService.get_current_user_from_token(db, token)
    if not current_user or not current_user.has_permission("users.write", db):
        raise HTTPException(status_code=403, detail="No tiene permisos para crear usuarios")
    return UserService.create_user(db, user_data)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Update user information"""
    # Users can only update their own profile unless they have admin permissions
    if current_user.id != user_id and not current_user.has_permission("users.write", db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return UserService.update_user(db, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.require_permission("users.delete"))
):
    """Delete a user"""
    UserService.delete_user(db, user_id)

@router.post("/{user_id}/assign-role")
async def assign_role(
    user_id: UUID,
    role_data: RoleAssign,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Assign a role to a user"""
    if not current_user.has_permission("users.write", db):
        raise HTTPException(status_code=403, detail="No tiene permisos para asignar roles")
    try:
        success = UserService.assign_role(db, user_id, role_data.role_name)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to assign role"
            )
        return {"message": "Role assigned successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Error de permisos: {str(e)}")

@router.delete("/{user_id}/roles/{role_name}")
def remove_role(
    user_id: UUID,
    role_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.require_permission("users.write"))
):
    """Remove a role from a user"""
    success = UserService.remove_role(db, user_id, role_name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove role"
        )
    return {"message": "Role removed successfully"}

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

@router.patch("/{user_id}/password", status_code=200)
def change_password(
    user_id: UUID,
    data: PasswordChangeRequest = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Change user password"""
    if current_user.id != user_id and not current_user.has_permission("users.write", db):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not AuthService.verify_password(data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    user.password_hash = AuthService.get_password_hash(data.new_password)
    db.commit()
    return {"ok": True, "message": "Contraseña cambiada correctamente"}
