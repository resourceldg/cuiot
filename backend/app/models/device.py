from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.device_type import DeviceType
import uuid

class Device(BaseModel):
    """Device model for IoT devices and sensors"""
    __tablename__ = "devices"
    
    # Override id to use UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Device identification
    device_id = Column(String(100), unique=True, nullable=False, index=True)  # Unique device identifier
    name = Column(String(255), nullable=False)  # Nombre del dispositivo
    type = Column(String(50), nullable=False, default="unknown")  # Tipo de dispositivo (wearable, sensor, etc.)
    location = Column(String(255), nullable=True)  # Ubicación física
    device_type_id = Column(Integer, ForeignKey('device_types.id'), nullable=True, index=True)
    model = Column(String(100), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True, unique=True)
    
    # Device status (normalized)
    status_type_id = Column(Integer, ForeignKey("status_types.id"), nullable=True, index=True)
    battery_level = Column(Integer, nullable=True)  # 0-100
    signal_strength = Column(Integer, nullable=True)  # 0-100
    last_seen = Column(DateTime(timezone=True), nullable=True)
    
    # Location and placement
    location_description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    
    # Configuration
    settings = Column(Text, nullable=True)  # JSON string with device settings
    firmware_version = Column(String(50), nullable=True)
    hardware_version = Column(String(50), nullable=True)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id", ondelete="CASCADE"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="devices")
    cared_person = relationship("CaredPerson", back_populates="devices")
    institution = relationship("Institution", back_populates="devices")
    device_configs = relationship("DeviceConfig", back_populates="device", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="device")
    alerts = relationship("Alert", back_populates="device")
    location_tracking = relationship("LocationTracking", back_populates="device")
    debug_events = relationship("DebugEvent", back_populates="device")
    status_type = relationship("StatusType")
    device_type = relationship("DeviceType")
    package = relationship("Package", backref="devices")
    
    def __repr__(self):
        return f"<Device(device_id='{self.device_id}', name='{self.name}', type='{self.type}')>"
    
    @property
    def is_online(self) -> bool:
        """Check if device is currently online"""
        if not self.last_seen:
            return False
        
        from datetime import datetime, timedelta
        now = datetime.now()
        # Consider offline if not seen in last 5 minutes
        return (now - self.last_seen) < timedelta(minutes=5)
    
    @classmethod
    def get_device_types(cls) -> list:
        """Returns available device types - DEPRECATED: Use DeviceType model instead"""
        return [
            "sensor", "tracker", "camera", "smartphone", "tablet", 
            "wearable", "medical_device", "environmental_sensor",
            "door_sensor", "motion_sensor", "temperature_sensor",
            "heart_rate_monitor", "fall_detector", "gps_tracker"
        ]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["active", "inactive", "maintenance", "error", "offline", "testing"]
