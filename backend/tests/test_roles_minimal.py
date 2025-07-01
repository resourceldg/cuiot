import pytest
import pytest_asyncio
from datetime import datetime
import json
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.database import get_db
from passlib.hash import bcrypt
import uuid
from sqlalchemy.orm import Session
import os
from uuid import UUID

@pytest_asyncio.fixture
def admin_user_data():
    return {
        "email": "admin_minimal@example.com",
        "username": "admin_minimal",
        "password": "adminpass123",
        "first_name": "Admin",
        "last_name": "User"
    }

@pytest_asyncio.fixture
def user_data():
    return {
        "email": "roleuser_minimal@example.com",
        "username": "roleuser_minimal",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.mark.asyncio
async def test_assign_and_remove_role_minimal(async_client, admin_user_data, user_data, db_session):
    try:
        # --- Limpiar la base de datos antes del test ---
        db: Session = db_session
        db.query(UserRole).delete()
        db.query(Role).delete()
        db.query(User).delete()
        db.commit()
        
        # --- Crear usuario admin vía API (sin token, primer usuario) ---
        admin_create_data = {
            "email": admin_user_data["email"],
            "username": admin_user_data["username"],
            "password": admin_user_data["password"],
            "first_name": admin_user_data["first_name"],
            "last_name": admin_user_data["last_name"]
        }
        admin_create_resp = await async_client.post("/api/v1/users/", json=admin_create_data)
        assert admin_create_resp.status_code == 201, f"ADMIN CREATE FAIL: Status: {admin_create_resp.status_code}, Body: {admin_create_resp.json()}"
        admin_id = admin_create_resp.json()["id"]
        # --- Asignar rol admin directamente en la base de datos ---
        admin_role = db.query(Role).filter_by(name="admin").first()
        if not admin_role:
            now = datetime.utcnow()
            admin_role = Role(
                id=uuid.uuid4(),
                name="admin",
                description="Rol admin para test minimal",
                permissions=json.dumps({"users": {"write": True, "read": True}}),
                is_system=True,
                is_active=True,
                created_at=now,
                updated_at=now
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        user_role = UserRole(
            user_id=UUID(admin_id),
            role_id=admin_role.id,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(user_role)
        db.commit()
        
        # --- Login admin vía API ---
        login_resp = await async_client.post("/api/v1/auth/login", json={"email": admin_user_data["email"], "password": admin_user_data["password"]})
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        admin_auth = {"Authorization": f"Bearer {token}"}
        
        # --- Crear usuario destino vía API ---
        try:
            create_user = await async_client.post("/api/v1/users/", json=user_data, headers=admin_auth)
            try:
                detail = create_user.json()
            except Exception:
                detail = create_user.text
            print(f"USER CREATE: status={create_user.status_code}, body={detail}, payload={user_data}")
            assert create_user.status_code == 201, f"USER CREATE FAIL: Status: {create_user.status_code}, Body: {detail}, Payload: {user_data}"
        except Exception as e:
            print(f"EXCEPTION in USER CREATE: {e}")
            raise
        user_id = detail["id"] if isinstance(detail, dict) and "id" in detail else None
        print(f"USER DESTINO ID: {user_id}")
        assert user_id is not None, f"El usuario destino no fue creado correctamente: {detail}"
        
        # --- Login usuario admin para obtener token actualizado ---
        try:
            login_data = {"email": admin_user_data["email"], "password": admin_user_data["password"]}
            login_resp = await async_client.post("/api/v1/auth/login", json=login_data)
            try:
                login_detail = login_resp.json()
            except Exception:
                login_detail = login_resp.text
            print(f"ADMIN LOGIN: status={login_resp.status_code}, body={login_detail}, payload={login_data}")
            assert login_resp.status_code == 200, f"ADMIN LOGIN FAIL: Status: {login_resp.status_code}, Body: {login_detail}, Payload: {login_data}"
            admin_token = login_detail["access_token"]
            admin_auth = {"Authorization": f"Bearer {admin_token}"}
        except Exception as e:
            print(f"EXCEPTION in ADMIN LOGIN: {e}")
            raise
        
        # --- Crear rol 'test_role' vía API ---
        role_data = {
            "name": "test_role",
            "description": "Rol de prueba para test minimal",
            "permissions": json.dumps({"users": {"read": True}}),
            "is_system": False
        }
        create_role_resp = await async_client.post("/api/v1/users/roles", json=role_data, headers=admin_auth)
        assert create_role_resp.status_code in (200, 201)
        
        # --- Asignar rol vía API ---
        try:
            print(f"ASSIGN ROLE: user_id={user_id}, admin_auth={admin_auth}")
            assign_role_payload = {"role_name": "test_role"}
            headers = {**admin_auth, "Content-Type": "application/json"}
            assign_role = await async_client.post(f"/api/v1/users/{user_id}/assign-role", json=assign_role_payload, headers=headers)
            try:
                assign_detail = assign_role.json()
            except Exception:
                assign_detail = assign_role.text
            print(f"ASSIGN ROLE: status={assign_role.status_code}, body={assign_detail}, payload={assign_role_payload}")
            if assign_role.status_code == 422:
                print(f"422 ERROR BODY: {assign_role.text}")
                assert False, f"422 ERROR BODY: {assign_role.text}"
            assert assign_role.status_code == 200, f"ASSIGN ROLE FAIL: Status: {assign_role.status_code}, Body: {assign_detail}, Payload: {assign_role_payload}"
        except Exception as e:
            print(f"EXCEPTION in ASSIGN ROLE: {e}")
            raise
        
        # --- Remover rol con admin ---
        remove_resp = await async_client.delete(f"/api/v1/users/{user_id}/roles/test_role", headers=admin_auth)
        assert remove_resp.status_code in (200, 204)
    except Exception as e:
        os.makedirs("backend/tests", exist_ok=True)
        with open("backend/tests/user_create_error.json", "w") as f:
            f.write(str(e))
        raise 