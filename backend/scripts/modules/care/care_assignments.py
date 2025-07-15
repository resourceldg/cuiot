"""
Care Assignments Submodule - Populates caregiver assignments to cared persons
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.caregiver_assignment import CaregiverAssignment
from app.models.caregiver_institution import CaregiverInstitution
from app.models.cared_person import CaredPerson
from app.models.shift_observation import ShiftObservation
from app.models.shift_observation_type import ShiftObservationType
from app.core.database import get_db


def populate_care_assignments(db: Session, num_assignments: int = 30):
    """
    Populate caregiver assignments and shift observations
    """
    print(f"🌱 Populating {num_assignments} care assignments...")
    
    # Get existing data
    caregiver_institutions = db.query(CaregiverInstitution).filter(CaregiverInstitution.status_type_id == 1).all()  # active caregivers
    cared_persons = db.query(CaredPerson).all()
    observation_types = db.query(ShiftObservationType).all()
    
    if not caregiver_institutions or not cared_persons:
        print(f"⚠️  Advertencia: No se pueden crear asignaciones de cuidado.")
        print(f"   - caregiver_institutions encontrados: {len(caregiver_institutions)}")
        print(f"   - cared_persons encontrados: {len(cared_persons)}")
        print("   Sugerencia: Ejecuta primero los submódulos de instituciones, cuidadores y personas cuidadas antes de poblar asignaciones.")
        return
    
    # Sample assignment data
    assignment_data = [
        {
            "start_date": datetime.utcnow() - timedelta(days=30),
            "end_date": datetime.utcnow() + timedelta(days=60),
            "notes": "Asignación regular de cuidado"
        },
        {
            "start_date": datetime.utcnow() - timedelta(days=15),
            "end_date": datetime.utcnow() + timedelta(days=45),
            "notes": "Cuidado especializado requerido"
        },
        {
            "start_date": datetime.utcnow() - timedelta(days=7),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "notes": "Asignación temporal por enfermedad del cuidador principal"
        }
    ]
    
    # Obtener los tipos de asignación disponibles
    assignment_type_ids = [1, 2, 3, 4, 5]  # IDs existentes en la base

    # Create assignments
    for i in range(num_assignments):
        if i < len(assignment_data):
            data = assignment_data[i]
        else:
            # Generate random assignment data
            start_days_ago = random.randint(1, 60)
            duration_days = random.randint(30, 180)
            
            data = {
                "start_date": datetime.utcnow() - timedelta(days=start_days_ago),
                "end_date": datetime.utcnow() + timedelta(days=duration_days),
                "notes": random.choice([
                    "Asignación regular de cuidado",
                    "Cuidado especializado requerido",
                    "Asignación temporal",
                    "Cuidado de emergencia",
                    "Cuidado post-operatorio",
                    "Cuidado de fin de semana"
                ])
            }
        
        # Create assignment
        caregiver_institution = random.choice(caregiver_institutions)
        assignment = CaregiverAssignment(
            caregiver_id=caregiver_institution.caregiver_id,
            cared_person_id=random.choice(cared_persons).id,
            start_date=data["start_date"],
            end_date=data["end_date"],
            notes=data["notes"],
            caregiver_assignment_type_id=random.choice(assignment_type_ids),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(assignment)
    
    # Create shift observations for active assignments
    active_assignments = db.query(CaregiverAssignment).filter(CaregiverAssignment.is_active == True).all()
    
    for assignment in random.sample(active_assignments, min(len(active_assignments), num_assignments // 2)):
        # Create 1-3 observations per assignment
        for _ in range(random.randint(1, 3)):
            observation = ShiftObservation(
                caregiver_id=assignment.caregiver_id,
                cared_person_id=assignment.cared_person_id,
                observation_type_id=random.choice(observation_types).id if observation_types else None,
                observation_text=random.choice([
                    "Paciente en buen estado general",
                    "Medicación administrada correctamente",
                    "Paciente cooperativo durante el cuidado",
                    "Se observa mejoría en la movilidad",
                    "Paciente descansando adecuadamente",
                    "Sin incidentes durante el turno",
                    "Paciente con buen apetito",
                    "Signos vitales estables"
                ]),
                observation_date=datetime.utcnow() - timedelta(days=random.randint(0, 7)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(observation)
    
    try:
        db.commit()
        print(f"✅ Successfully created care assignments and observations")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating care assignments: {e}")
        raise


if __name__ == "__main__":
    db = next(get_db())
    populate_care_assignments(db) 