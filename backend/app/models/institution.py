from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Institution(Base):
    """
    Modelo para instituciones de cuidado y atención.
    
    Reglas de negocio implementadas:
    - Una institución puede tener múltiples usuarios y personas bajo cuidado
    - Las instituciones tienen tipos específicos (geriátrico, centro de día, etc.)
    - Las instituciones tienen capacidades y servicios específicos
    - Las instituciones pueden tener múltiples ubicaciones
    """
    __tablename__ = "institutions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    institution_type = Column(String(50), nullable=False, index=True)  # geriatric, day_center, special_school, hospital, clinic
    legal_name = Column(String(200))
    tax_id = Column(String(50))
    license_number = Column(String(100))
    address = Column(JSONB, default=dict)
    contact_info = Column(JSONB, default=dict)
    services = Column(JSONB, default=dict)
    capacity = Column(JSONB, default=dict)
    operating_hours = Column(JSONB, default=dict)
    staff_info = Column(JSONB, default=dict)
    certifications = Column(JSONB, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    users = relationship("User", back_populates="institution")
    cared_persons = relationship("CaredPerson", back_populates="institution")
    devices = relationship("Device", back_populates="institution")
    protocols = relationship("EmergencyProtocol", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution(id={self.id}, name='{self.name}', type='{self.institution_type}')>"
    
    def get_contact_info(self) -> dict:
        """
        Obtiene la información de contacto de la institución.
        
        Returns:
            dict: Información de contacto
        """
        return self.contact_info or {}
    
    def add_contact(self, contact_type: str, value: str, is_primary: bool = False):
        """
        Agrega un contacto a la institución.
        
        Args:
            contact_type: Tipo de contacto (phone, email, website, etc.)
            value: Valor del contacto
            is_primary: Si es el contacto principal
        """
        if not self.contact_info:
            self.contact_info = {"contacts": []}
        
        contact = {
            "type": contact_type,
            "value": value,
            "is_primary": is_primary,
            "active": True
        }
        
        self.contact_info["contacts"].append(contact)
    
    def get_services(self) -> list:
        """
        Obtiene los servicios ofrecidos por la institución.
        
        Returns:
            list: Lista de servicios
        """
        if not self.services:
            return []
        
        return self.services.get("services", [])
    
    def add_service(self, service_name: str, description: str = None, is_available: bool = True):
        """
        Agrega un servicio a la institución.
        
        Args:
            service_name: Nombre del servicio
            description: Descripción del servicio
            is_available: Si el servicio está disponible
        """
        if not self.services:
            self.services = {"services": []}
        
        service = {
            "name": service_name,
            "description": description,
            "is_available": is_available,
            "active": True
        }
        
        self.services["services"].append(service)
    
    def get_capacity(self) -> dict:
        """
        Obtiene la capacidad de la institución.
        
        Returns:
            dict: Información de capacidad
        """
        return self.capacity or {}
    
    def set_capacity(self, total_beds: int = None, available_beds: int = None, 
                    total_staff: int = None, max_patients: int = None):
        """
        Establece la capacidad de la institución.
        
        Args:
            total_beds: Total de camas disponibles
            available_beds: Camas disponibles actualmente
            total_staff: Total de personal
            max_patients: Máximo de pacientes
        """
        self.capacity = {
            "total_beds": total_beds,
            "available_beds": available_beds,
            "total_staff": total_staff,
            "max_patients": max_patients,
            "occupancy_rate": (total_beds - available_beds) / total_beds * 100 if total_beds and available_beds else None
        }
    
    def get_operating_hours(self) -> dict:
        """
        Obtiene el horario de operación de la institución.
        
        Returns:
            dict: Horario de operación
        """
        return self.operating_hours or {}
    
    def set_operating_hours(self, hours: dict):
        """
        Establece el horario de operación de la institución.
        
        Args:
            hours: Diccionario con el horario por día
        """
        self.operating_hours = hours
    
    def get_address(self) -> dict:
        """
        Obtiene la dirección de la institución.
        
        Returns:
            dict: Información de dirección
        """
        return self.address or {}
    
    def set_address(self, street: str, city: str, state: str, postal_code: str, 
                   country: str = "Argentina", coordinates: dict = None):
        """
        Establece la dirección de la institución.
        
        Args:
            street: Calle y número
            city: Ciudad
            state: Provincia
            postal_code: Código postal
            country: País
            coordinates: Coordenadas GPS
        """
        self.address = {
            "street": street,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "coordinates": coordinates
        }
    
    @classmethod
    def get_institution_types(cls) -> list:
        """
        Retorna los tipos de institución disponibles.
        
        Returns:
            list: Lista de tipos de institución
        """
        return [
            {"value": "geriatric", "label": "Geriátrico", "description": "Centro de cuidado para adultos mayores"},
            {"value": "day_center", "label": "Centro de Día", "description": "Centro de atención diurna"},
            {"value": "special_school", "label": "Escuela Especial", "description": "Escuela para necesidades especiales"},
            {"value": "hospital", "label": "Hospital", "description": "Hospital general o especializado"},
            {"value": "clinic", "label": "Clínica", "description": "Clínica médica"},
            {"value": "rehabilitation", "label": "Centro de Rehabilitación", "description": "Centro de rehabilitación física"},
            {"value": "mental_health", "label": "Salud Mental", "description": "Centro de salud mental"},
            {"value": "disability_center", "label": "Centro de Discapacidad", "description": "Centro especializado en discapacidad"},
            {"value": "autism_center", "label": "Centro de Autismo", "description": "Centro especializado en autismo"},
            {"value": "nursing_home", "label": "Hogar de Ancianos", "description": "Hogar de cuidado para ancianos"}
        ]
    
    @classmethod
    def get_by_type(cls, db, institution_type: str) -> list:
        """
        Obtiene instituciones por tipo.
        
        Args:
            db: Sesión de base de datos
            institution_type: Tipo de institución
            
        Returns:
            list: Lista de instituciones del tipo especificado
        """
        return db.query(cls).filter(
            cls.institution_type == institution_type,
            cls.is_active == True
        ).all()
    
    @classmethod
    def get_by_location(cls, db, city: str = None, state: str = None) -> list:
        """
        Obtiene instituciones por ubicación.
        
        Args:
            db: Sesión de base de datos
            city: Ciudad
            state: Provincia
            
        Returns:
            list: Lista de instituciones en la ubicación especificada
        """
        query = db.query(cls).filter(cls.is_active == True)
        
        if city:
            query = query.filter(cls.address['city'].astext == city)
        
        if state:
            query = query.filter(cls.address['state'].astext == state)
        
        return query.all()
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para esta institución.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Debe tener información de contacto
        if not self.get_contact_info():
            errors.append("La institución debe tener al menos un contacto")
        
        # Regla: Debe tener dirección
        if not self.get_address():
            errors.append("La institución debe tener una dirección")
        
        # Regla: Debe tener al menos un servicio
        if not self.get_services():
            errors.append("La institución debe ofrecer al menos un servicio")
        
        return errors 