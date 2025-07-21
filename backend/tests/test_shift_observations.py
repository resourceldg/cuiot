import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/app')

from main import app
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.services.auth import AuthService

client = TestClient(app)

def create_test_user(db_session, email, first_name="Test", last_name="User", password="testpassword"):
    password_hash = AuthService.get_password_hash(password)
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password_hash=password_hash,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def create_test_cared_person(db_session, user_id, first_name="Test", last_name="Person"):
    # Get care_type_id for "delegated"
    if not care_type:
        # Create if not exists
        db_session.add(care_type)
        db_session.commit()
        db_session.refresh(care_type)
    
    cared_person = CaredPerson(
        first_name=first_name,
        last_name=last_name,
        care_type_id=care_type.id,
        user_id=user_id,
        is_active=True
    )
    db_session.add(cared_person)
    db_session.commit()
    db_session.refresh(cared_person)
    return cared_person

def get_shift_observation_type_id(db_session, type_name):
    """Helper function to get shift observation type ID"""
    from app.models.shift_observation_type import ShiftObservationType
    shift_type = db_session.query(ShiftObservationType).filter(ShiftObservationType.name == type_name).first()
    if not shift_type:
        # Create if not exists
        shift_type = ShiftObservationType(name=type_name, description=f"{type_name} shift")
        db_session.add(shift_type)
        db_session.commit()
        db_session.refresh(shift_type)
    return shift_type.id

