import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.database import Base
from app.services.user import UserService

# Configuración de la base de datos (ajusta según tu entorno)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    session = SessionLocal()
    try:
        # Elige el rol a asignar (puedes cambiarlo por 'admin', 'family', etc.)
        role_name = sys.argv[1] if len(sys.argv) > 1 else 'caregiver'
        role = session.query(Role).filter(Role.name == role_name).first()
        if not role:
            print(f"El rol '{role_name}' no existe. Crea el rol primero.")
            return
        users = session.query(User).all()
        count = 0
        for user in users:
            user_roles = session.query(UserRole).filter(UserRole.user_id == user.id).all()
            if not user_roles:
                UserRole.assign_role_to_user(session, user.id, role_name)
                count += 1
        session.commit()
        print(f"Roles asignados a {count} usuarios.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 