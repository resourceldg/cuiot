import pytest
from uuid import uuid4
from datetime import datetime, date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.core.database import get_db
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.medical_profile import MedicalProfile
from app.models.medication_schedule import MedicationSchedule
from app.models.medication_log import MedicationLog
from app.services.auth import AuthService
from app.schemas.user import UserCreate
from app.services.user import UserService

client = TestClient(app)

TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"

def get_auth_token():
    """Create test user and get auth token"""
    # Create test user
    user_data = {
        "email": TEST_USER_EMAIL,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": TEST_USER_PASSWORD
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    # If user already exists, ignore the error
    if response.status_code not in (200, 201, 400, 409):
        assert False, f"User registration failed: {response.text}"
    
    # Login to get token
    response = client.post("/api/v1/auth/login", json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["access_token"]

@pytest.fixture
def auth_headers():
    """Get authentication headers for tests"""
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_cared_person(db_session):
    """Create a test cared person"""
    cared_person = CaredPerson(
        id=uuid4(),
        first_name="Test",
        last_name="CaredPerson",
        date_of_birth=date(1950, 1, 1),
        gender="other",
        emergency_contact="123456789",
        is_active=True
    )
    db_session.add(cared_person)
    db_session.commit()
    db_session.refresh(cared_person)
    return cared_person

class TestMedicalProfile:
    def test_create_medical_profile(self, db_session, test_cared_person, auth_headers):
        """Test creating a medical profile"""
        medical_profile_data = {
            "blood_type": "O+",
            "allergies": "Penicillin, nuts",
            "chronic_conditions": "Diabetes, hypertension",
            "emergency_info": {"emergency_contact": "123456789"},
            "medical_preferences": {"diet": "low_sodium"},
            "insurance_info": {"provider": "Test Insurance"},
            "cared_person_id": str(test_cared_person.id)
        }
        
        response = client.post("/api/v1/medical-profiles/", json=medical_profile_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["blood_type"] == "O+"
        assert data["allergies"] == "Penicillin, nuts"
        assert data["cared_person_id"] == str(test_cared_person.id)

    def test_get_medical_profile_by_cared_person(self, db_session, test_cared_person, auth_headers):
        """Test getting medical profile by cared person ID"""
        # Create medical profile first
        medical_profile = MedicalProfile(
            id=uuid4(),
            blood_type="A+",
            allergies="None",
            chronic_conditions="None",
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(medical_profile)
        db_session.commit()
        
        response = client.get(f"/api/v1/medical-profiles/cared-person/{test_cared_person.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["blood_type"] == "A+"
        assert data["cared_person_id"] == str(test_cared_person.id)

    def test_update_medical_profile(self, db_session, test_cared_person, auth_headers):
        """Test updating a medical profile"""
        # Create medical profile first
        medical_profile = MedicalProfile(
            id=uuid4(),
            blood_type="B+",
            allergies="None",
            chronic_conditions="None",
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(medical_profile)
        db_session.commit()
        
        update_data = {
            "blood_type": "AB+",
            "allergies": "Shellfish"
        }
        
        response = client.put(f"/api/v1/medical-profiles/{medical_profile.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["blood_type"] == "AB+"
        assert data["allergies"] == "Shellfish"

class TestMedicationSchedule:
    def test_create_medication_schedule(self, db_session, test_cared_person, auth_headers):
        """Test creating a medication schedule"""
        schedule_data = {
            "medication_name": "Aspirin",
            "dosage": "100mg",
            "frequency": "Once daily",
            "start_date": str(date.today()),
            "instructions": "Take with food",
            "cared_person_id": str(test_cared_person.id)
        }
        
        response = client.post("/api/v1/medication-schedules/", json=schedule_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["medication_name"] == "Aspirin"
        assert data["dosage"] == "100mg"
        assert data["cared_person_id"] == str(test_cared_person.id)

    def test_get_active_medication_schedules(self, db_session, test_cared_person, auth_headers):
        """Test getting active medication schedules"""
        # Create active schedule
        active_schedule = MedicationSchedule(
            id=uuid4(),
            medication_name="Vitamin D",
            dosage="1000 IU",
            frequency="Once daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(active_schedule)
        db_session.commit()
        
        response = client.get(f"/api/v1/medication-schedules/cared-person/{test_cared_person.id}/active", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["medication_name"] == "Vitamin D"

    def test_get_medication_schedules_by_cared_person(self, db_session, test_cared_person, auth_headers):
        """Test getting all medication schedules for a cared person"""
        # Create multiple schedules
        schedule1 = MedicationSchedule(
            id=uuid4(),
            medication_name="Medication 1",
            dosage="10mg",
            frequency="Twice daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        schedule2 = MedicationSchedule(
            id=uuid4(),
            medication_name="Medication 2",
            dosage="20mg",
            frequency="Once daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add_all([schedule1, schedule2])
        db_session.commit()
        
        response = client.get(f"/api/v1/medication-schedules/cared-person/{test_cared_person.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

class TestMedicationLog:
    def test_create_medication_log(self, db_session, test_cared_person, auth_headers):
        """Test creating a medication log entry"""
        # Create medication schedule first
        schedule = MedicationSchedule(
            id=uuid4(),
            medication_name="Test Medication",
            dosage="50mg",
            frequency="Once daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(schedule)
        db_session.commit()
        
        log_data = {
            "medication_schedule_id": str(schedule.id),
            "taken_at": datetime.now().isoformat(),
            "confirmed_by": None,
            "notes": "Taken as prescribed",
            "dosage_given": "50mg",
            "is_missed": False
        }
        
        response = client.post("/api/v1/medication-logs/", json=log_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["medication_schedule_id"] == str(schedule.id)
        assert data["taken_at"] is not None

    def test_get_medication_logs_by_schedule(self, db_session, test_cared_person, auth_headers):
        # Create schedule and logs
        schedule = MedicationSchedule(
            id=uuid4(),
            medication_name="Test Medication",
            dosage="50mg",
            frequency="Once daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(schedule)
        db_session.commit()
        
        log1 = MedicationLog(
            id=uuid4(),
            medication_schedule_id=schedule.id,
            taken_at=datetime.now(),
            is_missed=False,
            notes="Taken as prescribed"
        )
        log2 = MedicationLog(
            id=uuid4(),
            medication_schedule_id=schedule.id,
            taken_at=datetime.now(),
            is_missed=True,
            notes="Missed dose"
        )
        db_session.add_all([log1, log2])
        db_session.commit()
        
        response = client.get(f"/api/v1/medication-logs/schedule/{schedule.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_recent_medication_logs(self, db_session, test_cared_person, auth_headers):
        # Create schedule and recent log
        schedule = MedicationSchedule(
            id=uuid4(),
            medication_name="Test Medication",
            dosage="50mg",
            frequency="Once daily",
            start_date=date.today(),
            cared_person_id=test_cared_person.id,
            is_active=True
        )
        db_session.add(schedule)
        db_session.commit()
        
        recent_log = MedicationLog(
            id=uuid4(),
            medication_schedule_id=schedule.id,
            taken_at=datetime.now(),
            is_missed=False,
            notes="Taken as prescribed"
        )
        db_session.add(recent_log)
        db_session.commit()
        
        response = client.get(f"/api/v1/medication-logs/cared-person/{test_cared_person.id}/recent?days=7", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["notes"] == "Taken as prescribed" 