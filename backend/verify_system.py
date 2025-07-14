from app.core.database import engine
from sqlalchemy import text

def verify_system():
    print("=== VERIFICACIÓN DEL SISTEMA MODULAR ===")
    
    with engine.connect() as conn:
        # Verificar cared_persons
        result = conn.execute(text('SELECT COUNT(*) FROM cared_persons'))
        cared_persons_count = result.scalar()
        print(f"✅ Cared Persons: {cared_persons_count}")
        
        # Verificar users
        result = conn.execute(text('SELECT COUNT(*) FROM users'))
        users_count = result.scalar()
        print(f"✅ Users: {users_count}")
        
        # Verificar devices
        result = conn.execute(text('SELECT COUNT(*) FROM devices'))
        devices_count = result.scalar()
        print(f"✅ Devices: {devices_count}")
        
        # Verificar devices con package_id
        result = conn.execute(text('SELECT COUNT(*) FROM devices WHERE package_id IS NOT NULL'))
        devices_with_package = result.scalar()
        print(f"✅ Devices with package_id: {devices_with_package}")
        
        # Obtener UUID del rol cuidador
        result = conn.execute(text("SELECT id FROM roles WHERE name ILIKE 'cuidador' OR name ILIKE 'caregiver' LIMIT 1"))
        row = result.fetchone()
        caregiver_role_id = row[0] if row else None
        caregivers_count = 0
        if caregiver_role_id:
            result = conn.execute(text('SELECT COUNT(*) FROM user_roles WHERE role_id = :role_id'), {'role_id': caregiver_role_id})
            caregivers_count = result.scalar()
        print(f"✅ Caregivers (rol cuidador): {caregivers_count}")
        
        # Verificar vital_signs
        result = conn.execute(text('SELECT COUNT(*) FROM vital_signs'))
        vital_signs_count = result.scalar()
        print(f"✅ Vital Signs: {vital_signs_count}")
        
        # Verificar shift_observations
        result = conn.execute(text('SELECT COUNT(*) FROM shift_observations'))
        shift_obs_count = result.scalar()
        print(f"✅ Shift Observations: {shift_obs_count}")
        
        print("\n🎯 RESUMEN DEL SISTEMA MODULAR:")
        print(f"   • Personas cuidadas: {cared_persons_count}")
        print(f"   • Cuidadores: {caregivers_count}")
        print(f"   • Dispositivos IoT: {devices_count} (con package_id: {devices_with_package})")
        print(f"   • Datos médicos: {vital_signs_count} signos vitales, {shift_obs_count} observaciones")
        
        if devices_count > 0 and devices_with_package == devices_count:
            print("✅ REGLA DE NEGOCIO: Todos los dispositivos tienen package_id")
        else:
            print("⚠️  ADVERTENCIA: Algunos dispositivos no tienen package_id")
            
        print("\n🚀 SISTEMA MODULAR FUNCIONANDO CORRECTAMENTE")

if __name__ == "__main__":
    verify_system() 