from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.models.alert import Alert
from app.models.elderly_person import ElderlyPerson
from app.schemas.alert import AlertCreate, AlertUpdate
from app.core.exceptions import NotFoundException, ValidationException

class AlertService:
    """Servicio para gestión de alertas del sistema"""
    
    @staticmethod
    def create_alert(db: Session, alert_data: AlertCreate) -> Alert:
        """
        Crear una nueva alerta
        
        Args:
            db: Sesión de base de datos
            alert_data: Datos de la alerta a crear
            
        Returns:
            Alert: Alerta creada
            
        Raises:
            NotFoundException: Si el adulto mayor no existe
        """
        # Verificar que el adulto mayor existe
        elderly_person = db.query(ElderlyPerson).filter(
            ElderlyPerson.id == alert_data.elderly_person_id
        ).first()
        
        if not elderly_person:
            raise NotFoundException(f"Adulto mayor con ID {alert_data.elderly_person_id} no encontrado")
        
        # Crear la alerta
        db_alert = Alert(
            elderly_person_id=alert_data.elderly_person_id,
            alert_type=alert_data.alert_type,
            message=alert_data.message,
            severity=alert_data.severity,
            created_by_id=alert_data.created_by_id,
            received_by_id=alert_data.received_by_id
        )
        
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        
        return db_alert
    
    @staticmethod
    def get_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
        """
        Obtener una alerta por ID
        
        Args:
            db: Sesión de base de datos
            alert_id: ID de la alerta
            
        Returns:
            Alert: Alerta encontrada o None
        """
        return db.query(Alert).filter(Alert.id == alert_id).first()
    
    @staticmethod
    def get_alerts(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        elderly_person_id: Optional[UUID] = None,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None,
        is_resolved: Optional[bool] = None,
        created_by_id: Optional[UUID] = None,
        received_by_id: Optional[UUID] = None
    ) -> tuple[List[Alert], int]:
        """
        Obtener lista de alertas con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            elderly_person_id: Filtrar por adulto mayor
            alert_type: Filtrar por tipo de alerta
            severity: Filtrar por severidad
            is_resolved: Filtrar por estado de resolución
            created_by_id: Filtrar por usuario creador
            received_by_id: Filtrar por usuario receptor
            
        Returns:
            tuple: (lista de alertas, total de registros)
        """
        query = db.query(Alert)
        
        # Aplicar filtros
        if elderly_person_id:
            query = query.filter(Alert.elderly_person_id == elderly_person_id)
        
        if alert_type:
            query = query.filter(Alert.alert_type == alert_type)
        
        if severity:
            query = query.filter(Alert.severity == severity)
        
        if is_resolved is not None:
            query = query.filter(Alert.is_resolved == is_resolved)
        
        if created_by_id:
            query = query.filter(Alert.created_by_id == created_by_id)
        
        if received_by_id:
            query = query.filter(Alert.received_by_id == received_by_id)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        alerts = query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
        
        return alerts, total
    
    @staticmethod
    def get_alerts_by_user(
        db: Session, 
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        created_only: bool = False,
        received_only: bool = False
    ) -> tuple[List[Alert], int]:
        """
        Obtener alertas por usuario (creadas o recibidas)
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            created_only: Solo alertas creadas por el usuario
            received_only: Solo alertas recibidas por el usuario
            
        Returns:
            tuple: (lista de alertas, total de registros)
        """
        query = db.query(Alert)
        
        if created_only:
            query = query.filter(Alert.created_by_id == user_id)
        elif received_only:
            query = query.filter(Alert.received_by_id == user_id)
        else:
            # Ambos: creadas o recibidas
            query = query.filter(
                (Alert.created_by_id == user_id) | (Alert.received_by_id == user_id)
            )
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        alerts = query.order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
        
        return alerts, total
    
    @staticmethod
    def get_alerts_by_elderly_person(
        db: Session, 
        elderly_person_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Alert], int]:
        """
        Obtener alertas de un adulto mayor específico
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: ID del adulto mayor
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de alertas, total de registros)
        """
        return AlertService.get_alerts(
            db=db,
            skip=skip,
            limit=limit,
            elderly_person_id=elderly_person_id
        )
    
    @staticmethod
    def update_alert(db: Session, alert_id: UUID, alert_data: AlertUpdate) -> Optional[Alert]:
        """
        Actualizar una alerta
        
        Args:
            db: Sesión de base de datos
            alert_id: ID de la alerta
            alert_data: Datos a actualizar
            
        Returns:
            Alert: Alerta actualizada o None si no existe
        """
        db_alert = AlertService.get_alert(db, alert_id)
        
        if not db_alert:
            return None
        
        # Actualizar campos
        update_data = alert_data.dict(exclude_unset=True)
        
        # Si se marca como resuelta, establecer timestamp
        if update_data.get('is_resolved') and not db_alert.is_resolved:
            update_data['resolved_at'] = datetime.utcnow()
        
        for field, value in update_data.items():
            setattr(db_alert, field, value)
        
        db.commit()
        db.refresh(db_alert)
        
        return db_alert
    
    @staticmethod
    def delete_alert(db: Session, alert_id: UUID) -> bool:
        """
        Eliminar una alerta
        
        Args:
            db: Sesión de base de datos
            alert_id: ID de la alerta
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        db_alert = AlertService.get_alert(db, alert_id)
        
        if not db_alert:
            return False
        
        db.delete(db_alert)
        db.commit()
        
        return True
    
    @staticmethod
    def resolve_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
        """
        Marcar una alerta como resuelta
        
        Args:
            db: Sesión de base de datos
            alert_id: ID de la alerta
            
        Returns:
            Alert: Alerta resuelta o None si no existe
        """
        db_alert = AlertService.get_alert(db, alert_id)
        
        if not db_alert:
            return None
        
        db_alert.is_resolved = True
        db_alert.resolved_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_alert)
        
        return db_alert
    
    @staticmethod
    def get_unresolved_alerts(db: Session, elderly_person_id: Optional[UUID] = None) -> List[Alert]:
        """
        Obtener alertas no resueltas
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: Filtrar por adulto mayor (opcional)
            
        Returns:
            List[Alert]: Lista de alertas no resueltas
        """
        query = db.query(Alert).filter(Alert.is_resolved == False)
        
        if elderly_person_id:
            query = query.filter(Alert.elderly_person_id == elderly_person_id)
        
        return query.order_by(desc(Alert.created_at)).all()
    
    @staticmethod
    def get_critical_alerts(db: Session, elderly_person_id: Optional[UUID] = None) -> List[Alert]:
        """
        Obtener alertas críticas (severidad 'critical')
        
        Args:
            db: Sesión de base de datos
            elderly_person_id: Filtrar por adulto mayor (opcional)
            
        Returns:
            List[Alert]: Lista de alertas críticas
        """
        query = db.query(Alert).filter(Alert.severity == 'critical')
        
        if elderly_person_id:
            query = query.filter(Alert.elderly_person_id == elderly_person_id)
        
        return query.order_by(desc(Alert.created_at)).all() 