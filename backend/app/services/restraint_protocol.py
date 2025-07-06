from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID
import uuid
import os
import shutil

from app.models.restraint_protocol import RestraintProtocol
from app.schemas.restraint_protocol import RestraintProtocolCreate, RestraintProtocolUpdate, RestraintProtocolResponse, RestraintProtocolSummary
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.institution import Institution

class RestraintProtocolService:
    """Service for managing restraint protocols and incident prevention"""
    
    @staticmethod
    def create_restraint_protocol(
        db: Session, 
        protocol_data: RestraintProtocolCreate, 
        created_by: User,
        attached_files: List[Dict[str, Any]] = None
    ) -> RestraintProtocol:
        """Create a new restraint protocol"""
        
        # Validate cared person exists
        cared_person = db.query(CaredPerson).filter(CaredPerson.id == protocol_data.cared_person_id).first()
        if not cared_person:
            raise ValueError("Cared person not found")
        
        # Validate institution if provided
        if protocol_data.institution_id:
            institution = db.query(Institution).filter(Institution.id == protocol_data.institution_id).first()
            if not institution:
                raise ValueError("Institution not found")
        
        # Create protocol
        protocol = RestraintProtocol(
            **protocol_data.model_dump(exclude={'attached_files'}),
            created_by_id=created_by.id,
            attached_files=attached_files or []
        )
        
        db.add(protocol)
        db.commit()
        db.refresh(protocol)
        
        return protocol
    
    @staticmethod
    def get_restraint_protocol_by_id(db: Session, protocol_id: UUID) -> Optional[RestraintProtocol]:
        """Get restraint protocol by ID"""
        return db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
    
    @staticmethod
    def get_restraint_protocols(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        cared_person_id: Optional[UUID] = None,
        institution_id: Optional[int] = None,
        protocol_type: Optional[str] = None,
        status_type_id: Optional[int] = None,
        active_only: bool = False
    ) -> List[RestraintProtocol]:
        """Get restraint protocols with filters"""
        
        query = db.query(RestraintProtocol)
        
        if cared_person_id:
            query = query.filter(RestraintProtocol.cared_person_id == cared_person_id)
        
        if institution_id:
            query = query.filter(RestraintProtocol.institution_id == institution_id)
        
        if protocol_type:
            query = query.filter(RestraintProtocol.protocol_type == protocol_type)
        
        if status_type_id:
            query = query.filter(RestraintProtocol.status_type_id == status_type_id)
        
        if active_only:
            from app.services.status_type import StatusTypeService
            active_status = StatusTypeService.get_status_by_name(db, "active")
            if active_status:
                query = query.filter(RestraintProtocol.status_type_id == active_status.id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_active_restraint_protocols(db: Session, cared_person_id: Optional[UUID] = None) -> List[RestraintProtocol]:
        """Get active restraint protocols"""
        from app.services.status_type import StatusTypeService
        
        active_status = StatusTypeService.get_status_by_name(db, "active")
        if not active_status:
            return []
        
        query = db.query(RestraintProtocol).filter(RestraintProtocol.status_type_id == active_status.id)
        
        if cared_person_id:
            query = query.filter(RestraintProtocol.cared_person_id == cared_person_id)
        
        return query.all()
    
    @staticmethod
    def get_protocols_requiring_review(db: Session) -> List[RestraintProtocol]:
        """Get protocols that require review"""
        from app.services.status_type import StatusTypeService
        
        now = datetime.now()
        active_status = StatusTypeService.get_status_by_name(db, "active")
        if not active_status:
            return []
        
        return db.query(RestraintProtocol).filter(
            and_(
                RestraintProtocol.status_type_id == active_status.id,
                RestraintProtocol.next_review_date <= now
            )
        ).all()
    
    @staticmethod
    def update_restraint_protocol(
        db: Session, 
        protocol_id: UUID, 
        protocol_data: RestraintProtocolUpdate,
        updated_by: User,
        attached_files: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[RestraintProtocol]:
        """Update a restraint protocol"""
        
        protocol = db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
        if not protocol:
            return None
        
        # Update fields
        update_data = protocol_data.model_dump(exclude_unset=True, exclude={'attached_files'})
        for field, value in update_data.items():
            setattr(protocol, field, value)
        
        # Update attached files if provided
        if attached_files is not None:
            protocol.attached_files = attached_files
        
        # Update metadata
        protocol.updated_by_id = updated_by.id
        protocol.updated_at = datetime.now()
        
        db.commit()
        db.refresh(protocol)
        
        return protocol
    
    @staticmethod
    def delete_restraint_protocol(db: Session, protocol_id: UUID) -> bool:
        """Delete a restraint protocol"""
        protocol = db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
        if not protocol:
            return False
        
        db.delete(protocol)
        db.commit()
        
        return True
    
    @staticmethod
    def suspend_restraint_protocol(db: Session, protocol_id: UUID, updated_by: User, reason: str = None) -> Optional[RestraintProtocol]:
        """Suspend a restraint protocol"""
        from app.services.status_type import StatusTypeService
        
        protocol = db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
        if not protocol:
            return None
        
        suspended_status = StatusTypeService.get_status_by_name(db, "suspended")
        if suspended_status:
            protocol.status_type_id = suspended_status.id
        
        protocol.updated_by_id = updated_by.id
        protocol.updated_at = datetime.now()
        
        if reason:
            protocol.notes = f"{protocol.notes or ''}\n\nSUSPENDED: {reason}"
        
        db.commit()
        db.refresh(protocol)
        
        return protocol
    
    @staticmethod
    def complete_restraint_protocol(db: Session, protocol_id: UUID, updated_by: User, completion_notes: str = None) -> Optional[RestraintProtocol]:
        """Complete a restraint protocol"""
        from app.services.status_type import StatusTypeService
        
        protocol = db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
        if not protocol:
            return None
        
        completed_status = StatusTypeService.get_status_by_name(db, "completed")
        if completed_status:
            protocol.status_type_id = completed_status.id
        
        protocol.end_date = datetime.now()
        protocol.updated_by_id = updated_by.id
        protocol.updated_at = datetime.now()
        
        if completion_notes:
            protocol.notes = f"{protocol.notes or ''}\n\nCOMPLETED: {completion_notes}"
        
        db.commit()
        db.refresh(protocol)
        
        return protocol
    
    @staticmethod
    def update_compliance_status(
        db: Session, 
        protocol_id: UUID, 
        compliance_status: str,
        updated_by: User,
        compliance_notes: str = None
    ) -> Optional[RestraintProtocol]:
        """Update compliance status of a protocol"""
        
        allowed_statuses = ["compliant", "non_compliant", "under_review", "pending_assessment"]
        if compliance_status not in allowed_statuses:
            raise ValueError(f"compliance_status debe ser uno de: {allowed_statuses}")
        
        protocol = db.query(RestraintProtocol).filter(RestraintProtocol.id == protocol_id).first()
        if not protocol:
            return None
        
        protocol.compliance_status = compliance_status
        protocol.last_compliance_check = datetime.now()
        protocol.updated_by_id = updated_by.id
        protocol.updated_at = datetime.now()
        
        if compliance_notes:
            protocol.notes = f"{protocol.notes or ''}\n\nCOMPLIANCE UPDATE: {compliance_notes}"
        
        db.commit()
        db.refresh(protocol)
        
        return protocol
    
    @staticmethod
    def get_protocol_summary(db: Session, cared_person_id: Optional[UUID] = None) -> RestraintProtocolSummary:
        """Get summary statistics for restraint protocols"""
        from app.services.status_type import StatusTypeService
        
        query = db.query(RestraintProtocol)
        if cared_person_id:
            query = query.filter(RestraintProtocol.cared_person_id == cared_person_id)
        
        total_protocols = query.count()
        
        # Get active protocols
        active_status = StatusTypeService.get_status_by_name(db, "active")
        active_protocols = 0
        if active_status:
            active_protocols = query.filter(RestraintProtocol.status_type_id == active_status.id).count()
        
        # Protocols by type
        protocols_by_type = {}
        for protocol_type in RestraintProtocol.get_protocol_types():
            count = query.filter(RestraintProtocol.protocol_type == protocol_type).count()
            if count > 0:
                protocols_by_type[protocol_type] = count
        
        # Protocols by status (using status types)
        protocols_by_status = {}
        status_types = StatusTypeService.get_status_types(db)
        for status_type in status_types:
            count = query.filter(RestraintProtocol.status_type_id == status_type.id).count()
            if count > 0:
                protocols_by_status[status_type.name] = count
        
        # Protocols requiring review
        now = datetime.now()
        protocols_requiring_review = 0
        if active_status:
            protocols_requiring_review = query.filter(
                and_(
                    RestraintProtocol.status_type_id == active_status.id,
                    RestraintProtocol.next_review_date <= now
                )
            ).count()
        
        return RestraintProtocolSummary(
            total_protocols=total_protocols,
            active_protocols=active_protocols,
            protocols_by_type=protocols_by_type,
            protocols_by_status=protocols_by_status,
            protocols_requiring_review=protocols_requiring_review
        )
    
    @staticmethod
    def validate_protocol_data(protocol_data: RestraintProtocolCreate) -> bool:
        """Validate protocol data"""
        # Check if start_date is in the future
        if protocol_data.start_date < datetime.now():
            raise ValueError("start_date debe ser en el futuro")
        
        # Check if end_date is after start_date
        if protocol_data.end_date and protocol_data.end_date <= protocol_data.start_date:
            raise ValueError("end_date debe ser después de start_date")
        
        # Check if next_review_date is after start_date
        if protocol_data.next_review_date and protocol_data.next_review_date <= protocol_data.start_date:
            raise ValueError("next_review_date debe ser después de start_date")
        
        return True 