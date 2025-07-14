"""
Catálogos básicos: status_types, relationship_types, care_types, etc.
"""
from app.models.status_type import StatusType
from app.models.relationship_type import RelationshipType
from app.models.care_type import CareType
from sqlalchemy.orm import Session
from datetime import datetime

def get_or_create_status_type(db: Session, name: str, category: str = None):
    obj = db.query(StatusType).filter_by(name=name).first()
    if obj:
        return obj
    obj = StatusType(name=name, category=category, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_or_create_relationship_type(db: Session, name: str, description: str = None):
    obj = db.query(RelationshipType).filter_by(name=name).first()
    if obj:
        return obj
    obj = RelationshipType(name=name, description=description, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_or_create_care_type(db: Session, name: str, description: str = None):
    obj = db.query(CareType).filter_by(name=name).first()
    if obj:
        return obj
    obj = CareType(name=name, description=description, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def populate_catalog_types(db: Session):
    print("🌱 Poblando catálogos básicos...")
    # Status Types
    for name in ["active", "inactive", "suspended", "terminated", "pending", "on_leave"]:
        get_or_create_status_type(db, name)
    # Relationship Types
    for name in ["employee", "contractor", "volunteer", "intern", "consultant", "temporary"]:
        get_or_create_relationship_type(db, name)
    # Care Types
    for name in ["self_care", "delegated_care", "institutional_care", "family_care", "private_care", "public_care"]:
        get_or_create_care_type(db, name)
    print("✅ Catálogos básicos listos.") 