#!/usr/bin/env python3
"""
Script para migrar los campos de lista a dict en la tabla packages.
Convierte features, limitations, customizable_options y add_ons_available de list a dict.
"""
import sys
from pathlib import Path
import json

# Asegurar que el path incluye la raíz del backend
current_path = Path(__file__).parent.parent
if str(current_path) not in sys.path:
    sys.path.insert(0, str(current_path))

from app.core.database import get_db
from app.models.package import Package

def list_to_dict(val):
    if isinstance(val, list):
        # Convierte ['a', 'b'] -> {'a': True, 'b': True}
        return {str(k): True for k in val}
    return val

def migrate_packages():
    db = next(get_db())
    try:
        packages = db.query(Package).all()
        print(f"Encontrados {len(packages)} paquetes para migrar.")
        for pkg in packages:
            changed = False
            for field in ["features", "limitations", "customizable_options", "add_ons_available"]:
                val = getattr(pkg, field)
                if isinstance(val, list):
                    setattr(pkg, field, list_to_dict(val))
                    changed = True
            if changed:
                print(f"Migrado paquete: {pkg.id} ({pkg.name})")
        db.commit()
        print("✅ Migración completada.")
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_packages() 