from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from uuid import UUID
from datetime import datetime, time

from app.models.reminder import Reminder
from app.models.cared_person import CaredPerson
from app.models.status_type import StatusType
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.core.exceptions import NotFoundException, ValidationException

class ReminderService:
    """Servicio para gestión de recordatorios del sistema"""
    
    @staticmethod
    def create_reminder(db: Session, reminder_data: ReminderCreate) -> Reminder:
        """
        Crear un nuevo recordatorio
        
        Args:
            db: Sesión de base de datos
            reminder_data: Datos del recordatorio a crear
            
        Returns:
            Reminder: Recordatorio creado
            
        Raises:
            NotFoundException: Si el adulto mayor no existe
        """
        # Verificar que la persona bajo cuidado existe
        cared_person = db.query(CaredPerson).filter(
            CaredPerson.id == reminder_data.cared_person_id
        ).first()
        
        if not cared_person:
            raise NotFoundException(f"Persona bajo cuidado con ID {reminder_data.cared_person_id} no encontrada")
        
        # Obtener el status_type_id por defecto (pending)
        default_status = db.query(StatusType).filter(StatusType.name == "pending").first()
        if not default_status:
            raise ValidationException("Status type 'pending' no encontrado en la base de datos")
        
        # Crear el recordatorio
        db_reminder = Reminder(
            cared_person_id=reminder_data.cared_person_id,
            user_id=reminder_data.user_id,
            title=reminder_data.title,
            description=reminder_data.description,
            reminder_type_id=reminder_data.reminder_type_id,
            scheduled_time=reminder_data.scheduled_time,
            due_date=reminder_data.due_date,
            repeat_pattern=reminder_data.repeat_pattern,
            status_type_id=reminder_data.status_type_id or default_status.id,
            priority=reminder_data.priority,
            is_important=reminder_data.is_important,
            reminder_data=reminder_data.reminder_data,
            notes=reminder_data.notes
        )
        
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)
        
        return db_reminder
    
    @staticmethod
    def get_reminder(db: Session, reminder_id: UUID) -> Optional[Reminder]:
        """
        Obtener un recordatorio por ID
        
        Args:
            db: Sesión de base de datos
            reminder_id: ID del recordatorio
            
        Returns:
            Reminder: Recordatorio encontrado o None
        """
        return db.query(Reminder).filter(Reminder.id == reminder_id).first()
    
    @staticmethod
    def get_reminders(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        cared_person_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        reminder_type_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        status_type_id: Optional[int] = None
    ) -> tuple[List[Reminder], int]:
        """
        Obtener lista de recordatorios con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            cared_person_id: Filtrar por adulto mayor
            reminder_type_id: Filtrar por tipo de recordatorio
            is_active: Filtrar por estado activo
            user_id: Filtrar por usuario creador
            status_type_id: Filtrar por tipo de status
            
        Returns:
            tuple: (lista de recordatorios, total de registros)
        """
        query = db.query(Reminder)
        
        # Aplicar filtros
        if cared_person_id:
            query = query.filter(Reminder.cared_person_id == cared_person_id)
        
        if user_id:
            query = query.filter(Reminder.user_id == user_id)
        
        if reminder_type_id:
            query = query.filter(Reminder.reminder_type_id == reminder_type_id)
        
        if is_active is not None:
            query = query.filter(Reminder.is_active == is_active)
        
        if status_type_id:
            query = query.filter(Reminder.status_type_id == status_type_id)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        reminders = query.order_by(desc(Reminder.created_at)).offset(skip).limit(limit).all()
        
        return reminders, total
    
    @staticmethod
    def get_reminders_by_cared_person(
        db: Session, 
        cared_person_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Reminder], int]:
        """
        Obtener recordatorios de un adulto mayor específico
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: ID del adulto mayor
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de recordatorios, total de registros)
        """
        return ReminderService.get_reminders(
            db=db,
            skip=skip,
            limit=limit,
            cared_person_id=cared_person_id
        )
    
    @staticmethod
    def get_reminders_by_user(
        db: Session, 
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Reminder], int]:
        """
        Obtener recordatorios por usuario (creados o recibidos)
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            created_only: Solo recordatorios creados por el usuario
            received_only: Solo recordatorios recibidos por el usuario
            
        Returns:
            tuple: (lista de recordatorios, total de registros)
        """
        query = db.query(Reminder).filter(Reminder.user_id == user_id)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        reminders = query.order_by(desc(Reminder.created_at)).offset(skip).limit(limit).all()
        
        return reminders, total
    
    @staticmethod
    def update_reminder(db: Session, reminder_id: UUID, reminder_data: ReminderUpdate) -> Optional[Reminder]:
        """
        Actualizar un recordatorio
        
        Args:
            db: Sesión de base de datos
            reminder_id: ID del recordatorio
            reminder_data: Datos a actualizar
            
        Returns:
            Reminder: Recordatorio actualizado o None si no existe
        """
        db_reminder = ReminderService.get_reminder(db, reminder_id)
        
        if not db_reminder:
            return None
        
        # Actualizar campos
        update_data = reminder_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_reminder, field, value)
        
        db.commit()
        db.refresh(db_reminder)
        
        return db_reminder
    
    @staticmethod
    def delete_reminder(db: Session, reminder_id: UUID) -> bool:
        """
        Eliminar un recordatorio
        
        Args:
            db: Sesión de base de datos
            reminder_id: ID del recordatorio
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        db_reminder = ReminderService.get_reminder(db, reminder_id)
        
        if not db_reminder:
            return False
        
        db.delete(db_reminder)
        db.commit()
        
        return True
    
    @staticmethod
    def activate_reminder(db: Session, reminder_id: UUID) -> Optional[Reminder]:
        """
        Activar un recordatorio
        
        Args:
            db: Sesión de base de datos
            reminder_id: ID del recordatorio
            
        Returns:
            Reminder: Recordatorio actualizado o None si no existe
        """
        return ReminderService.update_reminder(
            db=db,
            reminder_id=reminder_id,
            reminder_data=ReminderUpdate(is_active=True)
        )
    
    @staticmethod
    def deactivate_reminder(db: Session, reminder_id: UUID) -> Optional[Reminder]:
        """
        Desactivar un recordatorio
        
        Args:
            db: Sesión de base de datos
            reminder_id: ID del recordatorio
            
        Returns:
            Reminder: Recordatorio actualizado o None si no existe
        """
        return ReminderService.update_reminder(
            db=db,
            reminder_id=reminder_id,
            reminder_data=ReminderUpdate(is_active=False)
        )
    
    @staticmethod
    def get_active_reminders(db: Session, cared_person_id: Optional[UUID] = None) -> List[Reminder]:
        """
        Obtener recordatorios activos
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: Filtrar por adulto mayor (opcional)
            
        Returns:
            List[Reminder]: Lista de recordatorios activos
        """
        reminders, _ = ReminderService.get_reminders(
            db=db,
            cared_person_id=cared_person_id,
            is_active=True
        )
        return reminders
    
    @staticmethod
    def get_reminders_by_type(
        db: Session, 
        reminder_type: str, 
        cared_person_id: Optional[UUID] = None
    ) -> List[Reminder]:
        """
        Obtener recordatorios por tipo
        
        Args:
            db: Sesión de base de datos
            reminder_type: Tipo de recordatorio
            elderly_person_id: Filtrar por adulto mayor (opcional)
            
        Returns:
            List[Reminder]: Lista de recordatorios del tipo especificado
        """
        reminders, _ = ReminderService.get_reminders(
            db=db,
            cared_person_id=cared_person_id,
            reminder_type_id=reminder_type
        )
        return reminders
    
    @staticmethod
    def get_medication_reminders(db: Session, cared_person_id: Optional[UUID] = None) -> List[Reminder]:
        """
        Obtener recordatorios de medicación
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: Filtrar por adulto mayor (opcional)
            
        Returns:
            List[Reminder]: Lista de recordatorios de medicación
        """
        return ReminderService.get_reminders_by_type(
            db=db,
            reminder_type_id="medication",
            cared_person_id=cared_person_id
        ) 