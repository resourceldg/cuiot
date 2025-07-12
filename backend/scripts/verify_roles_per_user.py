import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.database import Base

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        print(f"{'ID':<36} {'Email':<30} {'Nombre':<20} {'Roles'}")
        print('-'*100)
        for user in users:
            user_roles = session.query(UserRole).filter(UserRole.user_id == user.id).all()
            role_names = []
            for ur in user_roles:
                role = session.query(Role).filter(Role.id == ur.role_id).first()
                if role:
                    role_names.append(role.name)
            print(f"{str(user.id):<36} {user.email:<30} {user.first_name+' '+(user.last_name or ''):<20} {', '.join(role_names) if role_names else 'Sin rol'}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 