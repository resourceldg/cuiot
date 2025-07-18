import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.package import UserPackage, Package

# Roles permitidos para cada tipo de paquete
ALLOWED_ROLES = set([
    "cared_person_self", "family", "family_member",
    "institution_admin", "institutional_user", "doctor", "staff"
])

def verify_user_subscriptions():
    db = next(get_db())
    users = db.query(User).filter(User.is_active == True).all()
    roles_dict = {r.id: r.name for r in db.query(Role).all()}
    users_without_subs = []
    users_with_subs = []
    for user in users:
        # Obtener roles activos del usuario
        user_roles = set()
        for ur in db.query(UserRole).filter_by(user_id=user.id, is_active=True):
            role_name = roles_dict.get(ur.role_id)
            if role_name:
                user_roles.add(role_name)
        if not user_roles & ALLOWED_ROLES:
            continue  # No es usuario con permiso de paquete
        # Buscar suscripciones activas
        user_packages = db.query(UserPackage).filter_by(user_id=user.id).all()
        if user_packages:
            users_with_subs.append((user, user_roles, user_packages))
        else:
            users_without_subs.append((user, user_roles))
    print("\n==== VERIFICACIÓN DE SUSCRIPCIONES DE USUARIOS ====")
    print(f"Usuarios con roles permitidos y suscripción: {len(users_with_subs)}")
    for user, roles, packages in users_with_subs:
        print(f"  - {user.email} | Roles: {', '.join(roles)} | Suscripciones: {len(packages)}")
    print(f"\nUsuarios con roles permitidos SIN suscripción: {len(users_without_subs)}")
    for user, roles in users_without_subs:
        print(f"  - {user.email} | Roles: {', '.join(roles)}")
    print("\nResumen: {} usuarios con suscripción, {} sin suscripción".format(len(users_with_subs), len(users_without_subs)))

if __name__ == "__main__":
    verify_user_subscriptions() 