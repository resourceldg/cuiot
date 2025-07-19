#!/usr/bin/env python3
"""
Script para actualizar automáticamente los modelos SQLAlchemy con mejoras del DDL
Implementa CASCADE DELETE y SET NULL en las relaciones apropiadas
"""

import os
import re
from pathlib import Path

# Configuración de rutas
BACKEND_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = BACKEND_DIR / "app" / "models"

# Mapeo de relaciones que deben tener CASCADE DELETE
CASCADE_RELATIONS = {
    # User -> UserRole
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> UserPackage
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> ServiceSubscription
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> BillingRecord
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> LocationTracking
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> Geofence
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> DebugEvent
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> Device
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> Event
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> Alert
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> Reminder
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # User -> CaredPerson
    r'user_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Caregiver -> CaregiverAssignment
    r'caregiver_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Caregiver -> CaregiverInstitution
    r'caregiver_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Caregiver -> CaregiverScore
    r'caregiver_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Caregiver -> CaregiverReview
    r'caregiver_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Reviewer -> CaregiverReview
    r'reviewer_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Reviewer -> InstitutionReview
    r'reviewer_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # VerifiedBy -> ShiftObservation
    r'verified_by = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Caregiver -> ShiftObservation
    r'caregiver_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # ConfirmedBy -> MedicationLog
    r'confirmed_by = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'confirmed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # RegisteredBy -> CaredPersonInstitution
    r'registered_by = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'registered_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")',
    
    # Package -> UserPackage
    r'package_id = Column\(UUID\(as_uuid=True\), ForeignKey\("packages\.id"\)': 
    'package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id", ondelete="CASCADE")',
    
    # UserPackage -> UserPackageAddOn
    r'user_package_id = Column\(UUID\(as_uuid=True\), ForeignKey\("user_packages\.id"\)': 
    'user_package_id = Column(UUID(as_uuid=True), ForeignKey("user_packages.id", ondelete="CASCADE")',
}

# Mapeo de relaciones que deben tener SET NULL
SET_NULL_RELATIONS = {
    # User -> UserRole (assigned_by)
    r'assigned_by = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")',
    
    # User -> UserPackage (legal_representative_id)
    r'legal_representative_id = Column\(UUID\(as_uuid=True\), ForeignKey\("users\.id"\)': 
    'legal_representative_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")',
    
    # Institution -> User
    r'institution_id = Column\(Integer, ForeignKey\("institutions\.id"\)': 
    'institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="SET NULL")',
}

# Mapeo de relaciones que deben tener RESTRICT
RESTRICT_RELATIONS = {
    # Role -> UserRole
    r'role_id = Column\(UUID\(as_uuid=True\), ForeignKey\("roles\.id"\)': 
    'role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT")',
}

def update_file_content(content: str, file_path: str) -> tuple[str, list[str]]:
    """Actualiza el contenido de un archivo con las mejoras del DDL"""
    updated_content = content
    changes_made = []
    
    # Aplicar CASCADE DELETE
    for pattern, replacement in CASCADE_RELATIONS.items():
        if re.search(pattern, content):
            updated_content = re.sub(pattern, replacement, updated_content)
            changes_made.append(f"CASCADE DELETE: {pattern[:50]}...")
    
    # Aplicar SET NULL
    for pattern, replacement in SET_NULL_RELATIONS.items():
        if re.search(pattern, content):
            updated_content = re.sub(pattern, replacement, updated_content)
            changes_made.append(f"SET NULL: {pattern[:50]}...")
    
    # Aplicar RESTRICT
    for pattern, replacement in RESTRICT_RELATIONS.items():
        if re.search(pattern, content):
            updated_content = re.sub(pattern, replacement, updated_content)
            changes_made.append(f"RESTRICT: {pattern[:50]}...")
    
    return updated_content, changes_made

def update_model_file(file_path: Path) -> bool:
    """Actualiza un archivo de modelo específico"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content, changes = update_file_content(content, str(file_path))
        
        if changes:
            # Crear backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Escribir contenido actualizado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ {file_path.name}: {len(changes)} cambios aplicados")
            for change in changes:
                print(f"   - {change}")
            return True
        else:
            print(f"⏭️  {file_path.name}: Sin cambios necesarios")
            return False
            
    except Exception as e:
        print(f"❌ Error actualizando {file_path.name}: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando actualización de modelos con mejoras DDL...")
    print(f"📁 Directorio de modelos: {MODELS_DIR}")
    
    if not MODELS_DIR.exists():
        print(f"❌ Directorio de modelos no encontrado: {MODELS_DIR}")
        return
    
    # Encontrar todos los archivos de modelos
    model_files = list(MODELS_DIR.glob("*.py"))
    model_files = [f for f in model_files if f.name != "__init__.py"]
    
    print(f"📋 Encontrados {len(model_files)} archivos de modelos")
    
    updated_count = 0
    total_changes = 0
    
    for model_file in model_files:
        print(f"\n📝 Procesando: {model_file.name}")
        if update_model_file(model_file):
            updated_count += 1
    
    print(f"\n🎉 Resumen:")
    print(f"   - Archivos procesados: {len(model_files)}")
    print(f"   - Archivos actualizados: {updated_count}")
    print(f"   - Archivos sin cambios: {len(model_files) - updated_count}")
    
    if updated_count > 0:
        print(f"\n💡 Próximos pasos:")
        print(f"   1. Revisar los archivos .backup generados")
        print(f"   2. Ejecutar tests para verificar que todo funciona")
        print(f"   3. Generar nueva migración Alembic si es necesario")
        print(f"   4. Hacer commit de los cambios")

if __name__ == "__main__":
    main() 