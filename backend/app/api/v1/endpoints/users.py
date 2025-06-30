from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID

from app.core.database import get_db
from app.services.auth import AuthService
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithRoles

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    institution_id: int = Query(None),
    is_freelance: bool = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get list of users"""
    users = UserService.get_users(
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
    current_user = Depends(AuthService.require_permission("users.write"))
):
    """Create a new user"""
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
    if current_user.id != user_id and not current_user.has_permission("users.write"):
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

@router.post("/{user_id}/roles/{role_name}")
def assign_role(
    user_id: UUID,
    role_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.require_permission("users.write"))
):
    """Assign a role to a user"""
    success = UserService.assign_role(db, user_id, role_name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign role"
        )
    return {"message": "Role assigned successfully"}

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
    user_id: int,
    data: PasswordChangeRequest = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Change user password"""
    if current_user.id != user_id and not current_user.has_permission("users.write"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not AuthService.verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    user.hashed_password = AuthService.get_password_hash(data.new_password)
    db.commit()
    return {"ok": True, "message": "Contraseña cambiada correctamente"}
