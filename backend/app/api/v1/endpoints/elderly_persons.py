from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.elderly_person import ElderlyPerson, ElderlyPersonCreate, ElderlyPersonUpdate
from app.services.elderly_person import (
    get_elderly_persons, get_elderly_person_by_id, create_elderly_person,
    update_elderly_person, delete_elderly_person, get_elderly_persons_by_user
)

router = APIRouter()

@router.get("/", response_model=List[ElderlyPerson])
async def get_all_elderly_persons(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtener lista de adultos mayores"""
    elderly_persons = get_elderly_persons(db, skip=skip, limit=limit)
    return elderly_persons

@router.get("/user/{user_id}", response_model=List[ElderlyPerson])
async def get_elderly_persons_by_user_id(
    user_id: UUID, 
    db: Session = Depends(get_db)
):
    """Obtener adultos mayores por usuario (familiar)"""
    elderly_persons = get_elderly_persons_by_user(db, user_id)
    return elderly_persons

@router.get("/{elderly_person_id}", response_model=ElderlyPerson)
async def get_elderly_person(
    elderly_person_id: UUID, 
    db: Session = Depends(get_db)
):
    """Obtener adulto mayor por ID"""
    elderly_person = get_elderly_person_by_id(db, elderly_person_id)
    if not elderly_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adulto mayor no encontrado"
        )
    return elderly_person

@router.post("/", response_model=ElderlyPerson, status_code=status.HTTP_201_CREATED)
async def create_new_elderly_person(
    elderly_person: ElderlyPersonCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo adulto mayor"""
    try:
        # Asignar el user_id del usuario autenticado
        elderly_person.user_id = current_user.id
        return create_elderly_person(db, elderly_person)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear adulto mayor: {str(e)}"
        )

@router.put("/{elderly_person_id}", response_model=ElderlyPerson)
async def update_existing_elderly_person(
    elderly_person_id: UUID, 
    elderly_person_update: ElderlyPersonUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar adulto mayor existente"""
    elderly_person = update_elderly_person(db, elderly_person_id, elderly_person_update)
    if not elderly_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adulto mayor no encontrado"
        )
    return elderly_person

@router.delete("/{elderly_person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_elderly_person(
    elderly_person_id: UUID, 
    db: Session = Depends(get_db)
):
    """Eliminar adulto mayor"""
    success = delete_elderly_person(db, elderly_person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adulto mayor no encontrado"
        ) 