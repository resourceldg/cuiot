-- Inicialización de la base de datos para el Sistema Integral de Monitoreo MVP

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Eliminar o comentar todas las tablas e inserts de negocio para evitar conflicto con Alembic
-- (users, elderly_persons, devices, events, alerts, reminders, device_configs, índices, inserts)

-- Función y trigger para asegurar que los campos JSONB sean realmente JSONB (no strings)
CREATE OR REPLACE FUNCTION ensure_jsonb_fields()
RETURNS TRIGGER AS $$
BEGIN
  -- emergency_contacts
  IF TG_OP = 'INSERT' OR NEW.emergency_contacts IS DISTINCT FROM OLD.emergency_contacts THEN
    IF NEW.emergency_contacts IS NOT NULL AND jsonb_typeof(NEW.emergency_contacts) IS NULL THEN
      BEGIN
        NEW.emergency_contacts := NEW.emergency_contacts::jsonb;
      EXCEPTION WHEN OTHERS THEN
        NEW.emergency_contacts := '[]'::jsonb;
      END;
    END IF;
  END IF;
  -- medical_conditions
  IF TG_OP = 'INSERT' OR NEW.medical_conditions IS DISTINCT FROM OLD.medical_conditions THEN
    IF NEW.medical_conditions IS NOT NULL AND jsonb_typeof(NEW.medical_conditions) IS NULL THEN
      BEGIN
        NEW.medical_conditions := NEW.medical_conditions::jsonb;
      EXCEPTION WHEN OTHERS THEN
        NEW.medical_conditions := '[]'::jsonb;
      END;
    END IF;
  END IF;
  -- medications
  IF TG_OP = 'INSERT' OR NEW.medications IS DISTINCT FROM OLD.medications THEN
    IF NEW.medications IS NOT NULL AND jsonb_typeof(NEW.medications) IS NULL THEN
      BEGIN
        NEW.medications := NEW.medications::jsonb;
      EXCEPTION WHEN OTHERS THEN
        NEW.medications := '[]'::jsonb;
      END;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Los triggers se deben crear solo si existen las tablas, así que Alembic los puede crear después si es necesario.
-- DROP TRIGGER IF EXISTS ensure_jsonb_fields_trigger ON cared_persons;
-- CREATE TRIGGER ensure_jsonb_fields_trigger
-- BEFORE INSERT OR UPDATE ON cared_persons
-- FOR EACH ROW EXECUTE FUNCTION ensure_jsonb_fields();

-- Función para eventos (campo value)
CREATE OR REPLACE FUNCTION ensure_event_value_jsonb()
RETURNS TRIGGER AS $$
BEGIN
  -- value field in events
  IF TG_OP = 'INSERT' OR NEW.value IS DISTINCT FROM OLD.value THEN
    IF NEW.value IS NOT NULL AND jsonb_typeof(NEW.value) IS NULL THEN
      BEGIN
        NEW.value := NEW.value::jsonb;
      EXCEPTION WHEN OTHERS THEN
        NEW.value := '{}'::jsonb;
      END;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- DROP TRIGGER IF EXISTS ensure_event_value_jsonb_trigger ON events;
-- CREATE TRIGGER ensure_event_value_jsonb_trigger
--     BEFORE INSERT OR UPDATE ON events
--     FOR EACH ROW
--     EXECUTE FUNCTION ensure_event_value_jsonb(); 