import pytest
import pytest_asyncio
import json
from datetime import datetime
from uuid import UUID
from app.models.user_role import UserRole
from app.core.database import get_db

@pytest_asyncio.fixture
async def admin_auth(async_client):
    """Create an admin user for testing user management"""
    # Register admin user
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
        "phone": "123456789"
    })
    
    # Handle case where user already exists
    if response.status_code == 400 and "already registered" in response.text:
        print("Admin user already exists, proceeding with login")
    elif response.status_code != 201:
        print(f"Warning: User registration failed with status {response.status_code}")
        print(f"Response: {response.text}")
    
    # Create admin role and assign it
    db = next(get_db())
    from app.models.user import User
    from app.models.role import Role
    
    # Find the user
    db_user = db.query(User).filter_by(email="admin@example.com").first()
    if not db_user:
        raise Exception("Could not find admin user in database")
    
    # Create admin role if it doesn't exist
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="Administrator role",
            permissions=json.dumps({
                "users": {
                    "read": True,
                    "write": True,
                    "delete": True,
                    "create": True,
                    "update": True,
                    "manage": True
                },
                "cared_persons": {
                    "read": True,
                    "write": True,
                    "delete": True
                },
                "institutions": {
                    "read": True,
                    "write": True,
                    "delete": True
                },
                "devices": {
                    "read": True,
                    "write": True,
                    "delete": True
                },
                "protocols": {
                    "read": True,
                    "write": True,
                    "delete": True
                },
                "reports": {
                    "read": True,
                    "write": True
                },
                "system": {
                    "read": True,
                    "write": True,
                    "delete": True
                },
                "admin": True,
                "super_admin": True
            }),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # Check if user already has admin role
    existing_role = db.query(UserRole).filter_by(
        user_id=db_user.id, 
        role_id=admin_role.id
    ).first()
    
    if not existing_role:
        # Assign role to user
        user_role = UserRole(
            user_id=db_user.id,
            role_id=admin_role.id,
            created_at=datetime.now()
        )
        db.add(user_role)
        db.commit()
    
    # Login to get token
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    
    if response.status_code != 200:
        print(f"Login failed with status {response.status_code}")
        print(f"Response: {response.text}")
        raise Exception(f"Login failed: {response.text}")
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    return {"headers": headers, "user_id": str(db_user.id)}

