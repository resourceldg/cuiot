#!/usr/bin/env python3
"""
Módulo de recordatorios (reminders)
Poblar recordatorios del sistema de cuidado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from app.models.reminder import Reminder
from app.models.reminder_type import ReminderType
from app.models.status_type import StatusType
from app.models.user import User
from app.models.cared_person import CaredPerson
from datetime import datetime, timedelta, timezone, date
import random
import json

def populate_reminders(db: Session, existing_data=None):
    print("   🔔 Poblando recordatorios...")
    reminder_types = existing_data.get("reminder_types", {}) if existing_data else {}
    users = existing_data.get("users", {}) if existing_data else {}
    cared_persons = existing_data.get("cared_persons", {}) if existing_data else {}
    status_types = existing_data.get("status_types", {}) if existing_data else {}
    if not reminder_types:
        reminder_types = {rt.name: rt for rt in db.query(ReminderType).all()}
    if not users:
        users = {f"user_{u.id}": u for u in db.query(User).all()}
    if not cared_persons:
        cared_persons = {f"{cp.first_name}_{cp.last_name}": cp for cp in db.query(CaredPerson).all()}
    if not status_types:
        status_types = {st.name: st for st in db.query(StatusType).all()}
    if not reminder_types or not users or not cared_persons:
        print("      ⚠️ Faltan datos requeridos para poblar recordatorios.")
        return {}
    reminders = {}
    cared_person_keys = list(cared_persons.keys())
    user_keys = list(users.keys())
    for cared_person_key in cared_person_keys[:min(5, len(cared_person_keys))]:
        cared_person = cared_persons[cared_person_key]
        num_reminders = min(5, len(reminder_types))
        reminder_type_names = list(reminder_types.keys())[:num_reminders]
        for reminder_type_name in reminder_type_names:
            reminder_type = reminder_types[reminder_type_name]
            reminder_data = generate_reminder_data(
                reminder_type=reminder_type,
                cared_person=cared_person,
                status_types=status_types
            )
            existing_reminder = db.query(Reminder).filter(
                Reminder.cared_person_id == cared_person.id,
                Reminder.reminder_type_id == reminder_type.id,
                Reminder.title == reminder_data["title"]
            ).first()
            if existing_reminder:
                reminders[f"{cared_person_key}_{reminder_type_name}"] = existing_reminder
                continue
            reminder = Reminder(**reminder_data)
            db.add(reminder)
            db.flush()
            reminders[f"{cared_person_key}_{reminder_type_name}"] = reminder
    for user_key in user_keys[:min(3, len(user_keys))]:
        user = users[user_key]
        if user.email and "admin" not in user.email.lower():
            num_reminders = min(2, len(reminder_types))
            reminder_type_names = list(reminder_types.keys())[:num_reminders]
            for reminder_type_name in reminder_type_names:
                reminder_type = reminder_types[reminder_type_name]
                reminder_data = generate_reminder_data(
                    reminder_type=reminder_type,
                    user=user,
                    status_types=status_types
                )
                existing_reminder = db.query(Reminder).filter(
                    Reminder.user_id == user.id,
                    Reminder.reminder_type_id == reminder_type.id,
                    Reminder.title == reminder_data["title"]
                ).first()
                if existing_reminder:
                    reminders[f"{user_key}_{reminder_type_name}"] = existing_reminder
                    continue
                reminder = Reminder(**reminder_data)
                db.add(reminder)
                db.flush()
                reminders[f"{user_key}_{reminder_type_name}"] = reminder
    db.commit()
    print(f"      ✅ {len(reminders)} recordatorios creados")
    return reminders

def generate_reminder_data(reminder_type, cared_person=None, user=None, status_types=None):
    now = datetime.now(timezone.utc)
    hours_ahead = random.randint(1, 72)
    scheduled_time = now + timedelta(hours=hours_ahead)
    due_date = None
    if random.random() > 0.3:
        due_date = scheduled_time.date() + timedelta(days=random.randint(1, 7))
    repeat_patterns = ["none", "daily", "weekly", "monthly"]
    repeat_pattern = random.choice(repeat_patterns)
    priority = random.randint(1, 10)
    is_important = priority >= 7 or reminder_type.name in ["medication", "appointment"]
    title, description, reminder_data = generate_reminder_content(reminder_type, cared_person, user)
    status_type = None
    completed_at = None
    completed_by = None
    if status_types:
        if random.random() < 0.3:
            status_type = status_types.get("completed")
            completed_at = now - timedelta(hours=random.randint(1, 24))
            if user:
                completed_by = user.id
        else:
            status_type = status_types.get("pending")
    notes = generate_reminder_notes(reminder_type, cared_person, user)
    reminder_data_dict = {
        "reminder_type_id": reminder_type.id,
        "title": title,
        "description": description,
        "scheduled_time": scheduled_time,
        "due_date": due_date,
        "repeat_pattern": repeat_pattern,
        "priority": priority,
        "is_important": is_important,
        "reminder_data": json.dumps(reminder_data) if reminder_data else None,
        "notes": notes,
        "status_type_id": status_type.id if status_type else None,
        "completed_at": completed_at,
        "completed_by": completed_by
    }
    if cared_person:
        reminder_data_dict["cared_person_id"] = cared_person.id
    elif user:
        reminder_data_dict["user_id"] = user.id
    return reminder_data_dict

def generate_reminder_content(reminder_type, cared_person=None, user=None):
    person_name = ""
    if cared_person:
        person_name = f"{cared_person.first_name} {cared_person.last_name}"
    elif user:
        person_name = f"{user.first_name} {user.last_name}"
    reminder_type_name = reminder_type.name
    if reminder_type_name == "medication":
        medications = [
            "Paracetamol 500mg", "Ibuprofeno 400mg", "Omeprazol 20mg",
            "Metformina 500mg", "Amlodipino 5mg", "Losartán 50mg",
            "Atorvastatina 20mg", "Aspirina 100mg", "Vitamina D 1000UI"
        ]
        medication = random.choice(medications)
        title = f"Medicación: {medication}"
        description = f"Recordatorio para tomar {medication}"
        reminder_data = {
            "medication": medication,
            "dosage": medication.split()[-1],
            "instructions": "Tomar con agua",
            "with_food": random.choice([True, False])
        }
    elif reminder_type_name == "appointment":
        appointments = [
            "Consulta médica general", "Revisión cardiología", "Control diabetes",
            "Fisioterapia", "Terapia ocupacional", "Consulta nutrición",
            "Revisión oftalmología", "Control presión arterial", "Análisis de sangre"
        ]
        appointment = random.choice(appointments)
        title = f"Cita médica: {appointment}"
        description = f"Recordatorio para cita de {appointment}"
        reminder_data = {
            "appointment_type": appointment,
            "location": "Centro Médico",
            "duration": "30 minutos",
            "preparation": "Llevar estudios previos"
        }
    elif reminder_type_name == "exercise":
        exercises = [
            "Caminata diaria", "Ejercicios de estiramiento", "Yoga suave",
            "Ejercicios de respiración", "Movilidad articular", "Ejercicios de equilibrio",
            "Natación", "Tai Chi", "Pilates adaptado"
        ]
        exercise = random.choice(exercises)
        title = f"Ejercicio: {exercise}"
        description = f"Recordatorio para realizar {exercise}"
        reminder_data = {
            "exercise_type": exercise,
            "duration": f"{random.randint(15, 45)} minutos",
            "intensity": random.choice(["baja", "moderada", "alta"]),
            "equipment_needed": random.choice([True, False])
        }
    elif reminder_type_name == "meal":
        meals = [
            "Desayuno", "Almuerzo", "Cena", "Merienda", "Colación"
        ]
        meal = random.choice(meals)
        title = f"Comida: {meal}"
        description = f"Recordatorio para {meal.lower()}"
        reminder_data = {
            "meal_type": meal,
            "dietary_restrictions": random.choice(["ninguna", "sin sal", "baja en azúcar", "sin gluten"]),
            "hydration": "Beber agua",
            "supplements": random.choice([True, False])
        }
    elif reminder_type_name == "hygiene":
        hygiene_tasks = [
            "Ducha diaria", "Cepillado de dientes", "Lavado de manos",
            "Corte de uñas", "Lavado de cabello", "Cambio de ropa",
            "Limpieza de prótesis", "Cuidado de la piel"
        ]
        task = random.choice(hygiene_tasks)
        title = f"Higiene: {task}"
        description = f"Recordatorio para {task.lower()}"
        reminder_data = {
            "hygiene_task": task,
            "products_needed": random.choice([True, False]),
            "assistance_needed": random.choice([True, False]),
            "duration": f"{random.randint(5, 20)} minutos"
        }
    elif reminder_type_name == "social":
        social_activities = [
            "Llamada a familia", "Visita de amigos", "Actividad grupal",
            "Paseo al parque", "Conversación con vecinos", "Participación en taller",
            "Celebración familiar", "Reunión social"
        ]
        activity = random.choice(social_activities)
        title = f"Actividad social: {activity}"
        description = f"Recordatorio para {activity.lower()}"
        reminder_data = {
            "activity_type": activity,
            "participants": random.randint(1, 5),
            "location": random.choice(["casa", "parque", "centro comunitario", "casa de familia"]),
            "duration": f"{random.randint(30, 120)} minutos"
        }
    elif reminder_type_name == "checkup":
        checkups = [
            "Control de presión arterial", "Medición de glucosa", "Peso corporal",
            "Temperatura", "Frecuencia cardíaca", "Saturación de oxígeno",
            "Revisión de heridas", "Control de medicación"
        ]
        checkup = random.choice(checkups)
        title = f"Revisión médica: {checkup}"
        description = f"Recordatorio para {checkup.lower()}"
        reminder_data = {
            "checkup_type": checkup,
            "equipment_needed": random.choice([True, False]),
            "record_results": True,
            "alert_threshold": random.choice([True, False])
        }
    elif reminder_type_name == "meditation":
        meditation_types = [
            "Meditación guiada", "Respiración consciente", "Relajación muscular",
            "Visualización positiva", "Mindfulness", "Oración",
            "Ejercicios de gratitud", "Meditación de compasión"
        ]
        meditation = random.choice(meditation_types)
        title = f"Meditación: {meditation}"
        description = f"Recordatorio para {meditation.lower()}"
        reminder_data = {
            "meditation_type": meditation,
            "duration": f"{random.randint(5, 30)} minutos",
            "environment": random.choice(["silencio", "música suave", "naturaleza"]),
            "position": random.choice(["sentado", "acostado", "caminando"])
        }
    else:
        title = f"Recordatorio: {reminder_type_name.title()}"
        description = f"Recordatorio de {reminder_type_name}"
        reminder_data = {
            "type": reminder_type_name,
            "category": reminder_type.category
        }
    return title, description, reminder_data

def generate_reminder_notes(reminder_type, cared_person=None, user=None):
    reminder_type_name = reminder_type.name
    notes_templates = {
        "medication": [
            "Tomar con el estómago lleno",
            "Evitar alcohol mientras tome esta medicación",
            "Mantener refrigerado",
            "Tomar antes de dormir",
            "Consultar si hay efectos secundarios"
        ],
        "appointment": [
            "Llegar 10 minutos antes",
            "Llevar documentación médica",
            "Ayuno de 8 horas requerido",
            "Usar ropa cómoda",
            "Traer lista de medicamentos actuales"
        ],
        "exercise": [
            "Realizar en ambiente ventilado",
            "Detener si hay dolor o malestar",
            "Hidratarse antes y después",
            "Usar ropa cómoda",
            "Realizar bajo supervisión si es necesario"
        ],
        "meal": [
            "Mantener horarios regulares",
            "Masticar lentamente",
            "Evitar distracciones durante la comida",
            "Mantener hidratación",
            "Respetar restricciones dietéticas"
        ],
        "hygiene": [
            "Usar agua templada",
            "Secar bien después del baño",
            "Revisar la piel en busca de lesiones",
            "Usar productos hipoalergénicos",
            "Mantener uñas cortas y limpias"
        ],
        "social": [
            "Preparar tema de conversación",
            "Llevar algo para compartir",
            "Respetar horarios de otros",
            "Mantener distancia social si es necesario",
            "Disfrutar del momento presente"
        ],
        "checkup": [
            "Registrar resultados en el diario",
            "Comparar con mediciones anteriores",
            "Consultar si hay valores anormales",
            "Mantener consistencia en horarios",
            "Usar el mismo equipo si es posible"
        ],
        "meditation": [
            "Encontrar un lugar tranquilo",
            "Apagar dispositivos electrónicos",
            "Mantener postura cómoda",
            "No juzgar los pensamientos",
            "Ser paciente con el proceso"
        ]
    }
    if reminder_type_name in notes_templates:
        return random.choice(notes_templates[reminder_type_name])
    return "Recordatorio importante para el cuidado y bienestar."

def populate_reminders_complete(db: Session, existing_data=None):
    print("🔔 POBLANDO MÓDULO DE RECORDATORIOS...")
    reminders_data = populate_reminders(db, existing_data)
    print("   ✅ Módulo de recordatorios poblado exitosamente")
    return reminders_data 