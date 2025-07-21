"""
Cared Persons Submodule - Populates cared person data
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.cared_person import CaredPerson
from app.models.relationship_type import RelationshipType
from app.models.user import User
from app.models.package import Package
from app.models.institution import Institution
from app.core.database import get_db


def populate_cared_persons(db: Session, num_cared_persons: int = 20):
    """
    Populate cared persons with realistic data
    """
    print(f"🌱 Populating {num_cared_persons} cared persons...")
    
    # Get existing data
    relationship_types = db.query(RelationshipType).all()
    packages = db.query(Package).all()
    institutions = db.query(Institution).all()
    
    if not relationship_types or not packages:
        print("❌ Missing required data: relationship_types or packages")
        return
    
    # Sample cared person data
    cared_person_data = [
        {
            "first_name": "María",
            "last_name": "González",
            "age": 78,
            "gender": "F",
            "emergency_contact": "+34 600 123 456",
            "medical_conditions": "Diabetes, hipertensión",
            "allergies": "Penicilina",
            "medications": "Metformina, Enalapril"
        },
        {
            "first_name": "José",
            "last_name": "Martínez",
            "age": 82,
            "gender": "M", 
            "emergency_contact": "+34 600 234 567",
            "medical_conditions": "Artritis, osteoporosis",
            "allergies": "Ninguna",
            "medications": "Calcio, vitamina D"
        },
        {
            "first_name": "Carmen",
            "last_name": "López",
            "age": 75,
            "gender": "F",
            "emergency_contact": "+34 600 345 678",
            "medical_conditions": "Demencia leve",
            "allergies": "Lactosa",
            "medications": "Donepezilo"
        },
        {
            "first_name": "Antonio",
            "last_name": "Rodríguez",
            "age": 79,
            "gender": "M",
            "emergency_contact": "+34 600 456 789",
            "medical_conditions": "EPOC, cardiopatía",
            "allergies": "Polvo",
            "medications": "Salbutamol, Furosemida"
        },
        {
            "first_name": "Isabel",
            "last_name": "Fernández",
            "age": 81,
            "gender": "F",
            "emergency_contact": "+34 600 567 890",
            "medical_conditions": "Parkinson",
            "allergies": "Ninguna",
            "medications": "Levodopa"
        }
    ]
    
    # Generate additional random cared persons
    first_names = ["Ana", "Luis", "Rosa", "Manuel", "Teresa", "Francisco", "Pilar", "Miguel", "Concepción", "Carlos"]
    last_names = ["García", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Morales", "Cruz", "Ortiz"]
    
    for i in range(num_cared_persons):
        if i < len(cared_person_data):
            data = cared_person_data[i]
        else:
            # Generate random data
            data = {
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "age": random.randint(70, 95),
                "gender": random.choice(["M", "F"]),
                "emergency_contact": f"+34 600 {random.randint(100000, 999999)}",
                "medical_conditions": random.choice([
                    "Hipertensión", "Diabetes", "Artritis", "Osteoporosis", 
                    "Demencia leve", "EPOC", "Cardiopatía", "Parkinson",
                    "Ninguna", "Múltiples condiciones"
                ]),
                "allergies": random.choice([
                    "Ninguna", "Penicilina", "Lactosa", "Polvo", "Polen", "Mariscos"
                ]),
                "medications": random.choice([
                    "Metformina", "Enalapril", "Calcio", "Donepezilo", 
                    "Salbutamol", "Levodopa", "Ninguna", "Múltiples medicamentos"
                ])
            }
        
        # Calculate date of birth from age
        from datetime import date
        current_year = date.today().year
        birth_year = current_year - data["age"]
        date_of_birth = date(birth_year, random.randint(1, 12), random.randint(1, 28))
        
        # Create cared person
        cared_person = CaredPerson(
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=date_of_birth,
            gender=data["gender"],
            emergency_contact=data["emergency_contact"],
            medical_notes=data["medical_conditions"] + "\nAlergias: " + data["allergies"] + "\nMedicamentos: " + data["medications"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(cared_person)
    
    try:
        db.commit()
        print(f"✅ Successfully created {num_cared_persons} cared persons")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating cared persons: {e}")
        raise


if __name__ == "__main__":
    db = next(get_db())
    populate_cared_persons(db) 