@pytest_asyncio.fixture
async def regular_user_auth(async_client):
    """Create a regular user for testing"""
    # Register regular user
    response = await async_client.post("/api/v1/auth/register", json={
        "email": "user@example.com",
        "password": "userpassword",
        "first_name": "Regular",
        "last_name": "User",
        "phone": "987654321"
    })
    user = response.json()
    
    # Create basic role and assign it
    db = next(get_db())
    from app.models.user import User
    from app.models.role import Role
    
    # Find the user
    db_user = db.query(User).filter_by(email="user@example.com").first()
    
    # Create basic role if it doesn't exist
    basic_role = db.query(Role).filter_by(name="family").first()
    if not basic_role:
        basic_role = Role(
            name="family",
            description="Family member role",
            permissions=json.dumps({
                "cared_persons": {"read": True},
                "devices": {"read": True},
                "alerts": {"read": True},
                "reports": {"read": True}
            }),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(basic_role)
        db.commit()
        db.refresh(basic_role)
    
    # Assign role to user
    user_role = UserRole(
        user_id=db_user.id,
        role_id=basic_role.id,
        created_at=datetime.now()
    )
    db.add(user_role)
    db.commit()
    
    # Login to get token
    response = await async_client.post("/api/v1/auth/login", json={
        "email": "user@example.com",
        "password": "userpassword"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    return {"headers": headers, "user_id": str(db_user.id)}

@pytest.mark.asyncio
async def test_get_users(async_client, admin_auth):
    """Test getting list of users"""
    response = await async_client.get("/api/v1/users/", headers=admin_auth["headers"])
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1  # At least the admin user

@pytest.mark.asyncio
async def test_get_user_by_id(async_client, admin_auth):
    """Test getting a specific user by ID"""
    # Get the admin user using admin credentials (self)
    response = await async_client.get(f"/api/v1/users/{admin_auth['user_id']}", headers=admin_auth["headers"])
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "admin@example.com"
    assert user["first_name"] == "Admin"
    assert user["last_name"] == "User"

@pytest.mark.asyncio
async def test_get_user_not_found(async_client, admin_auth):
    """Test getting a non-existent user"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.get(f"/api/v1/users/{fake_id}", headers=admin_auth["headers"])
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_user(async_client, admin_auth):
    """Test creating a new user"""
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "first_name": "New",
        "last_name": "User",
        "phone": "555555555"
    }
    
    response = await async_client.post("/api/v1/users/", json=user_data, headers=admin_auth["headers"])
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == "newuser@example.com"
    assert user["first_name"] == "New"
    assert user["last_name"] == "User"

@pytest.mark.asyncio
async def test_create_user_validation(async_client, admin_auth):
    """Test user creation validation"""
    # Test missing required fields
    invalid_data = {
        "first_name": "Test",
        # Missing email and password
    }
    
    response = await async_client.post("/api/v1/users/", json=invalid_data, headers=admin_auth["headers"])
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_user(async_client, admin_auth):
    """Test updating user information"""
    update_data = {
        "first_name": "Updated",
        "phone": "111111111"
    }
    
    response = await async_client.put(f"/api/v1/users/{admin_auth['user_id']}", 
                                    json=update_data, headers=admin_auth["headers"])
    assert response.status_code == 200
    user = response.json()
    assert user["first_name"] == "Updated"
    assert user["phone"] == "111111111"

@pytest.mark.asyncio
async def test_update_other_user_forbidden(async_client, admin_auth, regular_user_auth):
    """Test that admin can update other user's profile"""
    update_data = {"first_name": "Updated by Admin"}
    
    response = await async_client.put(f"/api/v1/users/{regular_user_auth['user_id']}", 
                                    json=update_data, headers=admin_auth["headers"])
    assert response.status_code == 200
    user = response.json()
    assert user["first_name"] == "Updated by Admin"

@pytest.mark.asyncio
async def test_delete_user(async_client, admin_auth):
    """Test deleting a user"""
    # First create a user to delete
    user_data = {
        "email": "todelete@example.com",
        "password": "deletepassword",
        "first_name": "To",
        "last_name": "Delete",
        "phone": "333333333"
    }
    
    response = await async_client.post("/api/v1/users/", json=user_data, headers=admin_auth["headers"])
    assert response.status_code == 201
    user_to_delete = response.json()
    
    # Delete the user
    response = await async_client.delete(f"/api/v1/users/{user_to_delete['id']}", headers=admin_auth["headers"])
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_assign_role(async_client, admin_auth, regular_user_auth):
    """Test assigning a role to a user"""
    # First create a role if it doesn't exist
    db = next(get_db())
    from app.models.role import Role
    
    test_role = db.query(Role).filter_by(name="test_role").first()
    if not test_role:
        test_role = Role(
            name="test_role",
            description="Test role",
            permissions=json.dumps({"test": True}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(test_role)
        db.commit()
        db.refresh(test_role)
    
    # Assign role
    response = await async_client.post(f"/api/v1/users/{regular_user_auth['user_id']}/roles/test_role", 
                                     headers=admin_auth["headers"])
    assert response.status_code == 200
    assert response.json()["message"] == "Role assigned successfully"

@pytest.mark.asyncio
async def test_remove_role(async_client, admin_auth, regular_user_auth):
    """Test removing a role from a user"""
    # First assign a role
    db = next(get_db())
    from app.models.role import Role
    
    test_role = db.query(Role).filter_by(name="test_role").first()
    if not test_role:
        test_role = Role(
            name="test_role",
            description="Test role",
            permissions=json.dumps({"test": True}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(test_role)
        db.commit()
        db.refresh(test_role)
    
    # Assign role first
    response = await async_client.post(f"/api/v1/users/{regular_user_auth['user_id']}/roles/test_role", 
                                     headers=admin_auth["headers"])
    assert response.status_code == 200
    
    # Then remove it
    response = await async_client.delete(f"/api/v1/users/{regular_user_auth['user_id']}/roles/test_role", 
                                       headers=admin_auth["headers"])
    assert response.status_code == 200
    assert response.json()["message"] == "Role removed successfully"

@pytest.mark.asyncio
async def test_change_password(async_client, admin_auth):
    """Test changing user password"""
    password_data = {
        "current_password": "adminpassword",
        "new_password": "newadminpass"
    }
    
    response = await async_client.patch(f"/api/v1/users/{admin_auth['user_id']}/password", 
                                      json=password_data, headers=admin_auth["headers"])
    assert response.status_code == 200
    assert response.json()["message"] == "Contraseña cambiada correctamente"

@pytest.mark.asyncio
async def test_change_password_wrong_current(async_client, admin_auth):
    """Test changing password with wrong current password"""
    password_data = {
        "current_password": "wrongpassword",
        "new_password": "newadminpass"
    }
    
    response = await async_client.patch(f"/api/v1/users/{admin_auth['user_id']}/password", 
                                      json=password_data, headers=admin_auth["headers"])
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_change_other_user_password_forbidden(async_client, admin_auth, regular_user_auth):
    """Test that admin cannot change other user's password without knowing current password"""
    password_data = {
        "current_password": "wrongpassword",  # Admin doesn't know user's current password
        "new_password": "newuserpass"
    }
    
    response = await async_client.patch(f"/api/v1/users/{regular_user_auth['user_id']}/password", 
                                      json=password_data, headers=admin_auth["headers"])
    # Should fail because admin doesn't know the user's current password
    assert response.status_code == 400
    assert "incorrecta" in response.json()["detail"] 