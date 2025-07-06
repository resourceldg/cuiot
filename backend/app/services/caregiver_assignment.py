from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.models.caregiver_assignment import CaregiverAssignment
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.status_type import StatusType
from app.schemas.caregiver_assignment import CaregiverAssignmentCreate, CaregiverAssignmentUpdate
from app.core.exceptions import NotFoundException, ValidationException

class CaregiverAssignmentService:
    """Servicio para gestión de asignaciones de cuidadores"""
    
    @staticmethod
    def create_assignment(db: Session, assignment_data: CaregiverAssignmentCreate) -> CaregiverAssignment:
        """
        Crear una nueva asignación de cuidador
        
        Args:
            db: Sesión de base de datos
            assignment_data: Datos de la asignación a crear
            
        Returns:
            CaregiverAssignment: Asignación creada
            
        Raises:
            NotFoundException: Si el cuidador o persona bajo cuidado no existe
            ValidationException: Si el status type no existe
        """
        # Verificar que el cuidador existe
        caregiver = db.query(User).filter(User.id == assignment_data.caregiver_id).first()
        if not caregiver:
            raise NotFoundException(f"Cuidador con ID {assignment_data.caregiver_id} no encontrado")
        
        # Verificar que la persona bajo cuidado existe
        cared_person = db.query(CaredPerson).filter(CaredPerson.id == assignment_data.cared_person_id).first()
        if not cared_person:
            raise NotFoundException(f"Persona bajo cuidado con ID {assignment_data.cared_person_id} no encontrada")
        
        # Obtener el status_type_id por defecto (active)
        default_status = db.query(StatusType).filter(StatusType.name == "active").first()
        if not default_status:
            raise ValidationException("Status type 'active' no encontrado en la base de datos")
        
        # Crear la asignación
        db_assignment = CaregiverAssignment(
            caregiver_id=assignment_data.caregiver_id,
            cared_person_id=assignment_data.cared_person_id,
            start_date=assignment_data.start_date,
            end_date=assignment_data.end_date,
            schedule=assignment_data.schedule,
            assignment_type=assignment_data.assignment_type,
            responsibilities=assignment_data.responsibilities,
            special_requirements=assignment_data.special_requirements,
            hourly_rate=assignment_data.hourly_rate,
            payment_frequency=assignment_data.payment_frequency,
            is_insured=assignment_data.is_insured,
            insurance_provider=assignment_data.insurance_provider,
            client_rating=assignment_data.client_rating,
            client_feedback=assignment_data.client_feedback,
            caregiver_self_rating=assignment_data.caregiver_self_rating,
            caregiver_notes=assignment_data.caregiver_notes,
            primary_doctor=assignment_data.primary_doctor,
            medical_contact=assignment_data.medical_contact,
            emergency_protocol=assignment_data.emergency_protocol,
            status_type_id=assignment_data.status_type_id or default_status.id,
            is_primary=assignment_data.is_primary,
            assigned_by=assignment_data.assigned_by,
            notes=assignment_data.notes
        )
        
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        
        return db_assignment
    
    @staticmethod
    def get_assignment(db: Session, assignment_id: int) -> Optional[CaregiverAssignment]:
        """
        Obtener una asignación por ID
        
        Args:
            db: Sesión de base de datos
            assignment_id: ID de la asignación
            
        Returns:
            CaregiverAssignment: Asignación encontrada o None
        """
        return db.query(CaregiverAssignment).filter(CaregiverAssignment.id == assignment_id).first()
    
    @staticmethod
    def get_assignments(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        caregiver_id: Optional[UUID] = None,
        cared_person_id: Optional[UUID] = None,
        assignment_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        status_type_id: Optional[int] = None,
        is_primary: Optional[bool] = None
    ) -> tuple[List[CaregiverAssignment], int]:
        """
        Obtener lista de asignaciones con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            caregiver_id: Filtrar por cuidador
            cared_person_id: Filtrar por persona bajo cuidado
            assignment_type: Filtrar por tipo de asignación
            is_active: Filtrar por estado activo
            status_type_id: Filtrar por tipo de status
            is_primary: Filtrar por asignación primaria
            
        Returns:
            tuple: (lista de asignaciones, total de registros)
        """
        query = db.query(CaregiverAssignment)
        
        # Aplicar filtros
        if caregiver_id:
            query = query.filter(CaregiverAssignment.caregiver_id == caregiver_id)
        
        if cared_person_id:
            query = query.filter(CaregiverAssignment.cared_person_id == cared_person_id)
        
        if assignment_type:
            query = query.filter(CaregiverAssignment.assignment_type == assignment_type)
        
        if is_active is not None:
            query = query.filter(CaregiverAssignment.is_active == is_active)
        
        if status_type_id:
            query = query.filter(CaregiverAssignment.status_type_id == status_type_id)
        
        if is_primary is not None:
            query = query.filter(CaregiverAssignment.is_primary == is_primary)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        assignments = query.order_by(desc(CaregiverAssignment.created_at)).offset(skip).limit(limit).all()
        
        return assignments, total
    
    @staticmethod
    def get_assignments_by_caregiver(
        db: Session, 
        caregiver_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[CaregiverAssignment], int]:
        """
        Obtener asignaciones de un cuidador específico
        
        Args:
            db: Sesión de base de datos
            caregiver_id: ID del cuidador
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de asignaciones, total de registros)
        """
        return CaregiverAssignmentService.get_assignments(
            db=db,
            skip=skip,
            limit=limit,
            caregiver_id=caregiver_id
        )
    
    @staticmethod
    def get_assignments_by_cared_person(
        db: Session, 
        cared_person_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[CaregiverAssignment], int]:
        """
        Obtener asignaciones de una persona bajo cuidado específica
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de asignaciones, total de registros)
        """
        return CaregiverAssignmentService.get_assignments(
            db=db,
            skip=skip,
            limit=limit,
            cared_person_id=cared_person_id
        )
    
    @staticmethod
    def update_assignment(db: Session, assignment_id: int, assignment_data: CaregiverAssignmentUpdate) -> Optional[CaregiverAssignment]:
        """
        Actualizar una asignación
        
        Args:
            db: Sesión de base de datos
            assignment_id: ID de la asignación
            assignment_data: Datos a actualizar
            
        Returns:
            CaregiverAssignment: Asignación actualizada o None si no existe
        """
        db_assignment = CaregiverAssignmentService.get_assignment(db, assignment_id)
        
        if not db_assignment:
            return None
        
        # Actualizar campos
        update_data = assignment_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_assignment, field, value)
        
        db.commit()
        db.refresh(db_assignment)
        
        return db_assignment
    
    @staticmethod
    def delete_assignment(db: Session, assignment_id: int) -> bool:
        """
        Eliminar una asignación
        
        Args:
            db: Sesión de base de datos
            assignment_id: ID de la asignación
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        db_assignment = CaregiverAssignmentService.get_assignment(db, assignment_id)
        
        if not db_assignment:
            return False
        
        db.delete(db_assignment)
        db.commit()
        
        return True
    
    @staticmethod
    def get_active_assignments(db: Session, cared_person_id: Optional[UUID] = None) -> List[CaregiverAssignment]:
        """
        Obtener asignaciones activas
        
        Args:
            db: Sesión de base de datos
            cared_person_id: Filtrar por persona bajo cuidado (opcional)
            
        Returns:
            List[CaregiverAssignment]: Lista de asignaciones activas
        """
        assignments, _ = CaregiverAssignmentService.get_assignments(
            db=db,
            cared_person_id=cared_person_id,
            is_active=True
        )
        return assignments
    
    @staticmethod
    def get_primary_caregiver(db: Session, cared_person_id: UUID) -> Optional[CaregiverAssignment]:
        """
        Obtener el cuidador primario de una persona
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            CaregiverAssignment: Asignación del cuidador primario o None
        """
        return db.query(CaregiverAssignment).filter(
            and_(
                CaregiverAssignment.cared_person_id == cared_person_id,
                CaregiverAssignment.is_primary == True,
                CaregiverAssignment.is_active == True
            )
        ).first() 