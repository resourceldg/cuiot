-- Migración completa del esquema de base de datos
-- Ejecutar una sola vez después de crear la base de datos
-- Incluye validaciones de integridad y prevención de errores

-- =====================================================
-- LIMPIEZA Y VALIDACIÓN PREVIA
-- =====================================================

-- Eliminar alertas con tipos inválidos (si existen)
DELETE FROM alerts WHERE alert_type NOT IN (
    'no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate', 'blood_pressure'
);

-- =====================================================
-- MIGRACIONES DE ESQUEMA
-- =====================================================

-- Tabla users
ALTER TABLE users ADD COLUMN IF NOT EXISTS user_type VARCHAR(20) DEFAULT 'family';

-- Tabla elderly_persons
ALTER TABLE elderly_persons ADD COLUMN IF NOT EXISTS medical_conditions TEXT DEFAULT '[]';
ALTER TABLE elderly_persons ADD COLUMN IF NOT EXISTS medications TEXT DEFAULT '[]';
ALTER TABLE elderly_persons ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;

-- Convertir campos JSON si es necesario
DO $$
BEGIN
    -- Convertir medical_conditions a JSONB si no lo es ya
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'elderly_persons' 
        AND column_name = 'medical_conditions' 
        AND data_type = 'text'
    ) THEN
        ALTER TABLE elderly_persons ALTER COLUMN medical_conditions TYPE JSONB USING medical_conditions::jsonb;
        ALTER TABLE elderly_persons ALTER COLUMN medical_conditions SET DEFAULT '[]'::jsonb;
    END IF;
    
    -- Convertir medications a JSONB si no lo es ya
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'elderly_persons' 
        AND column_name = 'medications' 
        AND data_type = 'text'
    ) THEN
        ALTER TABLE elderly_persons ALTER COLUMN medications TYPE JSONB USING medications::jsonb;
        ALTER TABLE elderly_persons ALTER COLUMN medications SET DEFAULT '[]'::jsonb;
    END IF;
END $$;

-- Tabla devices
ALTER TABLE devices ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'ready';
ALTER TABLE devices ADD COLUMN IF NOT EXISTS type VARCHAR(50) DEFAULT 'unknown';

-- Tabla events
ALTER TABLE events ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id);
ALTER TABLE events ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id);

-- Tabla alerts
ALTER TABLE alerts ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id);
ALTER TABLE alerts ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id);

-- Tabla reminders
ALTER TABLE reminders ADD COLUMN IF NOT EXISTS created_by_id UUID REFERENCES users(id);
ALTER TABLE reminders ADD COLUMN IF NOT EXISTS received_by_id UUID REFERENCES users(id);

-- =====================================================
-- CONSTRAINTS Y VALIDACIONES
-- =====================================================

-- Constraint para alert_type válido
DO $$
BEGIN
    -- Crear constraint solo si no existe
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'valid_alert_types'
    ) THEN
        ALTER TABLE alerts ADD CONSTRAINT valid_alert_types 
        CHECK (alert_type IN ('no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate', 'blood_pressure'));
    END IF;
END $$;

-- Constraint para device status válido
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'valid_device_status'
    ) THEN
        ALTER TABLE devices ADD CONSTRAINT valid_device_status 
        CHECK (status IN ('ready', 'offline', 'error', 'off'));
    END IF;
END $$;

-- Constraint para device type válido
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'valid_device_type'
    ) THEN
        ALTER TABLE devices ADD CONSTRAINT valid_device_type 
        CHECK (type IN ('smart_watch', 'panic_button', 'motion_sensor', 'door_sensor', 'bed_sensor', 'temperature_sensor'));
    END IF;
END $$;

-- =====================================================
-- ÍNDICES PARA RENDIMIENTO
-- =====================================================

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_elderly_persons_is_deleted ON elderly_persons(is_deleted);
CREATE INDEX IF NOT EXISTS idx_elderly_persons_is_active ON elderly_persons(is_active);
CREATE INDEX IF NOT EXISTS idx_devices_status ON devices(status);
CREATE INDEX IF NOT EXISTS idx_devices_type ON devices(type);
CREATE INDEX IF NOT EXISTS idx_alerts_alert_type ON alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_is_resolved ON alerts(is_resolved);

-- =====================================================
-- FUNCIONES DE VALIDACIÓN
-- =====================================================

-- Función para validar integridad de datos
CREATE OR REPLACE FUNCTION validate_data_integrity()
RETURNS TABLE(
    table_name TEXT,
    record_count BIGINT,
    status TEXT
) AS $$
BEGIN
    -- Validar usuarios
    RETURN QUERY SELECT 
        'users'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END::TEXT
    FROM users;
    
    -- Validar personas bajo cuidado
    RETURN QUERY SELECT 
        'elderly_persons'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END::TEXT
    FROM elderly_persons WHERE is_deleted = FALSE;
    
    -- Validar dispositivos
    RETURN QUERY SELECT 
        'devices'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END::TEXT
    FROM devices;
    
    -- Validar alertas con tipos válidos
    RETURN QUERY SELECT 
        'alerts_valid'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) = (SELECT COUNT(*) FROM alerts) THEN 'OK' ELSE 'INVALID_TYPES' END::TEXT
    FROM alerts WHERE alert_type IN ('no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate', 'blood_pressure');
    
    -- Validar eventos
    RETURN QUERY SELECT 
        'events'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END::TEXT
    FROM events;
    
    -- Validar recordatorios
    RETURN QUERY SELECT 
        'reminders'::TEXT,
        COUNT(*)::BIGINT,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END::TEXT
    FROM reminders;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- TRIGGERS DE VALIDACIÓN
-- =====================================================

-- Trigger para validar alert_type antes de insertar/actualizar
CREATE OR REPLACE FUNCTION validate_alert_type()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.alert_type NOT IN ('no_movement', 'sos', 'temperature', 'medication', 'fall', 'heart_rate', 'blood_pressure') THEN
        RAISE EXCEPTION 'Invalid alert_type: %. Valid types are: no_movement, sos, temperature, medication, fall, heart_rate, blood_pressure', NEW.alert_type;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger solo si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger 
        WHERE tgname = 'validate_alert_type_trigger'
    ) THEN
        CREATE TRIGGER validate_alert_type_trigger
        BEFORE INSERT OR UPDATE ON alerts
        FOR EACH ROW
        EXECUTE FUNCTION validate_alert_type();
    END IF;
END $$;

-- =====================================================
-- RESULTADO FINAL
-- =====================================================

-- Ejecutar validación final
SELECT 'MIGRATION_COMPLETE' as status, 
       'All schema migrations and validations applied successfully' as message;

-- Mostrar resumen de validación
SELECT * FROM validate_data_integrity(); 