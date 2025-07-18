from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserUpdate, UserWithRoles
from app.models.package import Package, UserPackage
from app.models.institution import Institution

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
            return None
        try:
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=422, detail=f"Error de validación: {str(e)}")
    
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
        """
        Assign a role to a user, trigger soft delete/validation/creation of essential records as needed.
        Ahora desactiva todos los roles previos antes de asignar el nuevo.

        ---
        POLÍTICA DE SOFT DELETE Y DATOS HISTÓRICOS:
        - Al cambiar de rol, todos los datos asociados a roles previos se marcan como soft delete (is_active = False).
        - Si el usuario vuelve a un rol anterior, NO se reactivan datos soft deleted automáticamente.
        - Cada ciclo de rol genera nuevos datos, manteniendo los anteriores como histórico para trazabilidad y auditoría.
        ---
        """
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

        # Desactivar todos los roles activos actuales del usuario (soft delete)
        user_roles = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.is_active == True).all()
        for ur in user_roles:
            ur.is_active = False
        db.commit()

        # 1. Soft delete (inactivar) registros de roles que ya no debe tener
        # 2. Validar y crear registros esenciales para el nuevo rol
        # 3. Lanzar excepción si faltan datos obligatorios
        missing_fields = []
        # --- ADMIN ---
        if role_name == "admin":
            for rel in [user.caregiver_assignments, user.caregiver_institutions, user.cared_persons]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
        elif role_name == "caregiver":
            for rel in [user.cared_persons]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
            if not user.professional_license:
                missing_fields.append("professional_license")
        elif role_name == "family":
            for rel in [user.caregiver_assignments, user.caregiver_institutions]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
            if not user.cared_persons or len(user.cared_persons) == 0:
                missing_fields.append("cared_person_link")
        elif role_name == "caredperson":
            for rel in [user.caregiver_assignments, user.caregiver_institutions]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
            if not user.cared_persons or len(user.cared_persons) == 0:
                from app.models.cared_person import CaredPerson
                cp = CaredPerson(user_id=user.id, first_name=user.first_name, last_name=user.last_name)
                db.add(cp)
        elif role_name == "institution_admin":
            for rel in [user.caregiver_assignments, user.caregiver_institutions, user.cared_persons]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
            if not user.institution_id:
                missing_fields.append("institution_id")
        elif role_name == "sin_rol":
            for rel in [user.caregiver_assignments, user.caregiver_institutions, user.cared_persons]:
                for obj in rel:
                    if hasattr(obj, 'is_active'):
                        obj.is_active = False
        else:
            pass

        if missing_fields:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": f"Faltan datos obligatorios para el rol '{role_name}'",
                    "missing_fields": missing_fields
                }
            )

        db.commit()

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
        # Get user first
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        # Get roles separately to avoid lazy loading issues
        user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
        role_ids = [ur.role_id for ur in user_roles]
        roles = []
        if role_ids:
            roles = [r.name for r in db.query(Role).filter(Role.id.in_(role_ids)).all()]
        
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

    @staticmethod
    def get_users_with_roles(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        institution_id: Optional[int] = None,
        is_freelance: Optional[bool] = None,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        package: Optional[str] = None,
        package_id: Optional[str] = None,
        institution_name: Optional[str] = None,
        no_institution: Optional[bool] = None
    ) -> List[UserWithRoles]:
        """Get list of users with their roles and advanced filters"""
        from sqlalchemy.orm import aliased
        # Start with base query
        query = db.query(User)

        # Join con UserRole y Role si se filtra por rol
        if role and role.strip():
            UserRoleAlias = aliased(UserRole)
            RoleAlias = aliased(Role)
            query = query.join(UserRoleAlias, User.id == UserRoleAlias.user_id)
            query = query.join(RoleAlias, UserRoleAlias.role_id == RoleAlias.id)
            query = query.filter(RoleAlias.name.ilike(role.strip()))
            query = query.filter(UserRoleAlias.is_active == True)

        # Apply basic filters first
        if no_institution:
            query = query.filter(User.institution_id.is_(None))
        elif institution_id is not None:
            query = query.filter(User.institution_id == institution_id)

        if is_freelance is not None:
            query = query.filter(User.is_freelance == is_freelance)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # Search filter (name, email, username)
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.username.ilike(search_term)
                )
            )

        # Institution name filter - join with institutions only if needed
        if institution_name and institution_name.strip():
            query = query.join(User.institution).filter(
                Institution.name.ilike(f"%{institution_name.strip()}%")
            )

        # Execute base query to get users
        users = query.offset(skip).limit(limit).all()

        # Package filter - only if packages exist
        if (package and package.strip()) or (package_id and package_id.strip()):
            package_count = db.query(Package).count()
            if package_count > 0:
                filtered_users = []
                for user in users:
                    # Solo considerar paquetes activos (status_type_id = 21 o NULL)
                    user_packages = db.query(UserPackage).filter(
                        UserPackage.user_id == user.id,
                        (UserPackage.status_type_id == 21) | (UserPackage.status_type_id.is_(None))
                    ).all()
                    has_matching_package = False
                    for user_package in user_packages:
                        package_obj = db.query(Package).filter(Package.id == user_package.package_id).first()
                        if package_obj:
                            if package_id and package_id.strip():
                                if str(package_obj.id) == package_id.strip():
                                    has_matching_package = True
                                    break
                            elif package and package.strip():
                                package_filter = package.strip().lower()
                                if (package_filter in package_obj.name.lower() or 
                                    (hasattr(package_obj, 'package_type') and 
                                     package_filter in package_obj.package_type.lower())):
                                    has_matching_package = True
                                    break
                    if has_matching_package:
                        filtered_users.append(user)
                users = filtered_users

        # Definir roles permitidos para paquetes personales e institucionales
        ROLES_WITH_PACKAGE = {"cared_person_self", "family_member", "family", "institution_admin"}

        # Transform to UserWithRoles format
        result = []
        for user in users:
            user_roles = db.query(UserRole).filter(
                UserRole.user_id == user.id,
                UserRole.is_active == True
            ).all()
            role_names = []
            for user_role in user_roles:
                role_obj = db.query(Role).filter(Role.id == user_role.role_id).first()
                if role_obj:
                    role_names.append(role_obj.name)
            # Solo permitir paquetes si el usuario tiene al menos un rol permitido
            allow_packages = any(r in ROLES_WITH_PACKAGE for r in role_names)
            user_packages = []
            if allow_packages:
                user_packages = db.query(UserPackage).filter(
                    UserPackage.user_id == user.id,
                    (UserPackage.status_type_id == 21) | (UserPackage.status_type_id.is_(None))
                ).all()
            package_subscriptions = []
            for user_package in user_packages:
                package_obj = db.query(Package).filter(Package.id == user_package.package_id).first()
                if package_obj:
                    package_subscriptions.append({
                        'id': str(user_package.id),
                        'package_id': str(user_package.package_id),
                        'package_name': package_obj.name,
                        'status_type_id': user_package.status_type_id,
                        'is_active': True
                    })
            user_with_roles = UserWithRoles(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                is_active=user.is_active,
                is_verified=user.is_verified,
                is_freelance=user.is_freelance,
                institution_id=user.institution_id,
                date_of_birth=user.date_of_birth,
                gender=user.gender,
                professional_license=user.professional_license,
                specialization=user.specialization,
                experience_years=user.experience_years,
                hourly_rate=user.hourly_rate,
                availability=user.availability,
                last_login=user.last_login,
                created_at=user.created_at,
                updated_at=user.updated_at,
                roles=role_names,
                package_subscriptions=package_subscriptions
            )
            result.append(user_with_roles)
        return result
