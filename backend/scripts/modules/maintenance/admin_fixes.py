"""
Funciones de mantenimiento para roles y usuario admin
"""
import json
from datetime import datetime
from app.core.database import get_db
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole

ADMIN_PERMISSIONS = {
    "users": {"read": True, "write": True, "delete": True},
    "cared_persons": {"read": True, "write": True, "delete": True},
    "institutions": {"read": True, "write": True, "delete": True},
    "devices": {"read": True, "write": True, "delete": True},
    "protocols": {"read": True, "write": True, "delete": True},
    "reports": {"read": True, "write": True},
    "system": {"read": True, "write": True, "delete": True}
}

ADMIN_EMAIL = "admin@cuiot.com"

def fix_admin_role_and_user(db=None):
    """
    Asegura que el rol admin tenga permisos completos y el usuario admin tenga el rol activo y sin expiración.
    Si no se pasa una sesión, la gestiona internamente.
    """
    close_db = False
    if db is None:
        db = next(get_db())
        close_db = True
    try:
        # 1. Asegurar que el rol admin existe y tiene permisos completos
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("❌ No existe el rol 'admin'")
            return False
        admin_role.permissions = json.dumps(ADMIN_PERMISSIONS)
        admin_role.is_active = True
        admin_role.is_system = True  # Marcar admin como sistema
        admin_role.updated_at = datetime.now()
        db.commit()
        print("✅ Permisos del rol admin corregidos y marcado como sistema")

        # 2. Asegurar que el usuario admin tiene el rol admin activo y sin expiración
        admin_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin_user:
            print(f"❌ No existe el usuario admin con email {ADMIN_EMAIL}")
            return False
        user_role = db.query(UserRole).filter(
            UserRole.user_id == admin_user.id,
            UserRole.role_id == admin_role.id
        ).first()
        if not user_role:
            # Asignar el rol admin si no lo tiene
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id, is_active=True, expires_at=None)
            db.add(user_role)
            print("✅ Rol admin asignado al usuario admin")
        else:
            user_role.is_active = True
            user_role.expires_at = None
            print("✅ Rol admin del usuario admin activado y sin expiración")
        db.commit()
        print("✅ Usuario admin verificado con rol admin activo")

        # Crear el rol especial 'sin_rol' si no existe
        sin_rol = db.query(Role).filter_by(name='sin_rol').first()
        if not sin_rol:
            sin_rol = Role(
                name='sin_rol',
                description='Rol placeholder para usuarios sin rol asignado',
                permissions=json.dumps({}),
                is_system=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True
            )
            db.add(sin_rol)
            db.commit()
            print("✅ Rol especial 'sin_rol' creado y marcado como sistema.")
        else:
            sin_rol.is_system = True
            db.commit()
            print("ℹ️  El rol especial 'sin_rol' ya existe y fue marcado como sistema.")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        if close_db:
            db.close() 