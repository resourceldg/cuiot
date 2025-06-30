from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserUpdate, UserWithRoles

class UserService:
    """User management service"""
    
    @staticmethod
    def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        institution_id: Optional[int] = None,
        is_freelance: Optional[bool] = None
    ) -> List[User]:
        """Get list of users with optional filters"""
        # Use simple query without eager loading to avoid hangs
        query = db.query(User)
        
        if institution_id is not None:
            query = query.filter(User.institution_id == institution_id)
        
        if is_freelance is not None:
            query = query.filter(User.is_freelance == is_freelance)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        from app.services.auth import AuthService
        
        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, user_data.email)
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
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            from app.services.auth import AuthService
            update_data["hashed_password"] = AuthService.get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User update failed"
            )
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        """Delete a user"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            db.delete(user)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete user with existing relationships"
            )
    
    @staticmethod
    def assign_role(db: Session, user_id: UUID, role_name: str) -> bool:
        """Assign a role to a user"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        return UserRole.assign_role_to_user(db, user_id, role_name)
    
    @staticmethod
    def remove_role(db: Session, user_id: UUID, role_name: str) -> bool:
        """Remove a role from a user"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserRole.remove_role_from_user(db, user_id, role_name)
    
    @staticmethod
    def get_user_with_roles(db: Session, user_id: UUID) -> Optional[UserWithRoles]:
        """Get user with role information"""
        # Use explicit join to avoid lazy loading issues
        from sqlalchemy.orm import joinedload
        
        user = db.query(User).options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        ).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        # Get role names from the loaded relationships
        roles = [user_role.role.name for user_role in user.user_roles if user_role.role]
        
        # Convert user to dict and add roles
        user_dict = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'professional_license': user.professional_license,
            'specialization': user.specialization,
            'experience_years': user.experience_years,
            'is_freelance': user.is_freelance,
            'hourly_rate': user.hourly_rate,
            'availability': user.availability,
            'is_verified': user.is_verified,
            'is_active': user.is_active,
            'last_login': user.last_login,
            'institution_id': user.institution_id,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'roles': roles
        }
        
        return UserWithRoles(**user_dict)
