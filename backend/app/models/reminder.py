from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime, timezone

class Reminder(BaseModel):
    """Reminder model for medication, appointments, and tasks"""
    __tablename__ = "reminders"
    
    # Reminder identification
    reminder_type = Column(String(50), nullable=False, index=True)  # medication, appointment, task, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(Date, nullable=True)
    repeat_pattern = Column(String(100), nullable=True)  # daily, weekly, monthly, custom
    
    # Status and completion
    status = Column(String(20), default="pending", nullable=False)  # pending, completed, missed, cancelled
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Priority and importance
    priority = Column(Integer, default=5, nullable=False)  # 1-10, higher is more important
    is_important = Column(Boolean, default=False, nullable=False)
    
    # Additional data
    reminder_data = Column(Text, nullable=True)  # JSON string with reminder details
    notes = Column(Text, nullable=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cared_person_id = Column(Integer, ForeignKey("cared_persons.id"), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="reminders")
    cared_person = relationship("CaredPerson", back_populates="reminders")
    completed_by_user = relationship("User", foreign_keys=[completed_by])
    
    def __repr__(self):
        return f"<Reminder(type='{self.reminder_type}', title='{self.title}', status='{self.status}')>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if reminder is overdue"""
        now = datetime.now(timezone.utc)
        return self.status == "pending" and self.scheduled_time < now
    
    @property
    def is_completed(self) -> bool:
        """Check if reminder is completed"""
        return self.status == "completed"
    
    @classmethod
    def get_reminder_types(cls) -> list:
        """Returns available reminder types"""
        return [
            "medication", "appointment", "task", "exercise", "meal",
            "hygiene", "social", "medical_checkup", "therapy", "maintenance"
        ]
    
    @classmethod
    def get_status_types(cls) -> list:
        """Returns available status types"""
        return ["pending", "completed", "missed", "cancelled", "snoozed"]
    
    @classmethod
    def get_repeat_patterns(cls) -> list:
        """Returns available repeat patterns"""
        return ["none", "daily", "weekly", "monthly", "yearly", "custom"]
