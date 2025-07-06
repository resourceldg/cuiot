from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.models.service_subscription import ServiceSubscription
from app.models.user import User
from app.models.institution import Institution
from app.models.status_type import StatusType
from app.schemas.service_subscription import ServiceSubscriptionCreate, ServiceSubscriptionUpdate
from app.core.exceptions import NotFoundException, ValidationException

class ServiceSubscriptionService:
    """Servicio para gestión de suscripciones de servicios"""
    
    @staticmethod
    def create_subscription(db: Session, subscription_data: ServiceSubscriptionCreate) -> ServiceSubscription:
        """
        Crear una nueva suscripción de servicio
        
        Args:
            db: Sesión de base de datos
            subscription_data: Datos de la suscripción a crear
            
        Returns:
            ServiceSubscription: Suscripción creada
            
        Raises:
            NotFoundException: Si el usuario o institución no existe
            ValidationException: Si el status type no existe
        """
        # Verificar que el usuario existe si se proporciona
        if subscription_data.user_id:
            user = db.query(User).filter(User.id == subscription_data.user_id).first()
            if not user:
                raise NotFoundException(f"Usuario con ID {subscription_data.user_id} no encontrado")
        
        # Verificar que la institución existe si se proporciona
        if subscription_data.institution_id:
            institution = db.query(Institution).filter(Institution.id == subscription_data.institution_id).first()
            if not institution:
                raise NotFoundException(f"Institución con ID {subscription_data.institution_id} no encontrada")
        
        # Obtener el status_type_id por defecto (active)
        default_status = db.query(StatusType).filter(StatusType.name == "active").first()
        if not default_status:
            raise ValidationException("Status type 'active' no encontrado en la base de datos")
        
        # Crear la suscripción
        db_subscription = ServiceSubscription(
            subscription_type=subscription_data.subscription_type,
            service_name=subscription_data.service_name,
            description=subscription_data.description,
            features=subscription_data.features,
            limitations=subscription_data.limitations,
            price_per_month=subscription_data.price_per_month,
            price_per_year=subscription_data.price_per_year,
            currency=subscription_data.currency,
            start_date=subscription_data.start_date,
            end_date=subscription_data.end_date,
            auto_renew=subscription_data.auto_renew,
            status_type_id=subscription_data.status_type_id or default_status.id,
            user_id=subscription_data.user_id,
            institution_id=subscription_data.institution_id
        )
        
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        
        return db_subscription
    
    @staticmethod
    def get_subscription(db: Session, subscription_id: int) -> Optional[ServiceSubscription]:
        """
        Obtener una suscripción por ID
        
        Args:
            db: Sesión de base de datos
            subscription_id: ID de la suscripción
            
        Returns:
            ServiceSubscription: Suscripción encontrada o None
        """
        return db.query(ServiceSubscription).filter(ServiceSubscription.id == subscription_id).first()
    
    @staticmethod
    def get_subscriptions(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[UUID] = None,
        institution_id: Optional[int] = None,
        subscription_type: Optional[str] = None,
        service_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        status_type_id: Optional[int] = None
    ) -> tuple[List[ServiceSubscription], int]:
        """
        Obtener lista de suscripciones con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            user_id: Filtrar por usuario
            institution_id: Filtrar por institución
            subscription_type: Filtrar por tipo de suscripción
            service_name: Filtrar por nombre del servicio
            is_active: Filtrar por estado activo
            status_type_id: Filtrar por tipo de status
            
        Returns:
            tuple: (lista de suscripciones, total de registros)
        """
        query = db.query(ServiceSubscription)
        
        # Aplicar filtros
        if user_id:
            query = query.filter(ServiceSubscription.user_id == user_id)
        
        if institution_id:
            query = query.filter(ServiceSubscription.institution_id == institution_id)
        
        if subscription_type:
            query = query.filter(ServiceSubscription.subscription_type == subscription_type)
        
        if service_name:
            query = query.filter(ServiceSubscription.service_name == service_name)
        
        if is_active is not None:
            query = query.filter(ServiceSubscription.is_active == is_active)
        
        if status_type_id:
            query = query.filter(ServiceSubscription.status_type_id == status_type_id)
        
        # Obtener total antes de aplicar paginación
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        subscriptions = query.order_by(desc(ServiceSubscription.created_at)).offset(skip).limit(limit).all()
        
        return subscriptions, total
    
    @staticmethod
    def get_subscriptions_by_user(
        db: Session, 
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[ServiceSubscription], int]:
        """
        Obtener suscripciones de un usuario específico
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de suscripciones, total de registros)
        """
        return ServiceSubscriptionService.get_subscriptions(
            db=db,
            skip=skip,
            limit=limit,
            user_id=user_id
        )
    
    @staticmethod
    def get_subscriptions_by_institution(
        db: Session, 
        institution_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[ServiceSubscription], int]:
        """
        Obtener suscripciones de una institución específica
        
        Args:
            db: Sesión de base de datos
            institution_id: ID de la institución
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            tuple: (lista de suscripciones, total de registros)
        """
        return ServiceSubscriptionService.get_subscriptions(
            db=db,
            skip=skip,
            limit=limit,
            institution_id=institution_id
        )
    
    @staticmethod
    def update_subscription(db: Session, subscription_id: int, subscription_data: ServiceSubscriptionUpdate) -> Optional[ServiceSubscription]:
        """
        Actualizar una suscripción
        
        Args:
            db: Sesión de base de datos
            subscription_id: ID de la suscripción
            subscription_data: Datos a actualizar
            
        Returns:
            ServiceSubscription: Suscripción actualizada o None si no existe
        """
        db_subscription = ServiceSubscriptionService.get_subscription(db, subscription_id)
        
        if not db_subscription:
            return None
        
        # Actualizar campos
        update_data = subscription_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_subscription, field, value)
        
        db.commit()
        db.refresh(db_subscription)
        
        return db_subscription
    
    @staticmethod
    def delete_subscription(db: Session, subscription_id: int) -> bool:
        """
        Eliminar una suscripción
        
        Args:
            db: Sesión de base de datos
            subscription_id: ID de la suscripción
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        db_subscription = ServiceSubscriptionService.get_subscription(db, subscription_id)
        
        if not db_subscription:
            return False
        
        db.delete(db_subscription)
        db.commit()
        
        return True
    
    @staticmethod
    def get_active_subscriptions(db: Session, user_id: Optional[UUID] = None, institution_id: Optional[int] = None) -> List[ServiceSubscription]:
        """
        Obtener suscripciones activas
        
        Args:
            db: Sesión de base de datos
            user_id: Filtrar por usuario (opcional)
            institution_id: Filtrar por institución (opcional)
            
        Returns:
            List[ServiceSubscription]: Lista de suscripciones activas
        """
        subscriptions, _ = ServiceSubscriptionService.get_subscriptions(
            db=db,
            user_id=user_id,
            institution_id=institution_id,
            is_active=True
        )
        return subscriptions
    
    @staticmethod
    def get_subscriptions_by_type(
        db: Session, 
        subscription_type: str,
        user_id: Optional[UUID] = None,
        institution_id: Optional[int] = None
    ) -> List[ServiceSubscription]:
        """
        Obtener suscripciones por tipo
        
        Args:
            db: Sesión de base de datos
            subscription_type: Tipo de suscripción
            user_id: Filtrar por usuario (opcional)
            institution_id: Filtrar por institución (opcional)
            
        Returns:
            List[ServiceSubscription]: Lista de suscripciones del tipo especificado
        """
        subscriptions, _ = ServiceSubscriptionService.get_subscriptions(
            db=db,
            user_id=user_id,
            institution_id=institution_id,
            subscription_type=subscription_type
        )
        return subscriptions 