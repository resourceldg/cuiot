from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.cared_person_institution import CaredPersonInstitution
from app.models.cared_person import CaredPerson
from app.models.institution import Institution
from app.models.user import User
from app.schemas.cared_person_institution import CaredPersonInstitutionCreate, CaredPersonInstitutionUpdate
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class CaredPersonInstitutionService:
    """Service for managing cared person institution relationships"""
    
    @staticmethod
    def create_relationship(db: Session, relationship_data: CaredPersonInstitutionCreate, registered_by: UUID) -> CaredPersonInstitution:
        """Create a new cared person institution relationship"""
        db_relationship = CaredPersonInstitution(
            **relationship_data.model_dump(),
            registered_by=registered_by
        )
        
        # If this is marked as primary, unmark other primary relationships
        if relationship_data.is_primary:
            CaredPersonInstitutionService._unmark_other_primary(db, relationship_data.cared_person_id)
        
        db.add(db_relationship)
        db.commit()
        db.refresh(db_relationship)
        return db_relationship
    
    @staticmethod
    def get_relationship_by_id(db: Session, relationship_id: UUID) -> Optional[CaredPersonInstitution]:
        """Get relationship by ID"""
        return db.query(CaredPersonInstitution).filter(CaredPersonInstitution.id == relationship_id).first()
    
    @staticmethod
    def get_relationships_by_cared_person(db: Session, cared_person_id: UUID, skip: int = 0, limit: int = 100) -> List[CaredPersonInstitution]:
        """Get all relationships for a cared person"""
        return db.query(CaredPersonInstitution).filter(
            CaredPersonInstitution.cared_person_id == cared_person_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_relationships_by_institution(db: Session, institution_id: int, skip: int = 0, limit: int = 100) -> List[CaredPersonInstitution]:
        """Get all relationships for an institution"""
        return db.query(CaredPersonInstitution).filter(
            CaredPersonInstitution.institution_id == institution_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_active_relationships_by_cared_person(db: Session, cared_person_id: UUID) -> List[CaredPersonInstitution]:
        """Get active relationships for a cared person"""
        return db.query(CaredPersonInstitution).filter(
            CaredPersonInstitution.cared_person_id == cared_person_id,
            CaredPersonInstitution.status == "active"
        ).all()
    
    @staticmethod
    def get_active_relationships_by_institution(db: Session, institution_id: int) -> List[CaredPersonInstitution]:
        """Get active relationships for an institution"""
        return db.query(CaredPersonInstitution).filter(
            CaredPersonInstitution.institution_id == institution_id,
            CaredPersonInstitution.status == "active"
        ).all()
    
    @staticmethod
    def update_relationship(db: Session, relationship_id: UUID, relationship_data: CaredPersonInstitutionUpdate) -> Optional[CaredPersonInstitution]:
        """Update a relationship"""
        db_relationship = CaredPersonInstitutionService.get_relationship_by_id(db, relationship_id)
        if not db_relationship:
            return None
        
        # If this is being marked as primary, unmark others
        if relationship_data.is_primary:
            CaredPersonInstitutionService._unmark_other_primary(db, db_relationship.cared_person_id)
        
        for field, value in relationship_data.model_dump(exclude_unset=True).items():
            setattr(db_relationship, field, value)
        
        db.commit()
        db.refresh(db_relationship)
        return db_relationship
    
    @staticmethod
    def delete_relationship(db: Session, relationship_id: UUID) -> bool:
        """Delete a relationship"""
        db_relationship = CaredPersonInstitutionService.get_relationship_by_id(db, relationship_id)
        if not db_relationship:
            return False
        
        db.delete(db_relationship)
        db.commit()
        return True
    
    @staticmethod
    def get_relationship_with_details(db: Session, relationship_id: UUID) -> Optional[Dict[str, Any]]:
        """Get relationship with additional details"""
        db_relationship = db.query(CaredPersonInstitution).filter(CaredPersonInstitution.id == relationship_id).first()
        if not db_relationship:
            return None
        
        # Get related data
        cared_person = db.query(CaredPerson).filter(CaredPerson.id == db_relationship.cared_person_id).first()
        institution = db.query(Institution).filter(Institution.id == db_relationship.institution_id).first()
        registered_by_user = db.query(User).filter(User.id == db_relationship.registered_by).first() if db_relationship.registered_by else None
        
        return {
            "id": str(db_relationship.id),
            "cared_person_id": str(db_relationship.cared_person_id),
            "institution_id": db_relationship.institution_id,
            "service_type": db_relationship.service_type,
            "start_date": db_relationship.start_date,
            "end_date": db_relationship.end_date,
            "schedule": db_relationship.schedule,
            "frequency": db_relationship.frequency,
            "duration_hours": db_relationship.duration_hours,
            "cost_per_session": db_relationship.cost_per_session,
            "payment_frequency": db_relationship.payment_frequency,
            "insurance_coverage": db_relationship.insurance_coverage,
            "insurance_provider": db_relationship.insurance_provider,
            "primary_doctor": db_relationship.primary_doctor,
            "medical_notes": db_relationship.medical_notes,
            "treatment_plan": db_relationship.treatment_plan,
            "status": db_relationship.status,
            "is_primary": db_relationship.is_primary,
            "is_active": db_relationship.is_active,
            "total_cost": db_relationship.total_cost,
            "created_at": db_relationship.created_at,
            "cared_person_name": cared_person.full_name if cared_person else None,
            "institution_name": institution.name if institution else None,
            "registered_by_name": registered_by_user.full_name if registered_by_user else None
        }
    
    @staticmethod
    def get_summary_by_cared_person(db: Session, cared_person_id: UUID) -> Optional[Dict[str, Any]]:
        """Get summary of institution relationships for a cared person"""
        relationships = CaredPersonInstitutionService.get_active_relationships_by_cared_person(db, cared_person_id)
        
        if not relationships:
            return None
        
        total_services = len(relationships)
        active_services = sum(1 for r in relationships if r.is_active)
        total_cost = sum(r.total_cost for r in relationships)
        
        # Get primary institution
        primary_institution = None
        for r in relationships:
            if r.is_primary:
                institution = db.query(Institution).filter(Institution.id == r.institution_id).first()
                primary_institution = institution.name if institution else None
                break
        
        # Get service types
        service_types = list(set(r.service_type for r in relationships))
        
        return {
            "total_services": total_services,
            "active_services": active_services,
            "total_cost": total_cost,
            "primary_institution": primary_institution,
            "service_types": service_types
        }
    
    @staticmethod
    def get_summary_by_institution(db: Session, institution_id: int) -> Optional[Dict[str, Any]]:
        """Get summary of cared person relationships for an institution"""
        relationships = CaredPersonInstitutionService.get_active_relationships_by_institution(db, institution_id)
        
        if not relationships:
            return None
        
        total_patients = len(relationships)
        active_patients = sum(1 for r in relationships if r.is_active)
        total_revenue = sum(r.total_cost for r in relationships)
        
        # Get service types
        service_types = list(set(r.service_type for r in relationships))
        
        return {
            "total_patients": total_patients,
            "active_patients": active_patients,
            "total_revenue": total_revenue,
            "service_types": service_types
        }
    
    @staticmethod
    def search_relationships(db: Session, 
                           cared_person_id: Optional[UUID] = None,
                           institution_id: Optional[int] = None,
                           service_type: Optional[str] = None,
                           status: Optional[str] = None,
                           is_primary: Optional[bool] = None,
                           skip: int = 0, 
                           limit: int = 100) -> List[CaredPersonInstitution]:
        """Search relationships with filters"""
        query = db.query(CaredPersonInstitution)
        
        if cared_person_id:
            query = query.filter(CaredPersonInstitution.cared_person_id == cared_person_id)
        
        if institution_id:
            query = query.filter(CaredPersonInstitution.institution_id == institution_id)
        
        if service_type:
            query = query.filter(CaredPersonInstitution.service_type == service_type)
        
        if status:
            query = query.filter(CaredPersonInstitution.status == status)
        
        if is_primary is not None:
            query = query.filter(CaredPersonInstitution.is_primary == is_primary)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def _unmark_other_primary(db: Session, cared_person_id: UUID):
        """Unmark other primary relationships for a cared person"""
        db.query(CaredPersonInstitution).filter(
            CaredPersonInstitution.cared_person_id == cared_person_id,
            CaredPersonInstitution.is_primary == True
        ).update({"is_primary": False})
        db.commit()
