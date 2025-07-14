"""
Medical Data Submodule - Populates medical records, diagnoses, and vital signs
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.diagnosis import Diagnosis
from app.models.vital_sign import VitalSign
from app.models.medication_schedule import MedicationSchedule
from app.models.medication_log import MedicationLog
from app.models.cared_person import CaredPerson
from app.models.user import User
from app.core.database import get_db


def populate_medical_data(db: Session, num_records: int = 50):
    """
    Populate medical data including diagnoses, vital signs, and medication records
    """
    print(f"🌱 Populating {num_records} medical records...")
    
    # Get existing data
    cared_persons = db.query(CaredPerson).all()
    users = db.query(User).all()
    
    if not cared_persons:
        print("❌ Missing required data: cared_persons")
        return
    
    # Sample diagnosis data
    diagnosis_data = [
        {
            "diagnosis_name": "Diabetes mellitus tipo 2",
            "description": "Trastorno metabólico caracterizado por niveles elevados de glucosa en sangre",
            "severity_level": "Moderada",
            "medical_notes": "Control dietético, ejercicio físico y medicación oral"
        },
        {
            "diagnosis_name": "Hipertensión arterial",
            "description": "Presión arterial elevada de forma persistente",
            "severity_level": "Leve",
            "medical_notes": "Modificación del estilo de vida y medicación antihipertensiva"
        },
        {
            "diagnosis_name": "Artritis reumatoide",
            "description": "Enfermedad inflamatoria crónica que afecta las articulaciones",
            "severity_level": "Moderada",
            "medical_notes": "Medicación antiinflamatoria y fisioterapia"
        },
        {
            "diagnosis_name": "Demencia tipo Alzheimer",
            "description": "Enfermedad neurodegenerativa que afecta la memoria y cognición",
            "severity_level": "Leve",
            "medical_notes": "Medicación para ralentizar el progreso y terapia cognitiva"
        },
        {
            "diagnosis_name": "EPOC",
            "description": "Enfermedad pulmonar obstructiva crónica",
            "severity_level": "Moderada",
            "medical_notes": "Broncodilatadores y rehabilitación pulmonar"
        }
    ]
    
    # Sample vital signs ranges
    vital_signs_ranges = {
        "blood_pressure_systolic": (110, 180),
        "blood_pressure_diastolic": (60, 100),
        "heart_rate": (60, 100),
        "temperature": (36.0, 37.5),
        "oxygen_saturation": (95, 100),
        "respiratory_rate": (12, 20)
    }
    
    # Sample medications
    medications = [
        {"name": "Metformina", "dosage": "500mg", "frequency": "2 veces al día"},
        {"name": "Enalapril", "dosage": "10mg", "frequency": "1 vez al día"},
        {"name": "Ibuprofeno", "dosage": "400mg", "frequency": "3 veces al día"},
        {"name": "Donepezilo", "dosage": "5mg", "frequency": "1 vez al día"},
        {"name": "Salbutamol", "dosage": "100mcg", "frequency": "Según necesidad"},
        {"name": "Calcio", "dosage": "500mg", "frequency": "1 vez al día"},
        {"name": "Vitamina D", "dosage": "1000UI", "frequency": "1 vez al día"},
        {"name": "Levodopa", "dosage": "100mg", "frequency": "3 veces al día"}
    ]
    
    # Create diagnoses
    for i, cared_person in enumerate(random.sample(cared_persons, min(len(cared_persons), num_records // 2))):
        if i < len(diagnosis_data):
            data = diagnosis_data[i]
        else:
            data = {
                "diagnosis_name": random.choice([
                    "Osteoporosis", "Parkinson", "Insuficiencia cardíaca", 
                    "Glaucoma", "Cataratas", "Depresión", "Ansiedad"
                ]),
                "description": "Descripción médica del diagnóstico",
                "severity_level": random.choice(["Leve", "Moderada", "Severa"]),
                "medical_notes": "Plan de tratamiento personalizado"
            }
        
        # Get a user for created_by_id
        user = db.query(User).first()
        
        diagnosis = Diagnosis(
            cared_person_id=cared_person.id,
            diagnosis_name=data["diagnosis_name"],
            description=data["description"],
            severity_level=data["severity_level"],
            diagnosis_date=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            doctor_name=f"Dr. {random.choice(['García', 'López', 'Martínez', 'Rodríguez', 'Fernández'])}",
            medical_notes=data["medical_notes"],
            cie10_code=f"E{random.randint(10, 99)}.{random.randint(0, 9)}",
            is_active=True,
            created_by_id=user.id if user else None,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            updated_at=datetime.utcnow()
        )
        db.add(diagnosis)
    
    # Create vital signs records (through shift observations)
    for cared_person in random.sample(cared_persons, min(len(cared_persons), num_records // 3)):
        for _ in range(random.randint(1, 3)):  # 1-3 records per person
            # First create a shift observation
            from app.models.shift_observation import ShiftObservation
            from app.models.shift_observation_type import ShiftObservationType
            
            observation_type = db.query(ShiftObservationType).first()
            # Create a proper shift observation with required fields
            shift_start = datetime.utcnow() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 8))
            shift_end = shift_start + timedelta(hours=8)
            
            shift_observation = ShiftObservation(
                shift_observation_type_id=observation_type.id if observation_type else 1,
                shift_type=random.choice(["morning", "afternoon", "night"]),
                shift_start=shift_start,
                shift_end=shift_end,
                observation_date=shift_start,
                cared_person_id=cared_person.id,
                caregiver_id=random.choice(users).id if users else None,
                physical_condition=random.choice(["excellent", "good", "fair", "poor"]),
                mobility_level=random.choice(["independent", "assisted", "wheelchair"]),
                mental_state=random.choice(["alert", "calm", "confused"]),
                mood=random.choice(["happy", "neutral", "sad"]),
                appetite=random.choice(["good", "fair", "poor"]),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(shift_observation)
            db.flush()  # Get the ID
            
            # Then create vital signs
            vital_signs = VitalSign(
                shift_observation_id=shift_observation.id,
                blood_pressure_systolic=random.randint(*vital_signs_ranges["blood_pressure_systolic"]),
                blood_pressure_diastolic=random.randint(*vital_signs_ranges["blood_pressure_diastolic"]),
                heart_rate=random.randint(*vital_signs_ranges["heart_rate"]),
                temperature=round(random.uniform(*vital_signs_ranges["temperature"]), 1),
                oxygen_saturation=random.randint(*vital_signs_ranges["oxygen_saturation"]),
                respiratory_rate=random.randint(*vital_signs_ranges["respiratory_rate"]),
                weight=random.uniform(50, 100),
                height=random.uniform(150, 180),
                bmi=random.uniform(20, 35),
                notes=random.choice([
                    "Valores normales", "Ligera elevación de presión", 
                    "Frecuencia cardíaca regular", "Sin observaciones especiales"
                ]),
                measured_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(vital_signs)
    
    # Create medication schedules
    for cared_person in random.sample(cared_persons, min(len(cared_persons), num_records // 4)):
        for _ in range(random.randint(1, 2)):  # 1-2 medications per person
            med = random.choice(medications)
            schedule = MedicationSchedule(
                cared_person_id=cared_person.id,
                medication_name=med["name"],
                dosage=med["dosage"],
                frequency=med["frequency"],
                start_date=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                end_date=datetime.utcnow() + timedelta(days=random.randint(30, 365)),
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(schedule)
    
    # Create medication logs (need to get medication schedules first)
    medication_schedules = db.query(MedicationSchedule).all()
    if medication_schedules:
        for _ in range(min(num_records // 3, len(medication_schedules))):
            schedule = random.choice(medication_schedules)
            caregiver = random.choice(users) if users else None
            
            log = MedicationLog(
                medication_schedule_id=schedule.id,
                taken_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                confirmed_by=caregiver.id if caregiver else None,
                confirmation_method=random.choice(['app', 'caregiver', 'auto']),
                notes=f"Medicación administrada: {schedule.medication_name}",
                is_missed=random.choice([True, False]),
                side_effects=random.choice([None, "Náuseas leves", "Somnolencia", "Dolor de cabeza"]),
                effectiveness_rating=random.choice(['excelente', 'bueno', 'regular', 'malo']),
                dosage_given=f"{random.randint(1, 3)} comprimido(s)",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(log)
    
    try:
        db.commit()
        print(f"✅ Successfully created medical records")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating medical data: {e}")
        raise


if __name__ == "__main__":
    db = next(get_db())
    populate_medical_data(db) 