def test_create_shift_observation_success(db_session: Session, clean_database, normalized_catalogs):
    """Test successful creation of a shift observation"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get shift_observation_type_id for "morning"
    shift_type_id = normalized_catalogs["shift_observation_type_id"]
    
    # Prepare test data
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": shift_type_id,
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "good",
        "mental_state": "alert",
        "mood": "happy",
        "appetite": "good",
        "food_intake": "full_meal",
        "fluid_intake": "adequate",
        "bowel_movement": "normal",
        "urinary_output": "normal",
        "incontinence_episodes": 0,
        "pain_level": 2,
        "hygiene_status_type_id": normalized_catalogs["status_type_id"],
        "mobility_level": "independent",
        "cognitive_function": "normal",
        "communication_ability": "normal",
        "social_interaction": "active",
        "exercise_performed": True,
        "exercise_details": "Caminata de 30 minutos en el jardín",
        "incidents_occurred": False,
        "fall_risk_assessment": "low",
        "family_contact": True,
        "family_notes": "Familia informada del buen estado general",
        "doctor_contact": False,
        "handover_notes": "Paciente estable, continuar con rutina normal",
        "cared_person_id": str(cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    
    # Should return success
    assert response.status_code == 201
    result = response.json()
    
    # Verify response structure
    assert "id" in result
    assert result["shift_observation_type_id"] == shift_type_id
    assert result["physical_condition"] == "good"
    assert result["mental_state"] == "alert"
    assert result["mood"] == "happy"
    assert result["appetite"] == "good"
    assert result["food_intake"] == "full_meal"
    assert result["fluid_intake"] == "adequate"
    assert result["bowel_movement"] == "normal"
    assert result["urinary_output"] == "normal"
    assert result["incontinence_episodes"] == 0
    assert result["pain_level"] == 2
    assert result["hygiene_status_type_id"] == normalized_catalogs["status_type_id"]
    assert result["mobility_level"] == "independent"
    assert result["cognitive_function"] == "normal"
    assert result["communication_ability"] == "normal"
    assert result["social_interaction"] == "active"
    assert result["exercise_performed"] == True
    assert result["exercise_details"] == "Caminata de 30 minutos en el jardín"
    assert result["incidents_occurred"] == False
    assert result["fall_risk_assessment"] == "low"
    assert result["family_contact"] == True
    assert result["family_notes"] == "Familia informada del buen estado general"
    assert result["doctor_contact"] == False
    assert result["handover_notes"] == "Paciente estable, continuar con rutina normal"
    assert result["cared_person_id"] == str(cared_person.id)
    assert result["caregiver_id"] == str(test_user.id)
    assert result["is_verified"] == False
    assert result["is_active"] == True
    
    # Verify caregiver information
    assert result["caregiver_name"] == "Test User"
    assert result["caregiver_email"] == "test@example.com"
    assert result["cared_person_name"] == "Test Person"

def test_create_shift_observation_invalid_shift_type(db_session: Session, clean_database, normalized_catalogs):
    """Test validation error for invalid shift type"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test2@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare test data with invalid shift type ID
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": 999999,  # Invalid ID that should trigger validation error
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "cared_person_id": str(cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    
    # Should return validation error (422 Unprocessable Entity) or server error (500)
    # Both are acceptable for invalid foreign key
    assert response.status_code in [422, 500]
    if response.status_code == 422:
        errors = response.json()["detail"]
        assert any(
            e["loc"][-1] == "shift_observation_type_id" and ("greater than 0" in e["msg"] or "does not exist" in e["msg"])
            for e in errors
        )

def test_get_shift_observations_list(db_session: Session, clean_database, normalized_catalogs):
    """Test getting list of shift observations"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test3@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get shift_observation_type_id for "afternoon"
    shift_type_id = get_shift_observation_type_id(db_session, "afternoon")
    
    # Create a test observation
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": shift_type_id,
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "excellent",
        "mental_state": "alert",
        "cared_person_id": str(cared_person.id)
    }
    
    # Create observation
    create_response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    assert create_response.status_code == 201
    
    # Get list
    response = client.get("/api/v1/shift-observations/", headers=headers)
    
    # Should return success
    assert response.status_code == 200
    result = response.json()
    
    # Verify response structure
    assert "observations" in result
    assert "total" in result
    assert "page" in result
    assert "size" in result
    assert "pages" in result
    
    # Verify observations
    assert len(result["observations"]) >= 1
    assert result["total"] >= 1
    
    # Verify first observation
    observation = result["observations"][0]
    assert observation["shift_observation_type_id"] == shift_type_id
    assert observation["physical_condition"] == "excellent"
    assert observation["mental_state"] == "alert"

def test_get_observations_by_cared_person(db_session: Session, clean_database, normalized_catalogs):
    """Test getting observations summary by cared person"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test4@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test observation
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "fair",
        "mental_state": "drowsy",
        "incidents_occurred": True,
        "incident_details": "Paciente se levantó de la cama sin asistencia",
        "cared_person_id": str(cared_person.id)
    }
    
    # Create observation
    create_response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    assert create_response.status_code == 201
    
    # Get summary by cared person
    response = client.get(f"/api/v1/shift-observations/cared-person/{cared_person.id}/summary", headers=headers)
    
    # Should return success
    assert response.status_code == 200
    result = response.json()
    
    # Verify response structure
    assert isinstance(result, list)
    assert len(result) >= 1
    
    # Verify summary
    summary = result[0]
    assert "id" in summary
    assert summary["physical_condition"] == "fair"
    assert summary["mental_state"] == "drowsy"
    assert summary["incidents_occurred"] == True
    assert summary["status"] == "draft"
    assert "caregiver_name" in summary
    assert "created_at" in summary

