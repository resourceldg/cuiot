#!/usr/bin/env python3
"""
Script Principal: Población Modular de Datos CUIOT
Consolida la ejecución de todos los módulos de población
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from scripts.modules.core.device_types import DeviceTypeManager
from scripts.modules.iot.device_manager import DeviceManager
from scripts.modules.iot.devices import populate_devices
from scripts.modules.iot.events import populate_events
from scripts.modules.iot.alerts import populate_alerts
from scripts.modules.iot.tracking import populate_tracking
from scripts.modules.care import (
    populate_cared_persons,
    populate_caregivers,
    populate_medical_data,
    populate_care_assignments
)
from scripts.modules.business.institutions import populate_institutions
from scripts.modules.business.packages import populate_packages
from scripts.modules.business.users import populate_users
from scripts.modules.business.addons import (
    populate_package_add_ons,
    populate_user_packages,
    populate_user_package_add_ons,
    populate_addons_complete
)
from scripts.modules.business.billing import (
    populate_billing_records,
    populate_billing_complete
)
from scripts.modules.business.scoring import (
    populate_caregiver_scores,
    populate_caregiver_reviews,
    populate_institution_scores,
    populate_institution_reviews,
    populate_scoring_complete
)
from scripts.modules.care.referrals import (
    populate_referrals,
    populate_medical_referrals,
    populate_referrals_complete
)
from scripts.modules.iot.geofences import (
    populate_geofences,
    populate_geofences_complete
)
from scripts.modules.care.reminders import (
    populate_reminders,
    populate_reminders_complete
)
from scripts.modules.care.emergency_protocols import (
    populate_emergency_protocols,
    populate_emergency_protocols_complete
)
from scripts.modules.iot.debug_events import (
    populate_debug_events,
    populate_debug_events_complete
)
from scripts.modules.iot.device_configs import (
    populate_device_configs,
    populate_device_configs_complete
)
from sqlalchemy.orm import Session

def run_core_population():
    """Ejecutar población de datos core"""
    print("\n🔧 MÓDULO CORE")
    print("=" * 30)
    
    db = next(get_db())
    try:
        # Agregar tipos de dispositivos especializados
        DeviceTypeManager.populate_device_types(db)
    finally:
        db.close()

def run_iot_population():
    """Ejecutar población de datos IoT"""
    print("\n📱 MÓDULO IoT")
    print("=" * 30)
    
    db = next(get_db())
    try:
        # Corregir dispositivos sin package_id
        DeviceManager.fix_devices_without_package(db)
        
        # Poblar dispositivos
        devices_created = DeviceManager.populate_devices(db, devices_per_type=2)
        
        if devices_created and devices_created > 0:
            # Poblar eventos para los dispositivos
            populate_events(db)
            
            # Poblar alertas para los dispositivos
            populate_alerts(db)
            
            # Poblar tracking de ubicación
            populate_tracking(db)
        
    finally:
        db.close()

def run_care_population():
    """Ejecutar población de datos de cuidado"""
    print("\n🏥 MÓDULO CARE")
    print("=" * 30)
    
    db = next(get_db())
    try:
        # Poblar personas cuidadas
        populate_cared_persons(db, num_cared_persons=15)
        
        # Poblar cuidadores
        populate_caregivers(db, num_caregivers=10)
        
        # Poblar datos médicos
        populate_medical_data(db, num_records=30)
        
        # Poblar asignaciones de cuidado
        populate_care_assignments(db, num_assignments=20)
        
    finally:
        db.close()

def run_business_institutions_population():
    """Ejecutar población de instituciones (Business)"""
    print("\n🏢 MÓDULO BUSINESS: INSTITUCIONES")
    print("=" * 30)
    populate_institutions()

def run_business_packages_population():
    """Ejecutar población de paquetes (Business)"""
    print("\n📦 MÓDULO BUSINESS: PAQUETES")
    print("=" * 30)
    populate_packages()

def run_business_users_population():
    """Ejecutar población de usuarios (Business)"""
    print("\n👥 MÓDULO BUSINESS: USUARIOS")
    print("=" * 30)
    populate_users()

def run_business_addons_population():
    """Ejecutar población de add-ons y suscripciones (Business)"""
    print("\n🎯 MÓDULO BUSINESS: ADD-ONS Y SUSCRIPCIONES")
    print("=" * 30)
    populate_addons_complete()

def run_business_addons_package_only():
    """Ejecutar solo población de add-ons de paquetes"""
    print("\n📦 MÓDULO BUSINESS: ADD-ONS DE PAQUETES")
    print("=" * 30)
    populate_package_add_ons()

def run_business_user_packages_only():
    """Ejecutar solo población de suscripciones de usuario"""
    print("\n👤 MÓDULO BUSINESS: SUSCRIPCIONES DE USUARIO")
    print("=" * 30)
    populate_user_packages()

def run_business_user_addons_only():
    """Ejecutar solo población de add-ons de usuario"""
    print("\n🎯 MÓDULO BUSINESS: ADD-ONS DE USUARIO")
    print("=" * 30)
    populate_user_package_add_ons()

def run_business_billing_population():
    """Ejecutar población de facturación (Business)"""
    print("\n💰 MÓDULO BUSINESS: FACTURACIÓN")
    print("=" * 30)
    populate_billing_complete()

def run_business_scoring_population():
    """Ejecutar población de scoring y reviews (Business)"""
    print("\n🏆 MÓDULO BUSINESS: SCORING Y REVIEWS")
    print("=" * 30)
    populate_scoring_complete()

def run_business_caregiver_scores_only():
    """Ejecutar solo población de puntuaciones de cuidadores"""
    print("\n👨‍⚕️ MÓDULO BUSINESS: PUNTUACIONES DE CUIDADORES")
    print("=" * 30)
    populate_caregiver_scores()

def run_business_caregiver_reviews_only():
    """Ejecutar solo población de reseñas de cuidadores"""
    print("\n⭐ MÓDULO BUSINESS: RESEÑAS DE CUIDADORES")
    print("=" * 30)
    populate_caregiver_reviews()

def run_business_institution_scores_only():
    """Ejecutar solo población de puntuaciones de instituciones"""
    print("\n🏥 MÓDULO BUSINESS: PUNTUACIONES DE INSTITUCIONES")
    print("=" * 30)
    populate_institution_scores()

def run_business_institution_reviews_only():
    """Ejecutar solo población de reseñas de instituciones"""
    print("\n🏢 MÓDULO BUSINESS: RESEÑAS DE INSTITUCIONES")
    print("=" * 30)
    populate_institution_reviews()

def run_care_referrals_population():
    """Ejecutar población de referencias y derivaciones médicas (Care)"""
    print("\n📋 MÓDULO CARE: REFERENCIAS Y DERIVACIONES MÉDICAS")
    print("=" * 30)
    populate_referrals_complete()

def run_care_referrals_only():
    """Ejecutar solo población de referencias generales"""
    print("\n📋 MÓDULO CARE: REFERENCIAS GENERALES")
    print("=" * 30)
    populate_referrals()

def run_care_medical_referrals_only():
    """Ejecutar solo población de derivaciones médicas"""
    print("\n🏥 MÓDULO CARE: DERIVACIONES MÉDICAS")
    print("=" * 30)
    populate_medical_referrals()

def run_iot_geofences_population():
    """Ejecutar población de geofences (IoT)"""
    print("\n📍 MÓDULO IOT: GEOFENCES")
    print("=" * 30)
    populate_geofences_complete()

def run_iot_geofences_only():
    """Ejecutar solo población de geofences"""
    print("\n📍 MÓDULO IOT: GEOFENCES")
    print("=" * 30)
    populate_geofences()

def run_care_reminders_population():
    """Ejecutar población de recordatorios (Care)"""
    print("\n🔔 MÓDULO CARE: RECORDATORIOS")
    print("=" * 30)
    
    db = next(get_db())
    try:
        populate_reminders_complete(db)
    finally:
        db.close()

def run_care_reminders_only():
    """Ejecutar solo población de recordatorios"""
    print("\n🔔 MÓDULO CARE: RECORDATORIOS")
    print("=" * 30)
    
    db = next(get_db())
    try:
        populate_reminders(db)
    finally:
        db.close()

def run_care_emergency_protocols_population():
    """Ejecutar población de protocolos de emergencia (Care)"""
    print("\n🚨 MÓDULO CARE: PROTOCOLOS DE EMERGENCIA")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_emergency_protocols_complete(db)
    finally:
        db.close()

def run_care_emergency_protocols_only():
    """Ejecutar solo población de protocolos de emergencia"""
    print("\n🚨 MÓDULO CARE: PROTOCOLOS DE EMERGENCIA")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_emergency_protocols(db)
    finally:
        db.close()

def run_iot_debug_events_population():
    """Ejecutar población de eventos de debug (IoT)"""
    print("\n🐛 MÓDULO IOT: EVENTOS DE DEBUG")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_debug_events_complete(db)
    finally:
        db.close()

def run_iot_debug_events_only():
    """Ejecutar solo población de eventos de debug"""
    print("\n🐛 MÓDULO IOT: EVENTOS DE DEBUG")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_debug_events(db)
    finally:
        db.close()

def run_iot_device_configs_population():
    """Ejecutar población de configuraciones de dispositivos (IoT)"""
    print("\n⚙️ MÓDULO IOT: CONFIGURACIONES DE DISPOSITIVOS")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_device_configs_complete(db)
    finally:
        db.close()

def run_iot_device_configs_only():
    """Ejecutar solo población de configuraciones de dispositivos"""
    print("\n⚙️ MÓDULO IOT: CONFIGURACIONES DE DISPOSITIVOS")
    print("=" * 30)
    db = next(get_db())
    try:
        populate_device_configs(db)
    finally:
        db.close()

def run_full_population():
    """Ejecutar población completa de datos"""
    print("🚀 POBLACIÓN COMPLETA DE DATOS CUIOT")
    print("=" * 50)
    
    # Core
    run_core_population()
    
    # IoT
    run_iot_population()
    
    # Care
    run_care_population()
    
    # Business
    run_business_institutions_population()
    run_business_packages_population()
    run_business_users_population()
    run_business_addons_population()
    run_business_billing_population()
    run_business_scoring_population()
    run_care_referrals_population()
    
    # Care: Recordatorios
    run_care_reminders_population()
    # Care: Protocolos de emergencia
    run_care_emergency_protocols_population()
    # IoT: Eventos de debug
    run_iot_debug_events_population()
    # IoT: Configuraciones de dispositivos
    run_iot_device_configs_population()
    
    print("\n✅ Población completa finalizada exitosamente")

def show_menu():
    """Mostrar menú de opciones"""
    print("\n🔧 GESTOR DE POBLACIÓN MODULAR CUIOT")
    print("=" * 50)
    print("1. Población Core (tipos de dispositivos)")
    print("2. Población IoT (dispositivos, eventos, alertas, tracking)")
    print("3. Población Care (personas cuidadas, cuidadores, datos médicos)")
    print("4. Población Completa")
    print("5. Solo corregir dispositivos sin package_id")
    print("6. Solo poblar dispositivos")
    print("7. Solo poblar eventos y alertas")
    print("8. Población Business: Instituciones")
    print("9. Población Business: Paquetes")
    print("10. Población Business: Usuarios")
    print("11. Población Business: Add-ons y Suscripciones (Completo)")
    print("12. Solo Add-ons de Paquetes")
    print("13. Solo Suscripciones de Usuario")
    print("14. Solo Add-ons de Usuario")
    print("15. Población Business: Facturación")
    print("16. Población Business: Scoring y Reviews")
    print("17. Solo Puntuaciones de Cuidadores")
    print("18. Solo Reseñas de Cuidadores")
    print("19. Solo Puntuaciones de Instituciones")
    print("20. Solo Reseñas de Instituciones")
    print("21. Población Care: Referencias y Derivaciones Médicas")
    print("22. Solo Referencias Generales")
    print("23. Solo Derivaciones Médicas")
    print("24. Población IoT: Geofences")
    print("25. Solo Geofences")
    print("26. Población Care: Recordatorios")
    print("27. Solo Recordatorios")
    print("28. Población Care: Protocolos de Emergencia")
    print("29. Solo Protocolos de Emergencia")
    print("30. Población IoT: Eventos de Debug")
    print("31. Solo Eventos de Debug")
    print("32. Población IoT: Configuraciones de Dispositivos")
    print("33. Solo Configuraciones de Dispositivos")
    print("0. Salir")

def main():
    """Función principal"""
    import argparse
    parser = argparse.ArgumentParser(description="Población modular de datos CUIOT")
    parser.add_argument('--core', action='store_true', help='Poblar datos core')
    parser.add_argument('--iot', action='store_true', help='Poblar módulo IoT')
    parser.add_argument('--care', action='store_true', help='Poblar módulo Care')
    parser.add_argument('--institutions', action='store_true', help='Poblar instituciones')
    parser.add_argument('--packages', action='store_true', help='Poblar paquetes')
    parser.add_argument('--users', action='store_true', help='Poblar usuarios')
    parser.add_argument('--addons', action='store_true', help='Poblar add-ons y suscripciones')
    parser.add_argument('--billing', action='store_true', help='Poblar facturación')
    parser.add_argument('--scoring', action='store_true', help='Poblar scoring y reviews')
    parser.add_argument('--referrals', action='store_true', help='Poblar referencias y derivaciones médicas')
    parser.add_argument('--geofences', action='store_true', help='Poblar geofences (zonas seguras, áreas restringidas, etc.)')
    parser.add_argument('--reminders', action='store_true', help='Poblar recordatorios (medicación, citas, ejercicio, etc.)')
    parser.add_argument('--emergency-protocols', action='store_true', help='Poblar protocolos de emergencia (globales e institucionales)')
    parser.add_argument('--debug-events', action='store_true', help='Poblar eventos de debug (testing, desarrollo, monitoreo)')
    parser.add_argument('--device-configs', action='store_true', help='Poblar configuraciones de dispositivos (personalización IoT)')
    parser.add_argument('--all', action='store_true', help='Poblar todo el sistema (full)')
    args = parser.parse_args()

    if args.core:
        run_core_population()
        return
    if args.iot:
        run_iot_population()
        return
    if args.care:
        run_care_population()
        return
    if args.institutions:
        run_business_institutions_population()
        return
    if args.packages:
        run_business_packages_population()
        return
    if args.users:
        run_business_users_population()
        return
    if args.addons:
        run_business_addons_population()
        return
    if args.billing:
        run_business_billing_population()
        return
    if args.scoring:
        run_business_scoring_population()
        return
    if args.referrals:
        run_care_referrals_population()
        return
    if args.geofences:
        run_iot_geofences_population()
        return
    if args.reminders:
        run_care_reminders_population()
        return
    if args.emergency_protocols:
        run_care_emergency_protocols_population()
        return
    if args.debug_events:
        run_iot_debug_events_population()
        return
    if args.device_configs:
        run_iot_device_configs_population()
        return
    if args.all:
        run_full_population()
        return

    # Si no hay argumentos, mostrar menú interactivo
    while True:
        show_menu()
        choice = input("\nSelecciona una opción (0-33): ").strip()
        if choice == "0":
            print("👋 ¡Hasta luego!")
            break
        elif choice == "1":
            run_core_population()
        elif choice == "2":
            run_iot_population()
        elif choice == "3":
            run_care_population()
        elif choice == "4":
            run_full_population()
        elif choice == "5":
            DeviceManager.fix_devices_without_package()
        elif choice == "6":
            devices_per_type = int(input("Dispositivos por tipo (1-5): ") or "2")
            DeviceManager.populate_devices(devices_per_type=devices_per_type)
        elif choice == "7":
            db = next(get_db())
            try:
                populate_events(db)
                populate_alerts(db)
                populate_tracking(db)
            finally:
                db.close()
        elif choice == "8":
            run_business_institutions_population()
        elif choice == "9":
            run_business_packages_population()
        elif choice == "10":
            run_business_users_population()
        elif choice == "11":
            run_business_addons_population()
        elif choice == "12":
            run_business_addons_package_only()
        elif choice == "13":
            run_business_user_packages_only()
        elif choice == "14":
            run_business_user_addons_only()
        elif choice == "15":
            run_business_billing_population()
        elif choice == "16":
            run_business_scoring_population()
        elif choice == "17":
            run_business_caregiver_scores_only()
        elif choice == "18":
            run_business_caregiver_reviews_only()
        elif choice == "19":
            run_business_institution_scores_only()
        elif choice == "20":
            run_business_institution_reviews_only()
        elif choice == "21":
            run_care_referrals_population()
        elif choice == "22":
            run_care_referrals_only()
        elif choice == "23":
            run_care_medical_referrals_only()
        elif choice == "24":
            run_iot_geofences_population()
        elif choice == "25":
            run_iot_geofences_only()
        elif choice == "26":
            run_care_reminders_population()
        elif choice == "27":
            run_care_reminders_only()
        elif choice == "28":
            run_care_emergency_protocols_population()
        elif choice == "29":
            run_care_emergency_protocols_only()
        elif choice == "30":
            run_iot_debug_events_population()
        elif choice == "31":
            run_iot_debug_events_only()
        elif choice == "32":
            run_iot_device_configs_population()
        elif choice == "33":
            run_iot_device_configs_only()
        else:
            print("❌ Opción no válida")
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main() 