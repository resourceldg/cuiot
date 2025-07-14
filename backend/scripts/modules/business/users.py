import random
from datetime import datetime, date
from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
import hashlib
import os

def generate_password_hash(password):
    """Simple password hash function"""
    salt = os.urandom(32).hex()
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"sha256${salt}${hash_obj.hexdigest()}"

SAMPLE_USERS = [
    # Administradores
    {
        "email": "admin@cuiot.com",
        "username": "admin",
        "password_hash": generate_password_hash("admin123"),
        "first_name": "Administrador",
        "last_name": "Sistema",
        "phone": "+54 11 5555-0001",
        "date_of_birth": date(1985, 5, 15),
        "gender": "Masculino",
        "professional_license": None,
        "specialization": None,
        "experience_years": None,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": None,
        "roles": ["admin"]
    },
    {
        "email": "maria.garcia@cuiot.com",
        "username": "mgarcia",
        "password_hash": generate_password_hash("password123"),
        "first_name": "María",
        "last_name": "García",
        "phone": "+54 11 5555-0002",
        "date_of_birth": date(1990, 8, 22),
        "gender": "Femenino",
        "professional_license": None,
        "specialization": None,
        "experience_years": None,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": None,
        "roles": ["admin"]
    },
    # Usuarios familiares
    {
        "email": "juan.perez@email.com",
        "username": "jperez",
        "password_hash": generate_password_hash("password123"),
        "first_name": "Juan",
        "last_name": "Pérez",
        "phone": "+54 11 5555-0003",
        "date_of_birth": date(1975, 3, 10),
        "gender": "Masculino",
        "professional_license": None,
        "specialization": None,
        "experience_years": None,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": None,
        "roles": ["family_member"]
    },
    {
        "email": "ana.rodriguez@email.com",
        "username": "arodriguez",
        "password_hash": generate_password_hash("password123"),
        "first_name": "Ana",
        "last_name": "Rodríguez",
        "phone": "+54 11 5555-0004",
        "date_of_birth": date(1980, 12, 5),
        "gender": "Femenino",
        "professional_license": None,
        "specialization": None,
        "experience_years": None,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": None,
        "roles": ["family_member"]
    },
    # Usuarios institucionales
    {
        "email": "dr.lopez@san-jose.com",
        "username": "dlopez",
        "password_hash": generate_password_hash("password123"),
        "first_name": "Dr. Carlos",
        "last_name": "López",
        "phone": "+54 11 5555-0005",
        "date_of_birth": date(1970, 6, 18),
        "gender": "Masculino",
        "professional_license": "MED-12345",
        "specialization": "Geriatría",
        "experience_years": 15,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": 1,  # Residencia San José
        "roles": ["institutional_user"]
    },
    {
        "email": "lic.martinez@losrobles.com",
        "username": "lmartinez",
        "password_hash": generate_password_hash("password123"),
        "first_name": "Lic. Laura",
        "last_name": "Martínez",
        "phone": "+54 11 5555-0006",
        "date_of_birth": date(1985, 9, 30),
        "gender": "Femenino",
        "professional_license": "PSI-67890",
        "specialization": "Psicología Geriátrica",
        "experience_years": 8,
        "is_freelance": False,
        "hourly_rate": None,
        "availability": None,
        "is_verified": True,
        "is_active": True,
        "institution_id": 2,  # Clínica Los Robles
        "roles": ["institutional_user"]
    }
]

def populate_users():
    db = next(get_db())
    created = 0
    
    # Obtener roles disponibles
    roles_dict = {}
    for role in db.query(Role).all():
        roles_dict[role.name] = role.id
    
    for data in SAMPLE_USERS:
        # Extraer roles del diccionario
        user_roles = data.pop("roles", [])
        
        # Verificar si el usuario ya existe
        user = db.query(User).filter_by(email=data["email"]).first()
        if not user:
            user = User(**data)
            db.add(user)
            db.flush()  # Para obtener el ID del usuario
            
            # Asignar roles
            for role_name in user_roles:
                if role_name in roles_dict:
                    user_role = UserRole(
                        user_id=user.id,
                        role_id=roles_dict[role_name],
                        is_active=True
                    )
                    db.add(user_role)
            
            created += 1
    
    db.commit()
    print(f"✅ Usuarios creados: {created} (idempotente)")
    db.close()

if __name__ == "__main__":
    populate_users() 