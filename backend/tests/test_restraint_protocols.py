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
        is_active=True,
        password_hash=password_hash
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_create_restraint_protocol_success(db_session: Session, normalized_catalogs):
    """Test successful creation of a restraint protocol"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test@example.com")
    test_cared_person = CaredPerson(
        first_name="Test",
        last_name="Person",
        care_type_id=normalized_catalogs["care_type_id"],
        user_id=test_user.id
    )
    db_session.add(test_cared_person)
    db_session.commit()
    db_session.refresh(test_cared_person)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data
    start_date = (datetime.now() + timedelta(days=1)).isoformat()
    next_review_date = (datetime.now() + timedelta(days=7)).isoformat()
    
    data = {
        "protocol_type": "physical",
        "title": "Protocolo de sujeción física para prevención de caídas",
        "description": "Protocolo para prevenir caídas durante la noche",
        "justification": "Paciente con historial de caídas nocturnas y riesgo de lesiones graves",
        "risk_assessment": "Alto riesgo de caída durante la noche, especialmente entre 2-4 AM",
        "start_date": start_date,
        "review_frequency": "weekly",
        "next_review_date": next_review_date,
        "responsible_professional": "Dr. María González",
        "professional_license": "MED-12345",
        "supervising_doctor": "Dr. Carlos Rodríguez",
        "status_type_id": normalized_catalogs["status_type_id"],
        "compliance_status": "compliant",
        "notes": "Protocolo implementado con consentimiento familiar",
        "cared_person_id": str(test_cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/restraint-protocols/", data=data, headers=headers)
    
    # Assertions
    assert response.status_code == 201
    result = response.json()
    
    assert result["protocol_type"] == "physical"
    assert result["title"] == "Protocolo de sujeción física para prevención de caídas"
    assert result["justification"] == "Paciente con historial de caídas nocturnas y riesgo de lesiones graves"
    assert result["responsible_professional"] == "Dr. María González"
    assert result["status_type_id"] == normalized_catalogs["status_type_id"]
    assert result["compliance_status"] == "compliant"
    assert result["cared_person_id"] == str(test_cared_person.id)
    assert result["created_by_id"] == str(test_user.id)
    assert "id" in result
    assert "created_at" in result

def test_create_restraint_protocol_invalid_type(db_session: Session, normalized_catalogs):
    """Test creation with invalid protocol type"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test2@example.com")
    test_cared_person = CaredPerson(
        first_name="Test",
        last_name="Person",
        care_type_id=normalized_catalogs["care_type_id"],
        user_id=test_user.id
    )
    db_session.add(test_cared_person)
    db_session.commit()
    db_session.refresh(test_cared_person)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data with invalid protocol type
    start_date = (datetime.now() + timedelta(days=1)).isoformat()
    
    data = {
        "protocol_type": "invalid_type",  # Invalid type
        "title": "Protocolo inválido",
        "justification": "Justificación de prueba",
        "start_date": start_date,
        "responsible_professional": "Dr. Test",
        "cared_person_id": str(test_cared_person.id)
    }
    
    # Make request
    response = client.post("/api/v1/restraint-protocols/", data=data, headers=headers)
    
    # Should return validation error (422 Unprocessable Entity)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        e["loc"][-1] == "protocol_type" and "debe ser uno de" in e["msg"]
        for e in errors
    )

def test_get_restraint_protocols_list(db_session: Session, normalized_catalogs):
    """Test getting list of restraint protocols"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test3@example.com")
    test_cared_person = CaredPerson(
        first_name="Test",
        last_name="Person",
        care_type_id=normalized_catalogs["care_type_id"],
        user_id=test_user.id
    )
    db_session.add(test_cared_person)
    db_session.commit()
    db_session.refresh(test_cared_person)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make request
    response = client.get("/api/v1/restraint-protocols/", headers=headers)
    
    # Should return empty list initially
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 0

def test_get_protocols_by_cared_person(db_session: Session, normalized_catalogs):
    """Test getting protocols for a specific cared person"""
    
    # Create test user and cared person
    test_user = create_test_user(db_session, "test4@example.com")
    test_cared_person = CaredPerson(
        first_name="Test",
        last_name="Person",
        care_type_id=normalized_catalogs["care_type_id"],
        user_id=test_user.id
    )
    db_session.add(test_cared_person)
    db_session.commit()
    db_session.refresh(test_cared_person)
    
    # Create auth token
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make request
    response = client.get(f"/api/v1/restraint-protocols/cared-person/{test_cared_person.id}", headers=headers)
    
    # Should return empty list initially
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 0 