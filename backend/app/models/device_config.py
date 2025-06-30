from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class DeviceConfig(BaseModel):
    """DeviceConfig model for device configuration and settings"""
    __tablename__ = "device_configs"
    
    # Configuration identification
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False, index=True)
    config_type = Column(String(50), nullable=False, index=True)  # sensor_config, alert_config, etc.
    config_name = Column(String(100), nullable=False)
    
    # Configuration data
    config_data = Column(Text, nullable=True)  # JSON string with configuration
    description = Column(Text, nullable=True)
    
    # Configuration status
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Version control
    version = Column(String(20), nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    applied_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    device = relationship("Device", back_populates="device_configs")
    applied_by_user = relationship("User", foreign_keys=[applied_by])
    
    def __repr__(self):
        return f"<DeviceConfig(device_id={self.device_id}, type='{self.config_type}', name='{self.config_name}')>"
    
    @classmethod
    def get_config_types(cls) -> list:
        """Returns available configuration types"""
        return [
            "sensor_config", "alert_config", "notification_config", 
            "sampling_config", "threshold_config", "calibration_config",
            "network_config", "security_config", "power_config"
        ]
