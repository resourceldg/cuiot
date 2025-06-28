-- Inicialización de la base de datos para Viejos Son Los Trapos MVP

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios (familiares)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'family', -- 'family', 'employee'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de adultos mayores
CREATE TABLE IF NOT EXISTS elderly_persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INTEGER,
    address TEXT,
    emergency_contacts JSONB, -- Array de contactos de emergencia
    medical_conditions JSONB DEFAULT '[]'::jsonb, -- Array de condiciones médicas
    medications JSONB DEFAULT '[]'::jsonb, -- Array de medicamentos
    is_active BOOLEAN DEFAULT true NOT NULL,
    is_deleted BOOLEAN DEFAULT false, -- Campo para soft delete
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de dispositivos IoT
CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_person_id UUID REFERENCES elderly_persons(id) ON DELETE CASCADE,
    device_id VARCHAR(100) UNIQUE NOT NULL, -- ID único del dispositivo ESP32
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'ready', -- ready, offline, error, off
    type VARCHAR(50) DEFAULT 'unknown', -- smart_watch, panic_button, motion_sensor, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de eventos/sensores
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_person_id UUID REFERENCES elderly_persons(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    title VARCHAR(120),
    description TEXT,
    event_type VARCHAR(50) NOT NULL, -- 'movement', 'sos_button', 'temperature', 'humidity', 'medical', 'family', etc.
    value JSONB, -- Datos del evento (temperatura, humedad, etc.)
    location VARCHAR(100),
    start_datetime TIMESTAMP WITH TIME ZONE,
    end_datetime TIMESTAMP WITH TIME ZONE,
    created_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    received_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de alertas
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_person_id UUID REFERENCES elderly_persons(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- 'no_movement', 'sos', 'temperature', 'medication'
    message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    is_resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    received_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de recordatorios
CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    elderly_person_id UUID REFERENCES elderly_persons(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    reminder_type VARCHAR(50) NOT NULL, -- 'medication', 'appointment', 'activity'
    scheduled_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT true,
    days_of_week INTEGER[], -- [1,2,3,4,5,6,7] para días de la semana
    created_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    received_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de configuración de dispositivos
CREATE TABLE IF NOT EXISTS device_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    config_key VARCHAR(100) NOT NULL,
    config_value JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(device_id, config_key)
);

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_events_device_id ON events(device_id);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_alerts_elderly_person_id ON alerts(elderly_person_id);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_alerts_is_resolved ON alerts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_reminders_elderly_person_id ON reminders(elderly_person_id);
CREATE INDEX IF NOT EXISTS idx_reminders_is_active ON reminders(is_active);

-- Datos de ejemplo para desarrollo
INSERT INTO users (email, password_hash, first_name, last_name, phone) VALUES
('lucia@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS8mti', 'Lucía', 'González', '+5491112345678')
ON CONFLICT (email) DO NOTHING;

INSERT INTO elderly_persons (user_id, first_name, last_name, age, address, emergency_contacts) VALUES
((SELECT id FROM users WHERE email = 'lucia@example.com'), 'Rosa', 'Martínez', 78, 'Av. Corrientes 1234, CABA', 
'[{"name": "Lucía González", "phone": "+5491112345678", "relationship": "hija"}, {"name": "Dr. Pérez", "phone": "+5491187654321", "relationship": "médico"}]')
ON CONFLICT DO NOTHING;

INSERT INTO devices (elderly_person_id, device_id, name, location, is_active) VALUES
((SELECT id FROM elderly_persons WHERE first_name = 'Rosa'), 'ESP32_001', 'Sensor Principal', 'Sala de estar', true)
ON CONFLICT (device_id) DO NOTHING;

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

DROP TRIGGER IF EXISTS ensure_jsonb_fields_trigger ON elderly_persons;
CREATE TRIGGER ensure_jsonb_fields_trigger
BEFORE INSERT OR UPDATE ON elderly_persons
FOR EACH ROW EXECUTE FUNCTION ensure_jsonb_fields();

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

DROP TRIGGER IF EXISTS ensure_event_value_jsonb_trigger ON events;
CREATE TRIGGER ensure_event_value_jsonb_trigger
    BEFORE INSERT OR UPDATE ON events
    FOR EACH ROW
    EXECUTE FUNCTION ensure_event_value_jsonb(); 