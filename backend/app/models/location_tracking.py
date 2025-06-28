from sqlalchemy import Column, String, Text, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base
import uuid


class LocationTracking(Base):
    """
    Modelo para seguimiento de ubicación en tiempo real.
    
    Reglas de negocio implementadas:
    - Seguimiento de ubicación para personas bajo cuidado
    - Soporte para debug y pruebas sin dispositivos IoT
    - Historial de ubicaciones con timestamps
    - Integración con geofences y alertas
    """
    __tablename__ = "location_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float)  # precisión en metros
    altitude = Column(Float)  # altura sobre el nivel del mar
    speed = Column(Float)  # velocidad en m/s
    heading = Column(Float)  # dirección en grados
    source_type = Column(String(50), default="manual")  # manual, gps, wifi, cell, debug
    source_device = Column(String(100))  # ID del dispositivo o fuente
    location_data = Column(JSONB, default=dict)  # datos adicionales del sensor
    is_debug = Column(Boolean, default=False)  # para pruebas y desarrollo
    debug_notes = Column(Text)  # notas para debug
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    cared_person = relationship("CaredPerson", back_populates="location_tracking")
    
    def __repr__(self):
        return f"<LocationTracking(id={self.id}, cared_person_id={self.cared_person_id}, lat={self.latitude}, lng={self.longitude})>"
    
    def get_location_data(self) -> dict:
        """
        Obtiene los datos adicionales de ubicación.
        
        Returns:
            dict: Datos adicionales de ubicación
        """
        return self.location_data or {}
    
    def set_location_data(self, data: dict):
        """
        Establece datos adicionales de ubicación.
        
        Args:
            data: Diccionario con datos adicionales
        """
        self.location_data = data
    
    def get_coordinates(self) -> tuple:
        """
        Obtiene las coordenadas como tupla.
        
        Returns:
            tuple: (latitude, longitude)
        """
        return (self.latitude, self.longitude)
    
    def set_coordinates(self, latitude: float, longitude: float):
        """
        Establece las coordenadas.
        
        Args:
            latitude: Latitud
            longitude: Longitud
        """
        self.latitude = latitude
        self.longitude = longitude
    
    def calculate_distance_to(self, other_lat: float, other_lng: float) -> float:
        """
        Calcula la distancia a otro punto usando la fórmula de Haversine.
        
        Args:
            other_lat: Latitud del otro punto
            other_lng: Longitud del otro punto
            
        Returns:
            float: Distancia en metros
        """
        import math
        
        # Radio de la Tierra en metros
        R = 6371000
        
        # Convertir a radianes
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other_lat)
        delta_lat = math.radians(other_lat - self.latitude)
        delta_lng = math.radians(other_lng - self.longitude)
        
        # Fórmula de Haversine
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def is_inside_geofence(self, geofence_center_lat: float, geofence_center_lng: float, 
                          geofence_radius: float) -> bool:
        """
        Verifica si la ubicación está dentro de un geofence.
        
        Args:
            geofence_center_lat: Latitud del centro del geofence
            geofence_center_lng: Longitud del centro del geofence
            geofence_radius: Radio del geofence en metros
            
        Returns:
            bool: True si está dentro del geofence
        """
        distance = self.calculate_distance_to(geofence_center_lat, geofence_center_lng)
        return distance <= geofence_radius
    
    def get_speed_kmh(self) -> float:
        """
        Obtiene la velocidad en km/h.
        
        Returns:
            float: Velocidad en km/h
        """
        if self.speed is None:
            return 0.0
        return self.speed * 3.6  # convertir m/s a km/h
    
    def get_heading_direction(self) -> str:
        """
        Obtiene la dirección cardinal basada en el heading.
        
        Returns:
            str: Dirección cardinal (N, NE, E, SE, S, SW, W, NW)
        """
        if self.heading is None:
            return "Unknown"
        
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(self.heading / 45) % 8
        return directions[index]
    
    @classmethod
    def get_source_types(cls) -> list:
        """
        Retorna los tipos de fuente de ubicación disponibles.
        
        Returns:
            list: Lista de tipos de fuente
        """
        return [
            {"value": "manual", "label": "Manual", "description": "Ubicación ingresada manualmente"},
            {"value": "gps", "label": "GPS", "description": "Ubicación por GPS"},
            {"value": "wifi", "label": "WiFi", "description": "Ubicación por WiFi"},
            {"value": "cell", "label": "Cellular", "description": "Ubicación por red celular"},
            {"value": "debug", "label": "Debug", "description": "Ubicación para pruebas"},
            {"value": "simulated", "label": "Simulado", "description": "Ubicación simulada"},
            {"value": "web", "label": "Web", "description": "Ubicación desde navegador web"},
            {"value": "mobile_app", "label": "App Móvil", "description": "Ubicación desde app móvil"}
        ]
    
    @classmethod
    def create_debug_location(cls, cared_person_id: uuid.UUID, latitude: float, longitude: float, 
                             notes: str = None) -> "LocationTracking":
        """
        Crea una ubicación de debug para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            latitude: Latitud
            longitude: Longitud
            notes: Notas de debug
            
        Returns:
            LocationTracking: Instancia de ubicación de debug
        """
        return cls(
            cared_person_id=cared_person_id,
            latitude=latitude,
            longitude=longitude,
            source_type="debug",
            is_debug=True,
            debug_notes=notes,
            accuracy=5.0,  # precisión típica de debug
            location_data={
                "debug": True,
                "test_location": True,
                "created_for_testing": True
            }
        )
    
    @classmethod
    def create_simulated_location(cls, cared_person_id: uuid.UUID, latitude: float, longitude: float,
                                 speed: float = None, heading: float = None) -> "LocationTracking":
        """
        Crea una ubicación simulada para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            latitude: Latitud
            longitude: Longitud
            speed: Velocidad simulada
            heading: Dirección simulada
            
        Returns:
            LocationTracking: Instancia de ubicación simulada
        """
        return cls(
            cared_person_id=cared_person_id,
            latitude=latitude,
            longitude=longitude,
            source_type="simulated",
            speed=speed,
            heading=heading,
            accuracy=10.0,  # precisión típica de simulación
            location_data={
                "simulated": True,
                "test_location": True,
                "simulation_data": True
            }
        )
    
    @classmethod
    def get_latest_location(cls, db, cared_person_id: uuid.UUID):
        """
        Obtiene la ubicación más reciente de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            LocationTracking: La ubicación más reciente o None
        """
        return db.query(cls).filter(
            cls.cared_person_id == cared_person_id
        ).order_by(cls.created_at.desc()).first()
    
    @classmethod
    def get_location_history(cls, db, cared_person_id: uuid.UUID, 
                           start_date=None, end_date=None, limit: int = 100) -> list:
        """
        Obtiene el historial de ubicaciones de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
            limit: Límite de registros
            
        Returns:
            list: Lista de ubicaciones
        """
        query = db.query(cls).filter(cls.cared_person_id == cared_person_id)
        
        if start_date:
            query = query.filter(cls.created_at >= start_date)
        
        if end_date:
            query = query.filter(cls.created_at <= end_date)
        
        return query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_debug_locations(cls, db, cared_person_id: uuid.UUID = None) -> list:
        """
        Obtiene ubicaciones de debug para pruebas.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado (opcional)
            
        Returns:
            list: Lista de ubicaciones de debug
        """
        query = db.query(cls).filter(cls.is_debug == True)
        
        if cared_person_id:
            query = query.filter(cls.cared_person_id == cared_person_id)
        
        return query.order_by(cls.created_at.desc()).all()
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para esta ubicación.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Latitud debe estar entre -90 y 90
        if self.latitude < -90 or self.latitude > 90:
            errors.append("La latitud debe estar entre -90 y 90 grados")
        
        # Regla: Longitud debe estar entre -180 y 180
        if self.longitude < -180 or self.longitude > 180:
            errors.append("La longitud debe estar entre -180 y 180 grados")
        
        # Regla: Precisión debe ser positiva si está definida
        if self.accuracy is not None and self.accuracy <= 0:
            errors.append("La precisión debe ser un valor positivo")
        
        # Regla: Velocidad debe ser no negativa si está definida
        if self.speed is not None and self.speed < 0:
            errors.append("La velocidad debe ser un valor no negativo")
        
        # Regla: Heading debe estar entre 0 y 360 si está definido
        if self.heading is not None and (self.heading < 0 or self.heading > 360):
            errors.append("El heading debe estar entre 0 y 360 grados")
        
        return errors 