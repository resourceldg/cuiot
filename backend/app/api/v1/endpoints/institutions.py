from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.institution import Institution
from app.schemas.institution import Institution as InstitutionSchema
from app.services.auth import AuthService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[InstitutionSchema])
def get_institutions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Obtener listado de instituciones"""
    institutions = db.query(Institution).offset(skip).limit(limit).all()
    return institutions 