from datetime import datetime, timedelta
from typing import Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserLogin, UserToken
from app.core.config import settings
from app.core.database import get_db

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

class AuthService:
    """Authentication and authorization service"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = AuthService.get_password_hash(user_data.password)
        
        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            date_of_birth=user_data.date_of_birth,
            gender=user_data.gender,
            professional_license=user_data.professional_license,
            specialization=user_data.specialization,
            experience_years=user_data.experience_years,
            is_freelance=user_data.is_freelance,
            hourly_rate=user_data.hourly_rate,
            availability=user_data.availability,
            is_verified=user_data.is_verified,
            institution_id=user_data.institution_id
        )
        
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User creation failed: {str(e)}"
            )
    
    @staticmethod
    def login_user(db: Session, user_data: UserLogin) -> UserToken:
        """Login a user and return access token"""
        user = AuthService.authenticate_user(db, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Obtener roles activos del usuario
        roles = [role.name for role in user.roles if role.is_active]
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id), "roles": roles}, expires_delta=access_token_expires
        )
        
        return UserToken(access_token=access_token, user=user)
    
    @staticmethod
    def get_current_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """Get current authenticated user"""
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    @staticmethod
    def get_current_active_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """Get current active user"""
        user = AuthService.get_current_user(db, credentials)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return user
    
    @staticmethod
    def check_permission(user: User, permission: str, db) -> bool:
        """Check if user has specific permission"""
        return user.has_permission(permission, db)
    
    @staticmethod
    def require_permission(permission: str):
        """Decorator to require specific permission"""
        def permission_checker(current_user: User = Depends(AuthService.get_current_active_user), db: Session = Depends(get_db)):
            if not AuthService.check_permission(current_user, permission, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            return current_user
        return permission_checker
    
    @staticmethod
    def get_current_active_user_optional(
        db: Session = Depends(get_db),
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Optional[User]:
        """Get current active user if token is present, else return None"""
        if credentials is None:
            return None
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        if payload is None:
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None or not user.is_active:
            return None
        return user
    
    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> Optional[User]:
        payload = AuthService.verify_token(token)
        if payload is None:
            return None
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        return user
