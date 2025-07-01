import pytest
import pytest_asyncio
import json
from datetime import datetime
from app.models.user_role import UserRole
from app.core.database import get_db

@pytest_asyncio.fixture
async def caregiver_auth(async_client, db_session):
    # Registrar usuario con rol caregiver
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "caregiver@example.com",
        "password": "testpassword",
        "first_name": "Care",
        "last_name": "Giver",
        "phone": "123456789"
    })
    user = response.json()
    
    # Asignar rol 'caregiver' usando acceso directo a la BD
    db = db_session
    from app.models.user import User
    from app.models.role import Role
    
    # Buscar el usuario
    db_user = db.query(User).filter_by(email="caregiver@example.com").first()
    
    # Buscar o crear el rol caregiver
    role = db.query(Role).filter_by(name="caregiver").first()
    if not role:
        # Crear el rol si no existe
        permissions_dict = {
            "cared_persons": {"read": True, "write": True},
            "devices": {"read": True, "write": True},
            "protocols": {"read": True, "write": True},
            "reports": {"read": True},
            "alerts": {"read": True, "write": True}
        }
        now = datetime.now()
        role = Role(
            name="caregiver",
            description="Cuidador profesional con acceso a personas bajo su cuidado",
            permissions=json.dumps(permissions_dict),
            is_system=True,
            created_at=now,
            updated_at=now
        )
        db.add(role)
        db.commit()
        db.refresh(role)
    
    # Asignar el rol al usuario
    success = UserRole.assign_role_to_user(db, db_user.id, "caregiver")
    if not success:
        # Si falla, crear la asignación manualmente
        user_role = UserRole(user_id=db_user.id, role_id=role.id)
        db.add(user_role)
        db.commit()
    
    # Verificar que se asignó correctamente
    user_roles = db.query(UserRole).filter_by(user_id=db_user.id).all()
    role_ids = [ur.role_id for ur in user_roles]
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    print(f"Usuario {db_user.email} tiene roles: {[r.name for r in roles]}")
    
    # Login para obtener token
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "caregiver@example.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, str(db_user.id)

@pytest.mark.asyncio
async def test_referral_code_generation(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    code_data = {
        "referrer_type": "caregiver",
        "referrer_id": user_id,
        "custom_code": "TEST123"
    }
    response = await async_client.post("/api/v1/referrals/generate-code", json=code_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["referral_code"] == "TEST123"
    assert data["referrer_type"] == "caregiver"
    assert data["referrer_id"] == user_id

@pytest.mark.asyncio
async def test_referral_code_validation(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    
    # Validar un código que no existe (debería devolver False)
    validation_data = {
        "referral_code": "INVALID123",
        "referred_email": "test@example.com"
    }
    response = await async_client.post("/api/v1/referrals/validate", json=validation_data)
    assert response.status_code == 200
    data = response.json()
    assert "is_valid" in data
    # El código no existe, así que debería ser inválido
    assert data["is_valid"] == False

@pytest.mark.asyncio
async def test_referral_creation(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    referral_data = {
        "referrer_type": "caregiver",
        "referrer_id": user_id,
        "referred_email": "newuser@example.com",
        "referral_code": "TEST123",
        "commission_amount": 50.0
    }
    response = await async_client.post("/api/v1/referrals/create", json=referral_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["referrer_type"] == "caregiver"
    assert data["referrer_id"] == user_id
    assert data["referred_email"] == "newuser@example.com"

@pytest.mark.asyncio
async def test_get_my_referrals(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    response = await async_client.get("/api/v1/referrals/my-referrals", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_my_commissions(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    response = await async_client.get("/api/v1/referrals/my-commissions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_referral_stats(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    response = await async_client.get("/api/v1/referrals/stats", headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Verificar que contiene los campos esperados según la respuesta real de la API
    assert "total_referrals" in data
    assert "converted_referrals" in data  # Cambiado de 'successful_referrals'
    assert "total_commissions_paid" in data  # Campo correcto según el servicio
    assert "avg_commission_amount" in data

@pytest.mark.asyncio
async def test_referral_not_found(async_client, caregiver_auth):
    headers, user_id = caregiver_auth
    # Intentar acceder a un referral que no existe
    response = await async_client.get("/api/v1/referrals/my-referrals?skip=1000&limit=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0 