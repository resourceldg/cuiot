from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from sqlalchemy.orm import Session
from datetime import datetime

def fix_users_roles():
    db: Session = next(get_db())
    default_role = db.query(Role).filter_by(name='family_member').first()
    if not default_role:
        print("❌ No existe el rol 'family_member'. Aborta.")
        return
    users = db.query(User).all()
    fixed = 0
    for user in users:
        # Asignar género por defecto si falta
        if not user.gender:
            user.gender = 'Otro'
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

if __name__ == "__main__":
    fix_users_roles() 