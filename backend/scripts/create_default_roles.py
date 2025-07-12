import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.role import Role
from app.core.database import Base
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ROLES = [
    {'name': 'caregiver', 'description': 'Cuidador profesional', 'is_system': False},
    {'name': 'family', 'description': 'Familiar o representante', 'is_system': False},
    {'name': 'institution', 'description': 'Institución', 'is_system': False},
    {'name': 'cared_person', 'description': 'Persona bajo cuidado', 'is_system': False},
]

def main():
    session = SessionLocal()
    try:
        for role_data in ROLES:
            existing = session.query(Role).filter(Role.name == role_data['name']).first()
            if not existing:
                role = Role(
                    name=role_data['name'],
                    description=role_data['description'],
                    permissions='{}',
                    is_system=role_data['is_system'],
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    is_active=True
                )
                session.add(role)
                print(f"Rol '{role_data['name']}' creado.")
            else:
                print(f"Rol '{role_data['name']}' ya existe.")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 