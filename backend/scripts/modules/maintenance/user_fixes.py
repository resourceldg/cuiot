"""
Funciones de mantenimiento para usuarios y roles
"""
from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from datetime import datetime

def fix_users_roles(db=None):
    """
    Asigna género por defecto ('other') y rol 'family_member' a usuarios que no lo tengan.
    Si no se pasa una sesión, la gestiona internamente.
    """
    close_db = False
    if db is None:
        db = next(get_db())
        close_db = True
    default_role = db.query(Role).filter_by(name='family_member').first()
    if not default_role:
        print("❌ No existe el rol 'family_member'. Aborta.")
        if close_db:
            db.close()
        return 0
    users = db.query(User).all()
    fixed = 0
    for user in users:
        # Asignar género por defecto si falta
        if not user.gender:
            user.gender = 'other'
            fixed += 1
        roles_count = db.query(UserRole).filter_by(user_id=user.id).count()
        if roles_count == 0:
            user_role = UserRole(
                user_id=user.id,
                role_id=default_role.id,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(user_role)
            fixed += 1
            print(f"🛠️  Asignado rol 'family_member' a usuario {user.email}")
    db.commit()
    print(f"✅ Usuarios corregidos: {fixed}")
    if close_db:
        db.close()
    return fixed 


def fix_normalize_gender_values(db=None):
    """
    Normaliza todos los valores de género en la base de datos a los valores estándar:
    - 'Masculino', 'masculino' -> 'male'
    - 'Femenino', 'femenino' -> 'female'
    - 'Otro', 'otro', '', NULL -> 'other'
    """
    close_db = False
    if db is None:
        db = next(get_db())
        close_db = True
    mapping = {
        'Masculino': 'male',
        'masculino': 'male',
        'Femenino': 'female',
        'femenino': 'female',
        'Otro': 'other',
        'otro': 'other',
        '': 'other',
        None: 'other',
    }
    users = db.query(User).all()
    fixed = 0
    for user in users:
        new_gender = mapping.get(user.gender, user.gender)
        if user.gender != new_gender:
            user.gender = new_gender
            fixed += 1
    db.commit()
    print(f"✅ Géneros normalizados: {fixed}")
    if close_db:
        db.close()
    return fixed 