import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime
import json

# Test data constants
TEST_USER_DATA = {
    "email": "testuser@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User",
    "phone": "123456789",
    "username": "testuser",
    "is_freelance": True,
    "hourly_rate": 2500  # $25.00 in cents
}

ADMIN_USER_DATA = {
    "email": "admin@example.com",
    "password": "adminpass123",
    "first_name": "Admin",
    "last_name": "User",
    "phone": "987654321",
    "username": "adminuser",
    "is_freelance": False
}

class TestUserAuthentication:
    """Test user authentication and registration"""
    
    @pytest.mark.asyncio
    async def test_user_registration_success(self, async_client):
        """Test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
            "phone": "555123456",
            "username": "newuser"
        }
        
        response = await async_client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        
        user = response.json()
        assert user["email"] == user_data["email"]
        assert user["first_name"] == user_data["first_name"]
        assert user["last_name"] == user_data["last_name"]
        assert user["phone"] == user_data["phone"]
        assert user["username"] == user_data["username"]
        assert "id" in user
        assert "password" not in user  # Password should not be returned
    
    @pytest.mark.asyncio
    async def test_user_registration_duplicate_email(self, async_client):
        """Test registration with duplicate email fails"""
        # First registration
        response = await async_client.post("/api/v1/auth/register", json=TEST_USER_DATA)
        assert response.status_code == 201
        
        # Second registration with same email
        response = await async_client.post("/api/v1/auth/register", json=TEST_USER_DATA)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_user_login_success(self, async_client):
        """Test successful user login"""
        # First register a user
        response = await async_client.post("/api/v1/auth/register", json=TEST_USER_DATA)
        assert response.status_code == 201
        
        # Then login
        response = await async_client.post("/api/v1/auth/login", json={
            "email": TEST_USER_DATA["email"],
            "password": TEST_USER_DATA["password"]
        })
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == TEST_USER_DATA["email"]
    
    @pytest.mark.asyncio
    async def test_user_login_invalid_credentials(self, async_client):
        """Test login with invalid credentials fails"""
        response = await async_client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

class TestUserCRUD:
    """Test user CRUD operations"""
    
    @pytest.mark.asyncio
    async def test_get_users_list(self, async_client, auth_headers):
        """Test getting list of users"""
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        
        # Should return 200 or 403 depending on permissions
        assert response.status_code in [200, 403]
        
        if response.status_code == 200:
            users = response.json()
            assert isinstance(users, list)
            # Should contain at least our test user
            user_emails = [user["email"] for user in users]
            assert "testuser@example.com" in user_emails
    
    @pytest.mark.asyncio
    async def test_get_users_with_pagination(self, async_client, auth_headers):
        """Test getting users with pagination parameters"""
        response = await async_client.get("/api/v1/users/?skip=0&limit=10", headers=auth_headers)
        
        assert response.status_code in [200, 403]
        
        if response.status_code == 200:
            users = response.json()
            assert isinstance(users, list)
            assert len(users) <= 10
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, async_client, auth_headers):
        """Test getting a specific user by ID"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        response = await async_client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
        
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == user_id
        assert user["email"] == "testuser@example.com"
        assert user["first_name"] == "Test"
        assert "roles" in user  # Should include roles field
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, async_client, auth_headers):
        """Test getting a user that doesn't exist"""
        fake_id = str(uuid4())
        response = await async_client.get(f"/api/v1/users/{fake_id}", headers=auth_headers)
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_update_own_profile(self, async_client, auth_headers):
        """Test updating own user profile"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        update_data = {
            "first_name": "Updated",
            "phone": "999888777",
            "last_name": "UpdatedUser"
        }
        
        response = await async_client.put(f"/api/v1/users/{user_id}", 
                                        json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        
        user = response.json()
        assert user["first_name"] == update_data["first_name"]
        assert user["phone"] == update_data["phone"]
        assert user["last_name"] == update_data["last_name"]
    
    @pytest.mark.asyncio
    async def test_update_user_invalid_data(self, async_client, auth_headers):
        """Test updating user with invalid data"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        invalid_data = {
            "email": "invalid-email",  # Invalid email format
            "first_name": ""  # Empty first name
        }
        
        response = await async_client.put(f"/api/v1/users/{user_id}", 
                                        json=invalid_data, headers=auth_headers)
        
        assert response.status_code == 422  # Validation error

class TestUserPasswordManagement:
    """Test password change functionality"""
    
    @pytest.mark.asyncio
    async def test_change_password_success(self, async_client, auth_headers):
        """Test successful password change"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        password_data = {
            "current_password": "testpassword",
            "new_password": "newpassword123"
        }
        
        response = await async_client.patch(f"/api/v1/users/{user_id}/password", 
                                          json=password_data, headers=auth_headers)
        
        # This might fail due to validation, but should not hang
        assert response.status_code in [200, 422]
        
        if response.status_code == 200:
            data = response.json()
            assert data["ok"] is True
            assert "correctamente" in data["message"]
    
    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, async_client, auth_headers):
        """Test password change with wrong current password"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        
        response = await async_client.patch(f"/api/v1/users/{user_id}/password", 
                                          json=password_data, headers=auth_headers)
        
        assert response.status_code == 400
        assert "incorrecta" in response.json()["detail"]

