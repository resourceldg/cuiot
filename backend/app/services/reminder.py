from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from uuid import UUID
from datetime import datetime, time

from app.models.reminder import Reminder
from app.models.elderly_person import ElderlyPerson
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
        # Verificar que el adulto mayor existe
        elderly_person = db.query(ElderlyPerson).filter(
            ElderlyPerson.id == reminder_data.elderly_person_id
        ).first()
        
        if not elderly_person:
            raise NotFoundException(f"Adulto mayor con ID {reminder_data.elderly_person_id} no encontrado")
        
        # Crear el recordatorio
        db_reminder = Reminder(
            elderly_person_id=reminder_data.elderly_person_id,
            title=reminder_data.title,
            description=reminder_data.description,
            reminder_type=reminder_data.reminder_type,
            scheduled_time=reminder_data.scheduled_time,
            days_of_week=reminder_data.days_of_week,
            created_by_id=reminder_data.created_by_id,
            received_by_id=reminder_data.received_by_id
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
        elderly_person_id: Optional[UUID] = None,
        reminder_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        created_by_id: Optional[UUID] = None,
        received_by_id: Optional[UUID] = None
    ) -> tuple[List[Reminder], int]:
        """
        Obtener lista de recordatorios con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            elderly_person_id: Filtrar por adulto mayor
            reminder_type: Filtrar por tipo de recordatorio
            is_active: Filtrar por estado activo
            created_by_id: Filtrar por usuario creador
            received_by_id: Filtrar por usuario receptor
            
        Returns:
            tuple: (lista de recordatorios, total de registros)
        """
        query = db.query(Reminder)
        
        # Aplicar filtros
        if elderly_person_id:
            query = query.filter(Reminder.elderly_person_id == elderly_person_id)
        
        if reminder_type:
            query = query.filter(Reminder.reminder_type == reminder_type)
        
        if is_active is not None:
            query = query.filter(Reminder.is_active == is_active)
        
        if created_by_id:
            query = query.filter(Reminder.created_by_id == created_by_id)
        
        if received_by_id:
            query = query.filter(Reminder.received_by_id == received_by_id)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        reminders = query.order_by(desc(Reminder.created_at)).offset(skip).limit(limit).all()
        
        return reminders, total
    
    @staticmethod
    def get_reminders_by_elderly_person(
        db: Session, 
        elderly_person_id: UUID,
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
            elderly_person_id=elderly_person_id
        )
    
    @staticmethod
    def get_reminders_by_user(
        db: Session, 
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        created_only: bool = False,
        received_only: bool = False
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
        query = db.query(Reminder)
        
        if created_only:
            query = query.filter(Reminder.created_by_id == user_id)
        elif received_only:
            query = query.filter(Reminder.received_by_id == user_id)
        else:
            # Ambos: creados o recibidos
            query = query.filter(
                (Reminder.created_by_id == user_id) | (Reminder.received_by_id == user_id)
            )
        
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
        update_data = reminder_data.dict(exclude_unset=True)
        
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
    def get_active_reminders(db: Session, elderly_person_id: Optional[UUID] = None) -> List[Reminder]:
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
            elderly_person_id=elderly_person_id,
            is_active=True
        )
        return reminders
    
    @staticmethod
    def get_reminders_by_type(
        db: Session, 
        reminder_type: str, 
        elderly_person_id: Optional[UUID] = None
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
            elderly_person_id=elderly_person_id,
            reminder_type=reminder_type
        )
        return reminders
    
    @staticmethod
    def get_medication_reminders(db: Session, elderly_person_id: Optional[UUID] = None) -> List[Reminder]:
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
            reminder_type="medication",
            elderly_person_id=elderly_person_id
        ) 