import sys
import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.package import UserPackage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fix_users_roles")

def fix_user_roles_and_packages(db: Session):
    users = db.query(User).all()
    total_fixed_roles = 0
    total_fixed_packages = 0
    for user in users:
        # --- Fix roles ---
        active_roles = [ur for ur in user.user_roles if ur.is_active]
        if len(active_roles) > 1:
            # Dejar solo el más reciente activo
            active_roles.sort(key=lambda ur: ur.created_at or datetime.min, reverse=True)
            for ur in active_roles[1:]:
                ur.is_active = False
                logger.info(f"Desactivado rol duplicado para usuario {user.email}: {ur.role_id}")
            total_fixed_roles += 1
        # --- Fix packages ---
        active_packages = [up for up in getattr(user, 'user_packages', []) if up.is_active]
        if len(active_packages) > 1:
            active_packages.sort(key=lambda up: up.created_at or datetime.min, reverse=True)
            for up in active_packages[1:]:
                up.is_active = False
                logger.info(f"Desactivado paquete duplicado para usuario {user.email}: {up.package_id}")
            total_fixed_packages += 1
    db.commit()
    logger.info(f"Usuarios con roles corregidos: {total_fixed_roles}")
    logger.info(f"Usuarios con paquetes corregidos: {total_fixed_packages}")

def main():
    db = next(get_db())
    fix_user_roles_and_packages(db)

if __name__ == "__main__":
    main() 