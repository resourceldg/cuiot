"""
Caregivers Submodule - Populates caregiver data
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.caregiver_institution import CaregiverInstitution
from app.models.caregiver_assignment_type import CaregiverAssignmentType
from app.models.user import User
from app.models.institution import Institution
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.status_type import StatusType
from app.models.relationship_type import RelationshipType
from app.core.database import get_db


def populate_caregivers(db: Session, num_caregivers: int = 15):
    """
    Populate caregivers with realistic data
    """
    print(f"🌱 Populating {num_caregivers} caregivers...")
    
    # Get existing data
    assignment_types = db.query(CaregiverAssignmentType).all()
    institutions = db.query(Institution).all()
    caregiver_role = db.query(Role).filter(Role.name == "caregiver").first()
    
    if not assignment_types or not institutions or not caregiver_role:
        print("❌ Missing required data: assignment_types, institutions, or caregiver role")
        return
    
    # Sample caregiver data
    caregiver_data = [
        {
            "first_name": "Elena",
            "last_name": "Vargas",
            "phone": "+34 600 111 222",
            "email": "elena.vargas@cuiot.com",
            "specialization": "Cuidado de personas con demencia",
            "experience_years": 8,
            "is_available": True
        },
        {
            "first_name": "Roberto",
            "last_name": "Silva",
            "phone": "+34 600 222 333",
            "email": "roberto.silva@cuiot.com",
            "specialization": "Cuidado post-operatorio",
            "experience_years": 5,
            "is_available": True
        },
        {
            "first_name": "Patricia",
            "last_name": "Mendoza",
            "phone": "+34 600 333 444",
            "email": "patricia.mendoza@cuiot.com",
            "specialization": "Cuidado de personas con movilidad reducida",
            "experience_years": 12,
            "is_available": True
        },
        {
            "first_name": "Carlos",
            "last_name": "Herrera",
            "phone": "+34 600 444 555",
            "email": "carlos.herrera@cuiot.com",
            "specialization": "Cuidado de personas con diabetes",
            "experience_years": 6,
            "is_available": True
        },
        {
            "first_name": "Ana",
            "last_name": "Rojas",
            "phone": "+34 600 555 666",
            "email": "ana.rojas@cuiot.com",
            "specialization": "Cuidado de personas mayores general",
            "experience_years": 10,
            "is_available": True
        }
    ]
    
    # Generate additional random caregivers
    first_names = ["Laura", "Miguel", "Sofia", "Javier", "Carmen", "Diego", "Isabella", "Andrés", "Valentina", "Ricardo"]
    last_names = ["Castillo", "Reyes", "Jiménez", "Moreno", "Herrera", "Castro", "Romero", "Alvarez", "Torres", "Gutierrez"]
    specializations = [
        "Cuidado de personas con demencia",
        "Cuidado post-operatorio", 
        "Cuidado de personas con movilidad reducida",
        "Cuidado de personas con diabetes",
        "Cuidado de personas mayores general",
        "Cuidado de personas con Parkinson",
        "Cuidado de personas con EPOC",
        "Cuidado de personas con cardiopatías",
        "Cuidado de personas con artritis",
        "Cuidado de personas con osteoporosis"
    ]
    
    for i in range(num_caregivers):
        if i < len(caregiver_data):
            data = caregiver_data[i].copy()
            # Añadir sufijo único al email fijo
            if data["email"]:
                local, domain = data["email"].split("@")
                data["email"] = f"{local}.{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}@{domain}"
        else:
            # Generate random data
            data = {
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "phone": f"+34 600 {random.randint(100000, 999999)}",
                "email": f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}.{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}@cuiot.com",
                "specialization": random.choice(specializations),
                "experience_years": random.randint(1, 15),
                "is_available": random.choice([True, True, True, False])  # 75% available
            }
        
        # Create caregiver user first
        caregiver_user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            password_hash="pbkdf2:sha256:dummyhash",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(caregiver_user)
        db.flush()  # Get the ID
        
        # Assign caregiver role via UserRole
        caregiver_user_role = UserRole(
            user_id=caregiver_user.id,
            role_id=caregiver_role.id,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(caregiver_user_role)
        db.flush()
        
        # Buscar status_type y relationship_type por nombre
        status_type = db.query(StatusType).filter_by(name="active").first()
        relationship_type = db.query(RelationshipType).filter_by(name="employee").first()
        
        # Create caregiver institution relationship
        caregiver_institution = CaregiverInstitution(
            caregiver_id=caregiver_user.id,
            institution_id=random.choice(institutions).id,
            contract_type=random.choice(["employee", "contractor", "volunteer"]),
            start_date=datetime.utcnow().date() - timedelta(days=random.randint(1, 365)),
            end_date=None,  # Ongoing contract
            position=data["specialization"],
            department="Cuidado",
            work_schedule='{"monday": "8:00-16:00", "tuesday": "8:00-16:00", "wednesday": "8:00-16:00", "thursday": "8:00-16:00", "friday": "8:00-16:00"}',
            hourly_rate=random.randint(800, 1500),  # 8-15 euros per hour
            salary=None,
            benefits='{"health_insurance": true, "vacation_days": 25}',
            status_type_id=status_type.id if status_type else None,
            relationship_type_id=relationship_type.id if relationship_type else None,
            is_primary=True,
            hired_by=None,
            hired_at=datetime.utcnow(),
            notes=f"Experiencia: {data['experience_years']} años. Disponible: {'Sí' if data['is_available'] else 'No'}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(caregiver_institution)
    
    try:
        db.commit()
        print(f"✅ Successfully created {num_caregivers} caregivers")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating caregivers: {e}")
        raise


if __name__ == "__main__":
    db = next(get_db())
    populate_caregivers(db) 