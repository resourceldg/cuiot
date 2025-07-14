#!/usr/bin/env python3
"""
Módulo de población de eventos de debug (DebugEvent)
Genera eventos de debug para testing, desarrollo y monitoreo del sistema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.debug_event import DebugEvent
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.device import Device
from datetime import datetime, timedelta
import random
import json

def generate_debug_data():
    """Generar datos de debug realistas"""
    debug_data = {
        "test_id": f"test_{random.randint(1000, 9999)}",
        "session_id": f"session_{random.randint(10000, 99999)}",
        "parameters": {
            "timeout": random.randint(30, 300),
            "retries": random.randint(1, 5),
            "batch_size": random.randint(10, 100)
        },
        "metrics": {
            "response_time": random.uniform(0.1, 5.0),
            "memory_usage": random.uniform(10.0, 500.0),
            "cpu_usage": random.uniform(5.0, 95.0)
        }
    }
    return json.dumps(debug_data)

def generate_stack_trace():
    """Generar stack trace simulado"""
    stack_trace = [
        "Traceback (most recent call last):",
        f"  File \"/app/services/debug_service.py\", line {random.randint(10, 100)}, in debug_function",
        "    result = process_data(data)",
        f"  File \"/app/utils/processor.py\", line {random.randint(20, 200)}, in process_data",
        "    return validate_and_transform(input_data)",
        f"  File \"/app/validators/data_validator.py\", line {random.randint(15, 150)}, in validate_and_transform",
        "    raise ValidationError('Invalid data format')",
        "ValidationError: Invalid data format"
    ]
    return "\n".join(stack_trace)

def populate_debug_events(db, existing_data=None):
    print("   🐛 Poblando eventos de debug...")
    
    # Obtener datos existentes
    users = db.query(User).all()
    cared_persons = db.query(CaredPerson).all()
    devices = db.query(Device).all()
    
    # Obtener tipos y configuraciones disponibles
    event_types = DebugEvent.get_event_types()
    severity_levels = DebugEvent.get_severity_levels()
    environments = DebugEvent.get_environments()
    
    # Fuentes de debug
    sources = ["test_suite", "manual_test", "system_test", "integration_test", "performance_test", "load_test", "api_test"]
    
    # Generar eventos de debug
    debug_events_created = 0
    
    # Eventos por usuario
    for user in users[:5]:  # Limitar a 5 usuarios para no saturar
        for _ in range(random.randint(3, 8)):
            event_type = random.choice(event_types)
            severity = random.choice(severity_levels)
            environment = random.choice(environments)
            source = random.choice(sources)
            
            # Generar datos específicos según el tipo
            if event_type == "test_event":
                message = f"Test event for user {user.first_name} - {random.choice(['login', 'logout', 'profile_update', 'data_access'])}"
                event_data = generate_debug_data()
                stack_trace = None
            elif event_type == "debug_event":
                message = f"Debug event: {random.choice(['data_validation', 'api_call', 'database_query', 'cache_miss'])}"
                event_data = generate_debug_data()
                stack_trace = None
            elif event_type == "simulation":
                message = f"Simulation event: {random.choice(['user_behavior', 'system_load', 'network_latency', 'device_failure'])}"
                event_data = generate_debug_data()
                stack_trace = None
            elif event_type in ["system_test", "integration_test"]:
                message = f"{event_type.replace('_', ' ').title()}: {random.choice(['component_test', 'service_test', 'endpoint_test'])}"
                event_data = generate_debug_data()
                stack_trace = generate_stack_trace() if random.random() < 0.3 else None
            else:
                message = f"{event_type.replace('_', ' ').title()}: {random.choice(['performance_check', 'load_balancing', 'error_handling'])}"
                event_data = generate_debug_data()
                stack_trace = generate_stack_trace() if random.random() < 0.2 else None
            
            # Crear evento de debug
            debug_event = DebugEvent(
                event_type=event_type,
                event_subtype=f"{event_type}_{random.randint(1, 5)}",
                severity=severity,
                event_data=event_data,
                message=message,
                stack_trace=stack_trace,
                source=source,
                test_session=f"session_{random.randint(1000, 9999)}",
                environment=environment,
                event_time=datetime.utcnow() - timedelta(minutes=random.randint(1, 1440)),  # Últimas 24 horas
                processed_at=datetime.utcnow() - timedelta(minutes=random.randint(0, 60)),
                user_id=user.id,
                cared_person_id=random.choice(cared_persons).id if cared_persons else None,
                device_id=random.choice(devices).id if devices else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(debug_event)
            debug_events_created += 1
    
    # Eventos por dispositivo
    for device in devices[:10]:  # Limitar a 10 dispositivos
        for _ in range(random.randint(2, 6)):
            event_type = random.choice(["device_event", "sensor_event", "system_event"])
            severity = random.choice(severity_levels)
            environment = random.choice(environments)
            
            message = f"Device {device.name} ({device.type}): {random.choice(['connection_lost', 'data_sync', 'firmware_update', 'battery_low', 'signal_weak'])}"
            event_data = generate_debug_data()
            
            debug_event = DebugEvent(
                event_type=event_type,
                event_subtype=f"device_{random.randint(1, 3)}",
                severity=severity,
                event_data=event_data,
                message=message,
                stack_trace=None,
                source="device_monitor",
                test_session=f"device_session_{random.randint(1000, 9999)}",
                environment=environment,
                event_time=datetime.utcnow() - timedelta(minutes=random.randint(1, 720)),  # Últimas 12 horas
                processed_at=datetime.utcnow() - timedelta(minutes=random.randint(0, 30)),
                user_id=random.choice(users).id if users else None,
                cared_person_id=random.choice(cared_persons).id if cared_persons else None,
                device_id=device.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(debug_event)
            debug_events_created += 1
    
    # Eventos del sistema (sin usuario/dispositivo específico)
    for _ in range(random.randint(10, 20)):
        event_type = random.choice(["system_test", "integration_test", "performance_test"])
        severity = random.choice(severity_levels)
        environment = random.choice(environments)
        
        message = f"System {event_type}: {random.choice(['database_connection', 'api_gateway', 'cache_service', 'notification_service', 'analytics_engine'])}"
        event_data = generate_debug_data()
        stack_trace = generate_stack_trace() if random.random() < 0.4 else None
        
        debug_event = DebugEvent(
            event_type=event_type,
            event_subtype=f"system_{random.randint(1, 5)}",
            severity=severity,
            event_data=event_data,
            message=message,
            stack_trace=stack_trace,
            source="system_monitor",
            test_session=f"system_session_{random.randint(1000, 9999)}",
            environment=environment,
            event_time=datetime.utcnow() - timedelta(minutes=random.randint(1, 2880)),  # Últimas 48 horas
            processed_at=datetime.utcnow() - timedelta(minutes=random.randint(0, 120)),
            user_id=None,
            cared_person_id=None,
            device_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(debug_event)
        debug_events_created += 1
    
    db.commit()
    print(f"   🐛 {debug_events_created} eventos de debug creados")

def populate_debug_events_complete(db, existing_data=None):
    populate_debug_events(db, existing_data)

if __name__ == "__main__":
    from app.core.database import get_db
    db = next(get_db())
    try:
        populate_debug_events_complete(db)
    finally:
        db.close() 