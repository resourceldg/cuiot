from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.status_type import StatusType
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate


class StatusTypeService:
    """Servicio para gestionar tipos de estado"""
    
    @staticmethod
    def create_status_type(db: Session, status_type: StatusTypeCreate) -> StatusType:
        """Crear un nuevo tipo de estado"""
        db_status_type = StatusType(**status_type.model_dump())
        db.add(db_status_type)
        db.commit()
        db.refresh(db_status_type)
        return db_status_type
    
    @staticmethod
    def get_status_type(db: Session, status_type_id: int) -> Optional[StatusType]:
        """Obtener un tipo de estado por ID"""
        return db.query(StatusType).filter(StatusType.id == status_type_id).first()
    
    @staticmethod
    def get_status_types(db: Session, skip: int = 0, limit: int = 100) -> List[StatusType]:
        """Obtener lista de tipos de estado"""
        return db.query(StatusType).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_status_types_by_category(db: Session, category: str) -> List[StatusType]:
        """Obtener tipos de estado por categoría"""
        return db.query(StatusType).filter(
            StatusType.category == category,
            StatusType.is_active == True
        ).all()
    
    @staticmethod
    def update_status_type(db: Session, status_type_id: int, status_type: StatusTypeUpdate) -> Optional[StatusType]:
        """Actualizar un tipo de estado"""
        db_status_type = db.query(StatusType).filter(StatusType.id == status_type_id).first()
        if db_status_type:
            update_data = status_type.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_status_type, field, value)
            db.commit()
            db.refresh(db_status_type)
        return db_status_type
    
    @staticmethod
    def delete_status_type(db: Session, status_type_id: int) -> bool:
        """Eliminar un tipo de estado (soft delete)"""
        db_status_type = db.query(StatusType).filter(StatusType.id == status_type_id).first()
        if db_status_type:
            db_status_type.is_active = False
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_status_by_name(db: Session, name: str) -> Optional[StatusType]:
        """Obtener tipo de estado por nombre"""
        return db.query(StatusType).filter(
            StatusType.name == name,
            StatusType.is_active == True
        ).first()
    
    @staticmethod
    def create_default_status_types(db: Session) -> List[StatusType]:
        """Crear tipos de estado por defecto del sistema"""
        default_statuses = [
            # Estados de alertas
            {"name": "active", "description": "Alerta activa", "category": "alert_status"},
            {"name": "resolved", "description": "Alerta resuelta", "category": "alert_status"},
            {"name": "acknowledged", "description": "Alerta reconocida", "category": "alert_status"},
            
            # Estados de facturación
            {"name": "pending", "description": "Pendiente de pago", "category": "billing_status"},
            {"name": "paid", "description": "Pagado", "category": "billing_status"},
            {"name": "overdue", "description": "Vencido", "category": "billing_status"},
            {"name": "cancelled", "description": "Cancelado", "category": "billing_status"},
            
            # Estados de dispositivos
            {"name": "online", "description": "Dispositivo en línea", "category": "device_status"},
            {"name": "offline", "description": "Dispositivo desconectado", "category": "device_status"},
            {"name": "maintenance", "description": "En mantenimiento", "category": "device_status"},
            {"name": "error", "description": "Error en dispositivo", "category": "device_status"},
            
            # Estados de usuarios
            {"name": "active", "description": "Usuario activo", "category": "user_status"},
            {"name": "inactive", "description": "Usuario inactivo", "category": "user_status"},
            {"name": "suspended", "description": "Usuario suspendido", "category": "user_status"},
            
            # Estados de asignaciones
            {"name": "assigned", "description": "Asignación activa", "category": "assignment_status"},
            {"name": "completed", "description": "Asignación completada", "category": "assignment_status"},
            {"name": "cancelled", "description": "Asignación cancelada", "category": "assignment_status"},
            
            # Estados de recordatorios
            {"name": "pending", "description": "Recordatorio pendiente", "category": "reminder_status"},
            {"name": "completed", "description": "Recordatorio completado", "category": "reminder_status"},
            {"name": "overdue", "description": "Recordatorio vencido", "category": "reminder_status"},
            
            # Estados de paquetes
            {"name": "active", "description": "Paquete activo", "category": "package_status"},
            {"name": "expired", "description": "Paquete expirado", "category": "package_status"},
            {"name": "cancelled", "description": "Paquete cancelado", "category": "package_status"},
        ]
        
        all_statuses = []
        for status_data in default_statuses:
            # Verificar si ya existe
            existing = db.query(StatusType).filter(
                StatusType.name == status_data["name"],
                StatusType.category == status_data["category"]
            ).first()
            
            if existing:
                all_statuses.append(existing)
            else:
                try:
                    status_type = StatusType(**status_data)
                    db.add(status_type)
                    db.flush()  # Flush para obtener el ID
                    all_statuses.append(status_type)
                except Exception as e:
                    db.rollback()
                    # Si falla la inserción, intentar obtener el existente
                    existing = db.query(StatusType).filter(
                        StatusType.name == status_data["name"],
                        StatusType.category == status_data["category"]
                    ).first()
                    if existing:
                        all_statuses.append(existing)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            # Si falla el commit, retornar los existentes
            return db.query(StatusType).all()
        
        return all_statuses 