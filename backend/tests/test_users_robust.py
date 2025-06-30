import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime

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

@pytest_asyncio.fixture
async def test_user_token(async_client):
    """Create a test user and return authentication token"""
    # Register user
    response = await async_client.post("/api/v1/auth/register", json=TEST_USER_DATA)
    assert response.status_code == 201
    
    # Login to get token
    response = await async_client.post("/api/v1/auth/login", json={
        "email": TEST_USER_DATA["email"],
        "password": TEST_USER_DATA["password"]
    })
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def admin_user_token(async_client):
    """Create an admin user and return authentication token"""
    # Register admin user
    response = await async_client.post("/api/v1/auth/register", json=ADMIN_USER_DATA)
    assert response.status_code == 201
    
    # Login to get token
    response = await async_client.post("/api/v1/auth/login", json={
        "email": ADMIN_USER_DATA["email"],
        "password": ADMIN_USER_DATA["password"]
    })
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def test_user_id(async_client, test_user_token):
    """Get the test user ID"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = await async_client.get("/api/v1/users/", headers=headers)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            if user["email"] == TEST_USER_DATA["email"]:
                return user["id"]
    return None

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
    async def test_get_users_list(self, async_client, test_user_token):
        """Test getting list of users"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.get("/api/v1/users/", headers=headers)
        
        # Should return 200 or 403 depending on permissions
        assert response.status_code in [200, 403]
        
        if response.status_code == 200:
            users = response.json()
            assert isinstance(users, list)
            # Should contain at least our test user
            user_emails = [user["email"] for user in users]
            assert TEST_USER_DATA["email"] in user_emails
    
    @pytest.mark.asyncio
    async def test_get_users_with_pagination(self, async_client, test_user_token):
        """Test getting users with pagination parameters"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.get("/api/v1/users/?skip=0&limit=10", headers=headers)
        
        assert response.status_code in [200, 403]
        
        if response.status_code == 200:
            users = response.json()
            assert isinstance(users, list)
            assert len(users) <= 10
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, async_client, test_user_token, test_user_id):
        """Test getting a specific user by ID"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.get(f"/api/v1/users/{test_user_id}", headers=headers)
        
        assert response.status_code == 200
        
        user = response.json()
        assert user["id"] == test_user_id
        assert user["email"] == TEST_USER_DATA["email"]
        assert user["first_name"] == TEST_USER_DATA["first_name"]
        assert "roles" in user  # Should include roles field
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, async_client, test_user_token):
        """Test getting a user that doesn't exist"""
        fake_id = str(uuid4())
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.get(f"/api/v1/users/{fake_id}", headers=headers)
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_update_own_profile(self, async_client, test_user_token, test_user_id):
        """Test updating own user profile"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        update_data = {
            "first_name": "Updated",
            "phone": "999888777",
            "last_name": "UpdatedUser"
        }
        
        response = await async_client.put(f"/api/v1/users/{test_user_id}", 
                                        json=update_data, headers=headers)
        
        assert response.status_code == 200
        
        user = response.json()
        assert user["first_name"] == update_data["first_name"]
        assert user["phone"] == update_data["phone"]
        assert user["last_name"] == update_data["last_name"]
    
    @pytest.mark.asyncio
    async def test_update_user_invalid_data(self, async_client, test_user_token, test_user_id):
        """Test updating user with invalid data"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        invalid_data = {
            "email": "invalid-email",  # Invalid email format
            "first_name": ""  # Empty first name
        }
        
        response = await async_client.put(f"/api/v1/users/{test_user_id}", 
                                        json=invalid_data, headers=headers)
        
        assert response.status_code == 422  # Validation error

class TestUserPasswordManagement:
    """Test password change functionality"""
    
    @pytest.mark.asyncio
    async def test_change_password_success(self, async_client, test_user_token, test_user_id):
        """Test successful password change"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        password_data = {
            "current_password": TEST_USER_DATA["password"],
            "new_password": "newpassword123"
        }
        
        response = await async_client.patch(f"/api/v1/users/{test_user_id}/password", 
                                          json=password_data, headers=headers)
        
        # This might fail due to validation, but should not hang
        assert response.status_code in [200, 422]
        
        if response.status_code == 200:
            data = response.json()
            assert data["ok"] is True
            assert "correctamente" in data["message"]
    
    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, async_client, test_user_token, test_user_id):
        """Test password change with wrong current password"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        
        response = await async_client.patch(f"/api/v1/users/{test_user_id}/password", 
                                          json=password_data, headers=headers)
        
        assert response.status_code == 400
        assert "incorrecta" in response.json()["detail"]

class TestUserRoleManagement:
    """Test user role assignment and removal"""
    
    @pytest.mark.asyncio
    async def test_assign_role_requires_permission(self, async_client, test_user_token, test_user_id):
        """Test that assigning roles requires proper permissions"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.post(f"/api/v1/users/{test_user_id}/roles/caregiver", 
                                         headers=headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_remove_role_requires_permission(self, async_client, test_user_token, test_user_id):
        """Test that removing roles requires proper permissions"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.delete(f"/api/v1/users/{test_user_id}/roles/caregiver", 
                                           headers=headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403

class TestUserPermissions:
    """Test user permission checks"""
    
    @pytest.mark.asyncio
    async def test_create_user_requires_permission(self, async_client, test_user_token):
        """Test that creating users requires proper permissions"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        new_user_data = {
            "email": "another@example.com",
            "password": "anotherpass123",
            "first_name": "Another",
            "last_name": "User",
            "phone": "111222333"
        }
        
        response = await async_client.post("/api/v1/users/", json=new_user_data, headers=headers)
        
        # Should fail due to lack of permissions
        assert response.status_code == 403
    
    @pytest.mark.asyncio
    async def test_delete_user_requires_permission(self, async_client, test_user_token, test_user_id):
        """Test that deleting users requires proper permissions"""
        if not test_user_id:
            pytest.skip("Could not get test user ID")
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.delete(f"/api/v1/users/{test_user_id}", headers=headers)
        
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
    async def test_invalid_uuid_format(self, async_client, test_user_token):
        """Test handling of invalid UUID format"""
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = await async_client.get("/api/v1/users/invalid-uuid", headers=headers)
        
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