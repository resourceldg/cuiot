import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import random
import json
from datetime import datetime, timedelta, time
from app.core.database import get_db
from app.models.geofence import Geofence
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.institution import Institution

# Utilidades
def random_coordinates_argentina():
    """Generar coordenadas aleatorias dentro de Argentina"""
    # Argentina bounds: lat: -55.0 to -21.8, lng: -73.6 to -53.6
    lat = random.uniform(-55.0, -21.8)
    lng = random.uniform(-73.6, -53.6)
    return lat, lng

def random_coordinates_buenos_aires():
    """Generar coordenadas aleatorias en Buenos Aires"""
    # Buenos Aires bounds: lat: -34.8 to -34.4, lng: -58.7 to -58.3
    lat = random.uniform(-34.8, -34.4)
    lng = random.uniform(-58.7, -58.3)
    return lat, lng

def random_polygon_coordinates(center_lat, center_lng, radius_meters=100):
    """Generar coordenadas de polígono alrededor de un punto central"""
    # Convertir metros a grados (aproximadamente)
    lat_offset = radius_meters / 111000  # 1 grado lat ≈ 111km
    lng_offset = radius_meters / (111000 * abs(center_lat) / 90)  # Ajustar por latitud
    
    # Crear un polígono simple (cuadrado)
    coordinates = [
        [center_lat - lat_offset, center_lng - lng_offset],
        [center_lat - lat_offset, center_lng + lng_offset],
        [center_lat + lat_offset, center_lng + lng_offset],
        [center_lat + lat_offset, center_lng - lng_offset],
        [center_lat - lat_offset, center_lng - lng_offset]  # Cerrar el polígono
    ]
    return json.dumps(coordinates)

