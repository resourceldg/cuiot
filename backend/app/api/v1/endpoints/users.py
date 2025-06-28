from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import (
    get_users, get_user_by_id, create_user, 
    update_user, delete_user
)
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Obtener usuario por ID"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.get("/", response_model=List[User])
async def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtener lista de usuarios"""
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear nuevo usuario"""
    try:
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear usuario: {str(e)}"
        )

@router.put("/{user_id}", response_model=User)
async def update_existing_user(
    user_id: UUID, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar usuario existente"""
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: UUID, db: Session = Depends(get_db)):
    """Eliminar usuario"""
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        ) 