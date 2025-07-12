import os
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.database import Base

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Lista de roles posibles para asignar aleatoriamente
ROLES = ['caregiver', 'family', 'institution', 'cared_person']

def main():
    session = SessionLocal()
    try:
        # Verifica que existan los roles en la base
        available_roles = {r.name: r for r in session.query(Role).filter(Role.name.in_(ROLES)).all()}
        if len(available_roles) < len(ROLES):
            print("Faltan roles en la base de datos. Crea todos los roles primero.")
            return
        users = session.query(User).all()
        count = 0
        for user in users:
            user_roles = session.query(UserRole).filter(UserRole.user_id == user.id).all()
            if not user_roles:
                random_role = random.choice(ROLES)
                UserRole.assign_role_to_user(session, user.id, random_role)
                print(f"Asignado rol '{random_role}' a usuario {user.email}")
                count += 1
        session.commit()
        print(f"Roles aleatorios asignados a {count} usuarios sin rol.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 