def populate_geofences():
    """Poblar geofences con datos realistas"""
    db = next(get_db())
    created = 0
    
    # Obtener datos existentes
    users = db.query(User).filter(User.is_active == True).all()
    cared_persons = db.query(CaredPerson).filter(CaredPerson.is_active == True).all()
    institutions = db.query(Institution).filter(Institution.is_active == True).all()
    
    if not users and not cared_persons and not institutions:
        print("⚠️  No hay usuarios, personas cuidadas o instituciones para crear geofences.")
        db.close()
        return
    
    print("📍 Generando geofences...")
    
    # Tipos de geofences disponibles
    geofence_types = Geofence.get_geofence_types()
    trigger_actions = Geofence.get_trigger_actions()
    
    # Nombres de lugares en Argentina
    place_names = [
        "Casa de María", "Residencia San José", "Centro Médico Norte", "Hospital Italiano",
        "Clínica Santa María", "Residencia Los Pinos", "Centro de Día Sur", "Hospital Alemán",
        "Casa de Ana", "Residencia El Bosque", "Centro Médico Este", "Clínica San Martín",
        "Residencia Las Flores", "Hospital Británico", "Centro de Rehabilitación", "Casa de Juan",
        "Residencia San Carlos", "Centro Médico Oeste", "Clínica San Lucas", "Hospital Francés"
    ]
    
    # Mensajes de alerta por tipo
    alert_messages = {
        "safe_zone": "Persona ha entrado en zona segura",
        "restricted_area": "ALERTA: Persona ha entrado en área restringida",
        "home_zone": "Persona ha llegado a casa",
        "work_zone": "Persona ha llegado al trabajo",
        "medical_zone": "Persona ha llegado al centro médico",
        "danger_zone": "ALERTA CRÍTICA: Persona en zona de peligro",
        "custom_zone": "Persona ha entrado en zona personalizada",
        "monitoring_zone": "Persona en zona de monitoreo"
    }
    
    # Crear geofences para usuarios
    for user in users[:5]:  # Máximo 5 usuarios
        for i in range(random.randint(1, 3)):  # 1-3 geofences por usuario
            geofence_type = random.choice(geofence_types)
            trigger_action = random.choice(trigger_actions)
            
            # Verificar si ya existe
            existing = db.query(Geofence).filter_by(
                user_id=user.id,
                geofence_type=geofence_type,
                trigger_action=trigger_action
            ).first()
            
            if existing:
                continue
            
            # Generar ubicación
            if random.choice([True, False]):
                lat, lng = random_coordinates_buenos_aires()
            else:
                lat, lng = random_coordinates_argentina()
            
            # Generar radio o polígono
            use_polygon = random.choice([True, False])
            radius = None
            polygon_coordinates = None
            
            if use_polygon:
                polygon_coordinates = random_polygon_coordinates(lat, lng, random.randint(50, 500))
            else:
                radius = random.uniform(50, 500)
            
            # Generar horario
            start_time = None
            end_time = None
            days_of_week = None
            
            if random.choice([True, False]):
                # Geofence con horario
                start_hour = random.randint(6, 10)
                end_hour = random.randint(18, 22)
                start_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
                end_time = datetime.now().replace(hour=end_hour, minute=0, second=0, microsecond=0)
                days_of_week = ",".join(map(str, random.sample(range(1, 8), random.randint(5, 7))))
            
            # Crear geofence
            geofence = Geofence(
                name=f"{random.choice(place_names)} - {user.first_name}",
                geofence_type=geofence_type,
                description=f"Geofence {geofence_type} para {user.first_name}",
                center_latitude=lat,
                center_longitude=lng,
                radius=radius,
                polygon_coordinates=polygon_coordinates,
                trigger_action=trigger_action,
                alert_message=alert_messages.get(geofence_type, "Alerta de geofence"),
                is_active=True,
                start_time=start_time,
                end_time=end_time,
                days_of_week=days_of_week,
                user_id=user.id,
                cared_person_id=None,
                institution_id=None
            )
            
            db.add(geofence)
            created += 1
    
    # Crear geofences para personas cuidadas
    for cared_person in cared_persons[:8]:  # Máximo 8 personas cuidadas
        for i in range(random.randint(1, 4)):  # 1-4 geofences por persona cuidada
            geofence_type = random.choice(geofence_types)
            trigger_action = random.choice(trigger_actions)
            
            # Verificar si ya existe
            existing = db.query(Geofence).filter_by(
                cared_person_id=cared_person.id,
                geofence_type=geofence_type,
                trigger_action=trigger_action
            ).first()
            
            if existing:
                continue
            
            # Generar ubicación
            if random.choice([True, False]):
                lat, lng = random_coordinates_buenos_aires()
            else:
                lat, lng = random_coordinates_argentina()
            
            # Generar radio o polígono
            use_polygon = random.choice([True, False])
            radius = None
            polygon_coordinates = None
            
            if use_polygon:
                polygon_coordinates = random_polygon_coordinates(lat, lng, random.randint(30, 300))
            else:
                radius = random.uniform(30, 300)
            
            # Generar horario (más restrictivo para personas cuidadas)
            start_time = None
            end_time = None
            days_of_week = None
            
            if random.choice([True, True, False]):  # 66% de probabilidad
                # Geofence con horario
                start_hour = random.randint(7, 9)
                end_hour = random.randint(19, 21)
                start_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
                end_time = datetime.now().replace(hour=end_hour, minute=0, second=0, microsecond=0)
                days_of_week = ",".join(map(str, random.sample(range(1, 8), random.randint(6, 7))))
            
            # Crear geofence
            geofence = Geofence(
                name=f"{random.choice(place_names)} - {cared_person.first_name}",
                geofence_type=geofence_type,
                description=f"Geofence {geofence_type} para {cared_person.first_name} {cared_person.last_name}",
                center_latitude=lat,
                center_longitude=lng,
                radius=radius,
                polygon_coordinates=polygon_coordinates,
                trigger_action=trigger_action,
                alert_message=alert_messages.get(geofence_type, "Alerta de geofence"),
                is_active=True,
                start_time=start_time,
                end_time=end_time,
                days_of_week=days_of_week,
                user_id=None,
                cared_person_id=cared_person.id,
                institution_id=None
            )
            
            db.add(geofence)
            created += 1
    
    # Crear geofences para instituciones
    for institution in institutions[:3]:  # Máximo 3 instituciones
        for i in range(random.randint(2, 5)):  # 2-5 geofences por institución
            geofence_type = random.choice(geofence_types)
            trigger_action = random.choice(trigger_actions)
            
            # Verificar si ya existe
            existing = db.query(Geofence).filter_by(
                institution_id=institution.id,
                geofence_type=geofence_type,
                trigger_action=trigger_action
            ).first()
            
            if existing:
                continue
            
            # Usar coordenadas de la institución si están disponibles
            if institution.latitude and institution.longitude:
                lat, lng = institution.latitude, institution.longitude
                # Agregar pequeña variación
                lat += random.uniform(-0.01, 0.01)
                lng += random.uniform(-0.01, 0.01)
            else:
                lat, lng = random_coordinates_buenos_aires()
            
            # Generar radio o polígono (más grande para instituciones)
            use_polygon = random.choice([True, False])
            radius = None
            polygon_coordinates = None
            
            if use_polygon:
                polygon_coordinates = random_polygon_coordinates(lat, lng, random.randint(100, 1000))
            else:
                radius = random.uniform(100, 1000)
            
            # Generar horario (más amplio para instituciones)
            start_time = None
            end_time = None
            days_of_week = None
            
            if random.choice([True, False]):
                # Geofence con horario
                start_hour = random.randint(6, 8)
                end_hour = random.randint(20, 22)
                start_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
                end_time = datetime.now().replace(hour=end_hour, minute=0, second=0, microsecond=0)
                days_of_week = ",".join(map(str, random.sample(range(1, 8), random.randint(5, 7))))
            
            # Crear geofence
            geofence = Geofence(
                name=f"{institution.name} - {geofence_type.replace('_', ' ').title()}",
                geofence_type=geofence_type,
                description=f"Geofence {geofence_type} para {institution.name}",
                center_latitude=lat,
                center_longitude=lng,
                radius=radius,
                polygon_coordinates=polygon_coordinates,
                trigger_action=trigger_action,
                alert_message=alert_messages.get(geofence_type, "Alerta de geofence"),
                is_active=True,
                start_time=start_time,
                end_time=end_time,
                days_of_week=days_of_week,
                user_id=None,
                cared_person_id=None,
                institution_id=institution.id
            )
            
            db.add(geofence)
            created += 1
    
    try:
        db.commit()
        print(f"✅ Geofences creados: {created} (idempotente)")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando geofences: {e}")
    finally:
        db.close()

def populate_geofences_complete():
    """Poblar geofences completos"""
    print("📍 MÓDULO IOT: GEOFENCES")
    print("=" * 30)
    populate_geofences()

if __name__ == "__main__":
    populate_geofences_complete() 