from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class LocationTracking(BaseModel):
    """LocationTracking model for GPS and location data"""
    __tablename__ = "location_tracking"
    
    # Location data
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)  # GPS accuracy in meters
    speed = Column(Float, nullable=True)  # Speed in km/h
    heading = Column(Float, nullable=True)  # Direction in degrees
    
    # Location context
    location_name = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    place_type = Column(String(50), nullable=True)  # home, work, hospital, etc.
    
    # Tracking metadata
    tracking_method = Column(String(50), nullable=True)  # gps, wifi, cell_tower, manual
    battery_level = Column(Integer, nullable=True)
    signal_strength = Column(Integer, nullable=True)
    
    # Timestamps
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    received_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="location_tracking")
    cared_person = relationship("CaredPerson", back_populates="location_tracking")
    device = relationship("Device", back_populates="location_tracking")
    
    def __repr__(self):
        return f"<LocationTracking(lat={self.latitude}, lng={self.longitude}, recorded_at='{self.recorded_at}')>"
    
    @classmethod
    def get_tracking_methods(cls) -> list:
        """Returns available tracking methods"""
        return ["gps", "wifi", "cell_tower", "manual", "beacon", "rfid"]
    
    @classmethod
    def get_place_types(cls) -> list:
        """Returns available place types"""
        return ["home", "work", "hospital", "clinic", "pharmacy", "store", "park", "other"]
