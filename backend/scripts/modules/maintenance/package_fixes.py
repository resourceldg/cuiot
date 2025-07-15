"""
Funciones de mantenimiento para paquetes (fix y migración de campos)
"""
import json
from app.core.database import get_db
from app.models.package import Package

def list_to_dict(val):
    if isinstance(val, list):
        return {str(k): True for k in val}
    return val

def fix_package_fields_to_dict(db=None):
    """
    Corrige los campos de Package (features, limitations, customizable_options, add_ons_available) convirtiendo listas a dict.
    Si no se pasa una sesión, la gestiona internamente.
    """
    close_db = False
    if db is None:
        db = next(get_db())
        close_db = True
    packages = db.query(Package).all()
    changed = 0
    for pkg in packages:
        updated = False
        for field in ["features", "limitations", "customizable_options", "add_ons_available"]:
            val = getattr(pkg, field)
            if isinstance(val, list):
                setattr(pkg, field, list_to_dict(val))
                updated = True
            elif isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        setattr(pkg, field, list_to_dict(parsed))
                        updated = True
                except Exception:
                    pass
        if updated:
            changed += 1
    db.commit()
    print(f"✅ Paquetes corregidos: {changed}")
    if close_db:
        db.close()
    return changed

def migrate_package_fields_to_dict(db=None):
    """
    Migra los campos de lista a dict en la tabla packages (features, limitations, customizable_options, add_ons_available).
    Si no se pasa una sesión, la gestiona internamente.
    """
    close_db = False
    if db is None:
        db = next(get_db())
        close_db = True
    try:
        packages = db.query(Package).all()
        print(f"Encontrados {len(packages)} paquetes para migrar.")
        migrated = 0
        for pkg in packages:
            changed = False
            for field in ["features", "limitations", "customizable_options", "add_ons_available"]:
                val = getattr(pkg, field)
                if isinstance(val, list):
                    setattr(pkg, field, list_to_dict(val))
                    changed = True
            if changed:
                print(f"Migrado paquete: {pkg.id} ({pkg.name})")
                migrated += 1
        db.commit()
        print("✅ Migración completada.")
        return migrated
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        db.rollback()
        return 0
    finally:
        if close_db:
            db.close() 