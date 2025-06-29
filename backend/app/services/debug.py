from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

from app.models.debug_event import DebugEvent
from app.models.event import Event
from app.models.alert import Alert
from app.models.device import Device
from app.models.cared_person import CaredPerson
from app.models.user import User
from app.schemas.debug import DebugEventCreate, DebugSummary

class DebugService:
    """Debug and testing service"""
    
    @staticmethod
    def create_debug_event(db: Session, event_data: DebugEventCreate) -> DebugEvent:
        """Create a debug event"""
        debug_event = DebugEvent(**event_data.dict())
        db.add(debug_event)
        db.commit()
        db.refresh(debug_event)
        return debug_event
    
    @staticmethod
    def get_debug_events(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        event_type: str = None,
        severity: str = None,
        test_session: str = None
    ) -> List[DebugEvent]:
        """Get debug events with filters"""
        query = db.query(DebugEvent)
        
        if event_type:
            query = query.filter(DebugEvent.event_type == event_type)
        
        if severity:
            query = query.filter(DebugEvent.severity == severity)
        
        if test_session:
            query = query.filter(DebugEvent.test_session == test_session)
        
        return query.order_by(desc(DebugEvent.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def generate_test_data(db: Session, count: int = 10) -> Dict[str, Any]:
        """Generate test data for development"""
        from app.services.auth import AuthService
        
        results = {
            "users_created": 0,
            "cared_persons_created": 0,
            "devices_created": 0,
            "events_created": 0,
            "alerts_created": 0,
            "debug_events_created": 0
        }
        
        # Create test users
        for i in range(min(count, 5)):
            try:
                user_data = {
                    "email": f"test_user_{i}@example.com",
                    "username": f"testuser{i}",
                    "first_name": f"Test User {i}",
                    "last_name": f"Example {i}",
                    "phone": f"+1234567890{i}",
                    "is_freelance": i % 2 == 0,
                    "is_verified": True,
                    "password": "testpassword123"
                }
                
                from app.schemas.user import UserCreate
                user_create = UserCreate(**user_data)
                from app.services.user import UserService
                UserService.create_user(db, user_create)
                results["users_created"] += 1
                
            except Exception as e:
                print(f"Error creating test user {i}: {e}")
        
        # Create test cared persons
        for i in range(min(count, 3)):
            try:
                cared_person_data = {
                    "first_name": f"Test Person {i}",
                    "last_name": f"Care {i}",
                    "phone": f"+123456789{i}",
                    "care_level": ["low", "medium", "high"][i % 3],
                    "mobility_level": ["independent", "assisted", "wheelchair"][i % 3]
                }
                
                from app.models.cared_person import CaredPerson
                cared_person = CaredPerson(**cared_person_data)
                db.add(cared_person)
                results["cared_persons_created"] += 1
                
            except Exception as e:
                print(f"Error creating test cared person {i}: {e}")
        
        # Create test devices
        for i in range(min(count, 4)):
            try:
                device_data = {
                    "device_id": f"TEST_DEVICE_{i:03d}",
                    "device_type": ["sensor", "tracker", "camera", "wearable"][i % 4],
                    "model": f"Test Model {i}",
                    "manufacturer": "Test Manufacturer",
                    "status": "active",
                    "battery_level": 80 + (i * 5) % 20,
                    "signal_strength": 90 + (i * 3) % 10
                }
                
                from app.models.device import Device
                device = Device(**device_data)
                db.add(device)
                results["devices_created"] += 1
                
            except Exception as e:
                print(f"Error creating test device {i}: {e}")
        
        # Create test events
        for i in range(min(count, 8)):
            try:
                event_data = {
                    "event_type": ["sensor_event", "system_event", "user_action"][i % 3],
                    "event_subtype": f"test_subtype_{i}",
                    "severity": ["info", "warning", "error"][i % 3],
                    "message": f"Test event message {i}",
                    "event_time": datetime.utcnow() - timedelta(hours=i)
                }
                
                from app.models.event import Event
                event = Event(**event_data)
                db.add(event)
                results["events_created"] += 1
                
            except Exception as e:
                print(f"Error creating test event {i}: {e}")
        
        # Create test alerts
        for i in range(min(count, 6)):
            try:
                alert_data = {
                    "alert_type": ["health_alert", "security_alert", "device_alert"][i % 3],
                    "alert_subtype": f"test_alert_{i}",
                    "severity": ["low", "medium", "high"][i % 3],
                    "title": f"Test Alert {i}",
                    "message": f"Test alert message {i}",
                    "status": "active",
                    "priority": 5 + (i % 5)
                }
                
                from app.models.alert import Alert
                alert = Alert(**alert_data)
                db.add(alert)
                results["alerts_created"] += 1
                
            except Exception as e:
                print(f"Error creating test alert {i}: {e}")
        
        # Create test debug events
        for i in range(min(count, 10)):
            try:
                debug_data = {
                    "event_type": ["test_event", "debug_event", "simulation"][i % 3],
                    "event_subtype": f"test_debug_{i}",
                    "severity": ["debug", "info", "warning"][i % 3],
                    "message": f"Test debug message {i}",
                    "source": "test_suite",
                    "test_session": f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "environment": "development",
                    "event_time": datetime.utcnow() - timedelta(minutes=i)
                }
                
                debug_event = DebugEvent(**debug_data)
                db.add(debug_event)
                results["debug_events_created"] += 1
                
            except Exception as e:
                print(f"Error creating test debug event {i}: {e}")
        
        db.commit()
        return results
    
    @staticmethod
    def clean_test_data(db: Session) -> Dict[str, int]:
        """Clean all test data (robusto: borra todo lo relevante, no solo los TEST_DEVICE_*)"""
        results = {
            "location_tracking_deleted": 0,
            "geofences_deleted": 0,
            "debug_events_deleted": 0,
            "cared_persons_deleted": 0,
            "devices_deleted": 0
        }

        # Eliminar en orden correcto para respetar claves foráneas
        from app.models.location_tracking import LocationTracking
        from app.models.geofence import Geofence
        from app.models.debug_event import DebugEvent
        from app.models.cared_person import CaredPerson
        from app.models.device import Device

        results["location_tracking_deleted"] = db.query(LocationTracking).delete()
        results["geofences_deleted"] = db.query(Geofence).delete()
        results["debug_events_deleted"] = db.query(DebugEvent).delete()
        results["cared_persons_deleted"] = db.query(CaredPerson).delete()
        results["devices_deleted"] = db.query(Device).delete()
        db.commit()
        return results
    
    @staticmethod
    def get_debug_summary(db: Session) -> DebugSummary:
        """Get debug summary statistics"""
        # Total events
        total_events = db.query(func.count(DebugEvent.id)).scalar()
        
        # Events by type
        events_by_type = db.query(
            DebugEvent.event_type,
            func.count(DebugEvent.id)
        ).group_by(DebugEvent.event_type).all()
        events_by_type_dict = {event_type: count for event_type, count in events_by_type}
        
        # Events by severity
        events_by_severity = db.query(
            DebugEvent.severity,
            func.count(DebugEvent.id)
        ).group_by(DebugEvent.severity).all()
        events_by_severity_dict = {severity: count for severity, count in events_by_severity}
        
        # Recent events (last 10)
        recent_events = db.query(DebugEvent).order_by(
            desc(DebugEvent.created_at)
        ).limit(10).all()
        
        # Test sessions
        test_sessions = db.query(DebugEvent.test_session).distinct().all()
        test_sessions_list = [session[0] for session in test_sessions if session[0]]
        
        return DebugSummary(
            total_events=total_events,
            events_by_type=events_by_type_dict,
            events_by_severity=events_by_severity_dict,
            recent_events=recent_events,
            test_sessions=test_sessions_list
        )