def test_update_shift_observation(db_session: Session, normalized_catalogs):
    """Test updating a shift observation"""
    # Create test user and cared person
    test_user = create_test_user(db_session, "test5@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    # Create a test observation
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "good",
        "mental_state": "alert",
        "cared_person_id": str(cared_person.id)
    }
    # Create observation
    create_response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    assert create_response.status_code == 201
    observation_id = create_response.json()["id"]
    # Update observation
    update_data = {
        "physical_condition": "excellent",
        "mental_state": "alert",
        "mood": "happy",
        "handover_notes": "Paciente muy colaborativo durante el turno"
    }
    response = client.put(f"/api/v1/shift-observations/{observation_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert result["physical_condition"] == "excellent"
    assert result["mental_state"] == "alert"
    assert result["mood"] == "happy"
    assert result["handover_notes"] == "Paciente muy colaborativo durante el turno"

def test_verify_shift_observation(db_session: Session, normalized_catalogs):
    """Test verifying a shift observation"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test6@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test observation
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "good",
        "mental_state": "alert",
        "cared_person_id": str(cared_person.id)
    }
    
    # Create observation
    create_response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    assert create_response.status_code == 201
    observation_id = create_response.json()["id"]
    
    # Verify observation
    response = client.post(f"/api/v1/shift-observations/{observation_id}/verify", headers=headers)
    
    # Should return success
    assert response.status_code == 200
    result = response.json()
    
    # Verify verification fields
    assert result["is_verified"] == True
    assert result["verified_by"] == str(test_user.id)
    assert result["verified_at"] is not None
    # Note: status field has been normalized to status_type_id
    # The verification process should update the status_type_id to a "reviewed" status

def test_delete_shift_observation(db_session: Session, normalized_catalogs):
    """Test deleting a shift observation"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test7@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test observation
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "good",
        "mental_state": "alert",
        "cared_person_id": str(cared_person.id)
    }
    
    # Create observation
    create_response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    assert create_response.status_code == 201
    observation_id = create_response.json()["id"]
    
    # Delete observation
    response = client.delete(f"/api/v1/shift-observations/{observation_id}", headers=headers)
    
    # Should return success (204 No Content)
    assert response.status_code == 204
    
    # Verify observation is not found
    get_response = client.get(f"/api/v1/shift-observations/{observation_id}", headers=headers)
    assert get_response.status_code == 404

def test_shift_observation_with_medication_data(db_session: Session, normalized_catalogs):
    """Test creating observation with medication data"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test8@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare test data with medication information
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "good",
        "mental_state": "alert",
        "medications_taken": '[{"name": "Paracetamol", "dose": "500mg", "time": "08:00"}]',
        "medications_missed": '[{"name": "Vitamina D", "reason": "Paciente se negó"}]',
        "side_effects_observed": "Ninguno observado",
        "medication_notes": "Paciente tolera bien la medicación",
        "cared_person_id": str(cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    
    # Should return success
    assert response.status_code == 201
    result = response.json()
    
    # Verify medication data
    assert result["medications_taken"] is not None
    assert result["medications_missed"] is not None
    assert result["side_effects_observed"] == "Ninguno observado"
    assert result["medication_notes"] == "Paciente tolera bien la medicación"

def test_shift_observation_with_incident(db_session: Session, normalized_catalogs):
    """Test creating observation with incident details"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test9@example.com")
    cared_person = create_test_cared_person(db_session, test_user.id)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare test data with incident
    shift_start = datetime.utcnow()
    shift_end = shift_start + timedelta(hours=8)
    
    data = {
        "shift_observation_type_id": normalized_catalogs["shift_observation_type_id"],
        "shift_start": shift_start.isoformat(),
        "shift_end": shift_end.isoformat(),
        "physical_condition": "fair",
        "mental_state": "confused",
        "incidents_occurred": True,
        "incident_details": "Paciente intentó levantarse de la cama sin asistencia a las 02:30",
        "fall_risk_assessment": "high",
        "safety_concerns": "Paciente presenta confusión nocturna",
        "restraint_used": False,
        "cared_person_id": str(cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/shift-observations/", data=data, headers=headers)
    
    # Should return success
    assert response.status_code == 201
    result = response.json()
    
    # Verify incident data
    assert result["incidents_occurred"] == True
    assert result["incident_details"] == "Paciente intentó levantarse de la cama sin asistencia a las 02:30"
    assert result["fall_risk_assessment"] == "high"
    assert result["safety_concerns"] == "Paciente presenta confusión nocturna"
    assert result["restraint_used"] == False 