#!/usr/bin/env python3
"""
Script para actualizar los permisos del rol admin en la base de datos CUIOT
"""
import sys
import os
import json
from pathlib import Path

# Asegurar que el path incluye la raíz del backend
current_path = Path(__file__).parent.parent
if str(current_path) not in sys.path:
    sys.path.insert(0, str(current_path))

from app.core.database import get_db
from app.models.role import Role
from datetime import datetime

# Script para dejar solo el rol 'Administrador del sistema' como de sistema
from app.core.database import SessionLocal

def main():
    session = SessionLocal()
    try:
        # Cambiar todos los roles a is_system=False
        session.query(Role).update({Role.is_system: False})
        # Buscar el rol de admin (puede ser 'admin' o 'Administrador del sistema')
        admin_role = session.query(Role).filter(
            (Role.name == 'admin') | (Role.name == 'Administrador del sistema')
        ).first()
        if admin_role:
            admin_role.is_system = True
            print(f"Rol de sistema: {admin_role.name}")
        else:
            print("No se encontró el rol de administrador de sistema.")
        session.commit()
        print("Actualización completada.")
    finally:
        session.close()

if __name__ == "__main__":
    main() 