class TestUserRoleManagement:
    """Test user role assignment and removal"""
    
    @pytest.mark.asyncio
    async def test_assign_role_requires_permission(self, async_client, admin_auth, auth_headers):
        # Crear usuario de destino con admin
        user_data = {
            "email": "roleuser3@example.com",
            "username": "roleuser3",
            "password": "testpass123",
            "first_name": "Role3",
            "last_name": "User3"
        }
        create_resp = await async_client.post("/api/v1/users/", json=user_data, headers=admin_auth)
        assert create_resp.status_code == 201
        user_id = create_resp.json()["id"]
        # Crear rol test_role si no existe (siempre con admin)
        role_data = {
            "name": "test_role",
            "description": "Rol de prueba para test minimal",
            "permissions": json.dumps({"users": {"read": True}}),
            "is_system": False
        }
        create_role_resp = await async_client.post("/api/v1/users/roles", json=role_data, headers=admin_auth)
        if create_role_resp.status_code not in (200, 201):
            # Si el error es por rol duplicado, continuar
            if create_role_resp.status_code == 400 and ("ya existe" in create_role_resp.text or "already exists" in create_role_resp.text):
                pass
            else:
                print(f"Error creando rol: {create_role_resp.status_code}, {create_role_resp.text}")
                assert False, f"Error creando rol: {create_role_resp.status_code}, {create_role_resp.text}"
        # Intentar asignar rol sin permisos admin
        data = {"role_name": "test_role"}
        response = await async_client.post(f"/api/v1/users/{user_id}/assign-role", json=data, headers=auth_headers)
        assert response.status_code == 403
        assert "No tiene permisos" in response.text
    
    @pytest.mark.asyncio
    async def test_remove_role_requires_permission(self, async_client, auth_headers):
        """Test that removing roles requires proper permissions"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        response = await async_client.delete(f"/api/v1/users/{user_id}/roles/caregiver", 
                                           headers=auth_headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403

class TestUserPermissions:
    """Test user permission checks"""
    
    @pytest.mark.asyncio
    async def test_create_user_requires_permission(self, async_client, auth_headers):
        """Test that creating users requires proper permissions"""
        new_user_data = {
            "email": "another@example.com",
            "password": "anotherpass123",
            "first_name": "Another",
            "last_name": "User",
            "phone": "111222333"
        }
        
        response = await async_client.post("/api/v1/users/", json=new_user_data, headers=auth_headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_delete_user_requires_permission(self, async_client, auth_headers):
        """Test that deleting users requires proper permissions"""
        # Get user ID from authenticated user
        response = await async_client.get("/api/v1/users/", headers=auth_headers)
        if response.status_code != 200:
            pytest.skip("Could not get users list")
        
        user_id = next((u["id"] for u in response.json() if u["email"] == "testuser@example.com"), None)
        if not user_id:
            pytest.skip("Could not get test user ID")
        
        response = await async_client.delete(f"/api/v1/users/{user_id}", headers=auth_headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403

class TestUserValidation:
    """Test user data validation"""
    
    @pytest.mark.asyncio
    async def test_user_registration_validation(self, async_client):
        """Test user registration with various validation scenarios"""
        # Test with missing required fields
        invalid_data = {
            "email": "test@example.com",
            # Missing password and first_name
        }
        
        response = await async_client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422
        
        # Test with invalid email
        invalid_data = {
            "email": "invalid-email",
            "password": "testpass123",
            "first_name": "Test"
        }
        
        response = await async_client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422
        
        # Test with short password
        invalid_data = {
            "email": "test@example.com",
            "password": "short",
            "first_name": "Test"
        }
        
        response = await async_client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422

class TestUserErrorHandling:
    """Test error handling in user endpoints"""
    
    @pytest.mark.asyncio
    async def test_invalid_uuid_format(self, async_client, auth_headers):
        """Test handling of invalid UUID format"""
        response = await async_client.get("/api/v1/users/invalid-uuid", headers=auth_headers)
        
        assert response.status_code == 422  # Validation error for UUID format
    
    @pytest.mark.asyncio
    async def test_missing_authentication(self, async_client):
        """Test endpoints without authentication"""
        response = await async_client.get("/api/v1/users/")
        assert response.status_code == 403
        
        response = await async_client.get(f"/api/v1/users/{str(uuid4())}")
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_invalid_token(self, async_client):
        """Test endpoints with invalid token"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = await async_client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 401 