#!/usr/bin/env python3
"""
Script para resetear la contraseña del usuario admin@cuiot.com a 'Admin123!'
"""

import sys
from pathlib import Path

# Asegurar que el path incluye la raíz del backend
current_path = Path(__file__).parent.parent
if str(current_path) not in sys.path:
    sys.path.insert(0, str(current_path))

from app.core.database import get_db
from app.models.user import User
from app.services.auth import AuthService

def reset_admin_password():
    email = "admin@cuiot.com"
    new_password = "Admin123!"
    db = next(get_db())
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ No existe un usuario con email: {email}")
            return False
        user.password_hash = AuthService.get_password_hash(new_password)
        db.commit()
        print(f"✅ Contraseña reseteada para {email}")
        print(f"Nueva contraseña: {new_password}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password() 