from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class Geofence(BaseModel):
    """Geofence model for location-based alerts and zones"""
    __tablename__ = "geofences"
    
    # Geofence identification
    name = Column(String(200), nullable=False, index=True)
    geofence_type = Column(String(50), nullable=False, index=True)  # safe_zone, restricted_area, etc.
    description = Column(Text, nullable=True)
    
    # Location and geometry
    center_latitude = Column(Float, nullable=False)
    center_longitude = Column(Float, nullable=False)
    radius = Column(Float, nullable=True)  # Radius in meters for circular geofences
    polygon_coordinates = Column(Text, nullable=True)  # JSON string with polygon coordinates
    
    # Geofence behavior
    trigger_action = Column(String(50), nullable=False)  # enter, exit, both
    alert_message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Schedule
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    days_of_week = Column(String(50), nullable=True)  # "1,2,3,4,5,6,7" for days
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=True)
    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="geofences")
    cared_person = relationship("CaredPerson", back_populates="geofences")
    institution = relationship("Institution", back_populates="geofences")
    
    def __repr__(self):
        return f"<Geofence(name='{self.name}', type='{self.geofence_type}', action='{self.trigger_action}')>"
    
    @classmethod
    def get_geofence_types(cls) -> list:
        """Returns available geofence types"""
        return [
            "safe_zone", "restricted_area", "home_zone", "work_zone", 
            "medical_zone", "danger_zone", "custom_zone", "monitoring_zone"
        ]
    
    @classmethod
    def get_trigger_actions(cls) -> list:
        """Returns available trigger actions"""
        return ["enter", "exit", "both", "inside", "outside"]
