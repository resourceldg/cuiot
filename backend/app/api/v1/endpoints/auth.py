from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserLogin, UserToken, UserResponse, UserWithRoles

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        user = AuthService.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=UserToken)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    try:
        return AuthService.login_user(db, user_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserWithRoles)
def get_current_user(
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    """Get current authenticated user with roles"""
    # Obtener los nombres de los roles activos
    roles = [role.name for role in current_user.roles if hasattr(role, 'is_active') and role.is_active]
    print("DEBUG /auth/me - current_user:", current_user)
    print("DEBUG /auth/me - roles:", roles)
    # Serializar el usuario como UserWithRoles (campos explícitos)
    user_data = UserWithRoles(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        phone=current_user.phone,
        date_of_birth=current_user.date_of_birth,
        gender=current_user.gender,
        professional_license=current_user.professional_license,
        specialization=current_user.specialization,
        experience_years=current_user.experience_years,
        is_freelance=current_user.is_freelance,
        hourly_rate=current_user.hourly_rate,
        availability=current_user.availability,
        is_verified=current_user.is_verified,
        institution_id=current_user.institution_id,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active,
        last_login=current_user.last_login,
        roles=roles
    )
    print("DEBUG /auth/me - user_data:", user_data)
    return user_data

@router.get("/check-email")
def check_email_exists(
    email: str = Query(..., description="Email to check"),
    db: Session = Depends(get_db)
):
    """Check if an email already exists in the system (public endpoint)"""
    from app.models.user import User
    existing_user = db.query(User).filter(User.email == email).first()
    
    return {
        "exists": existing_user is not None,
        "email": email
    }
