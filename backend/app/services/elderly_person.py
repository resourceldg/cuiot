from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from app.models.elderly_person import ElderlyPerson
from app.schemas.elderly_person import ElderlyPersonCreate, ElderlyPersonUpdate

def get_elderly_persons(db: Session, skip: int = 0, limit: int = 100) -> List[ElderlyPerson]:
    """Obtener lista de adultos mayores no eliminados"""
    return db.query(ElderlyPerson).filter(ElderlyPerson.is_deleted == False).offset(skip).limit(limit).all()

def get_elderly_person_by_id(db: Session, elderly_person_id: UUID) -> Optional[ElderlyPerson]:
    """Obtener adulto mayor por ID (solo si no está eliminado)"""
    return db.query(ElderlyPerson).filter(ElderlyPerson.id == elderly_person_id, ElderlyPerson.is_deleted == False).first()

def get_elderly_persons_by_user(db: Session, user_id: UUID) -> List[ElderlyPerson]:
    """Obtener adultos mayores por usuario (no eliminados)"""
    return db.query(ElderlyPerson).filter(ElderlyPerson.user_id == user_id, ElderlyPerson.is_deleted == False).all()

def create_elderly_person(db: Session, elderly_person: ElderlyPersonCreate) -> ElderlyPerson:
    """Crear nuevo adulto mayor"""
    db_elderly_person = ElderlyPerson(
        user_id=elderly_person.user_id,
        first_name=elderly_person.first_name,
        last_name=elderly_person.last_name,
        age=elderly_person.age,
        address=elderly_person.address,
        emergency_contacts=elderly_person.emergency_contacts
    )
    db.add(db_elderly_person)
    db.commit()
    db.refresh(db_elderly_person)
    return db_elderly_person

def update_elderly_person(db: Session, elderly_person_id: UUID, elderly_person_update: ElderlyPersonUpdate) -> Optional[ElderlyPerson]:
    """Actualizar adulto mayor (permitir activo o inactivo, solo no eliminados)"""
    db_elderly_person = db.query(ElderlyPerson).filter(ElderlyPerson.id == elderly_person_id, ElderlyPerson.is_deleted == False).first()
    if not db_elderly_person:
        return None
    update_data = elderly_person_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_elderly_person, field, value)
    db.commit()
    db.refresh(db_elderly_person)
    return db_elderly_person

def delete_elderly_person(db: Session, elderly_person_id: UUID) -> bool:
    """Soft delete: marcar adulto mayor como eliminado (is_deleted = True)"""
    db_elderly_person = db.query(ElderlyPerson).filter(ElderlyPerson.id == elderly_person_id, ElderlyPerson.is_deleted == False).first()
    if not db_elderly_person:
        return False
    db_elderly_person.is_deleted = True
    db.commit()
    return True 