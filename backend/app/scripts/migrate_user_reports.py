"""
Script de migración para agregar relaciones usuario-reporte
Agrega campos created_by_id y received_by_id a las tablas de reportes
"""
import uuid
from sqlalchemy import text
from app.core.database import engine

def migrate_user_reports():
    """Migración para agregar relaciones usuario-reporte"""
    
    with engine.begin() as conn:
        print("🔄 Iniciando migración de relaciones usuario-reporte...")
        
        # 1. Agregar campo user_type a la tabla users si no existe
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS user_type VARCHAR(20) DEFAULT 'family'
            """))
            print("✅ Campo user_type agregado a tabla users")
        except Exception as e:
            print(f"⚠️  Campo user_type ya existe o error: {e}")
        
        # 2. Agregar campos a la tabla events
        try:
            conn.execute(text("""
                ALTER TABLE events 
                ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id),
                ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id)
            """))
            print("✅ Campos created_by_id y received_by_id agregados a tabla events")
        except Exception as e:
            print(f"⚠️  Campos ya existen o error en events: {e}")
        
        # 3. Agregar campos a la tabla alerts
        try:
            conn.execute(text("""
                ALTER TABLE alerts 
                ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id),
                ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id)
            """))
            print("✅ Campos created_by_id y received_by_id agregados a tabla alerts")
        except Exception as e:
            print(f"⚠️  Campos ya existen o error en alerts: {e}")
        
        # 4. Agregar campos a la tabla reminders
        try:
            conn.execute(text("""
                ALTER TABLE reminders 
                ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id),
                ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id)
            """))
            print("✅ Campos created_by_id y received_by_id agregados a tabla reminders")
        except Exception as e:
            print(f"⚠️  Campos ya existen o error en reminders: {e}")
        
        # 5. Hacer created_by_id NOT NULL en events (después de agregar datos por defecto)
        try:
            # Primero asignar un usuario por defecto si hay eventos sin created_by_id
            conn.execute(text("""
                UPDATE events 
                SET created_by_id = (
                    SELECT id FROM users LIMIT 1
                )
                WHERE created_by_id IS NULL
            """))
            
            # Luego hacer el campo NOT NULL
            conn.execute(text("""
                ALTER TABLE events 
                ALTER COLUMN created_by_id SET NOT NULL
            """))
            print("✅ Campo created_by_id hecho NOT NULL en events")
        except Exception as e:
            print(f"⚠️  Error al hacer created_by_id NOT NULL en events: {e}")
        
        # 6. Hacer created_by_id NOT NULL en alerts
        try:
            # Primero asignar un usuario por defecto si hay alertas sin created_by_id
            conn.execute(text("""
                UPDATE alerts 
                SET created_by_id = (
                    SELECT id FROM users LIMIT 1
                )
                WHERE created_by_id IS NULL
            """))
            
            # Luego hacer el campo NOT NULL
            conn.execute(text("""
                ALTER TABLE alerts 
                ALTER COLUMN created_by_id SET NOT NULL
            """))
            print("✅ Campo created_by_id hecho NOT NULL en alerts")
        except Exception as e:
            print(f"⚠️  Error al hacer created_by_id NOT NULL en alerts: {e}")
        
        # 7. Hacer created_by_id NOT NULL en reminders
        try:
            # Primero asignar un usuario por defecto si hay recordatorios sin created_by_id
            conn.execute(text("""
                UPDATE reminders 
                SET created_by_id = (
                    SELECT id FROM users LIMIT 1
                )
                WHERE created_by_id IS NULL
            """))
            
            # Luego hacer el campo NOT NULL
            conn.execute(text("""
                ALTER TABLE reminders 
                ALTER COLUMN created_by_id SET NOT NULL
            """))
            print("✅ Campo created_by_id hecho NOT NULL en reminders")
        except Exception as e:
            print(f"⚠️  Error al hacer created_by_id NOT NULL en reminders: {e}")
        
        print("🎉 Migración completada exitosamente!")

if __name__ == "__main__":
    migrate_user_reports() 