from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

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
        query = db.query(User)
        
        if institution_id is not None:
            query = query.filter(User.institution_id == institution_id)
        
        if is_freelance is not None:
            query = query.filter(User.is_freelance == is_freelance)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
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
            hashed_password=hashed_password,
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
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
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
    def delete_user(db: Session, user_id: int) -> bool:
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
    def assign_role(db: Session, user_id: int, role_name: str) -> bool:
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
    def remove_role(db: Session, user_id: int, role_name: str) -> bool:
        """Remove a role from a user"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserRole.remove_role_from_user(db, user_id, role_name)
    
    @staticmethod
    def get_user_with_roles(db: Session, user_id: int) -> Optional[UserWithRoles]:
        """Get user with role information"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Get role names
        roles = [role.name for role in user.roles]
        
        return UserWithRoles(
            **user.__dict__,
            roles=roles
        )
