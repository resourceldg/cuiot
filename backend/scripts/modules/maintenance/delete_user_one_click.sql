-- Función súper simple para eliminar un usuario de una sola vez
-- Aprovecha CASCADE DELETE para hacer todo automáticamente

CREATE OR REPLACE FUNCTION delete_user_one_click(user_email TEXT)
RETURNS TEXT AS $$
DECLARE
    user_record RECORD;
    deleted_count INTEGER;
BEGIN
    -- Buscar el usuario por email
    SELECT u.id, u.email, u.first_name, u.last_name INTO user_record
    FROM users u WHERE u.email = user_email;
    
    IF user_record.id IS NULL THEN
        RETURN 'ERROR: Usuario con email ' || user_email || ' no encontrado';
    END IF;
    
    -- Eliminar el usuario - CASCADE DELETE se encarga de todo automáticamente
    DELETE FROM users WHERE id = user_record.id;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    IF deleted_count > 0 THEN
        RETURN 'SUCCESS: Usuario ' || user_record.email || ' (' || user_record.first_name || ' ' || user_record.last_name || ') eliminado exitosamente con todas sus dependencias';
    ELSE
        RETURN 'ERROR: No se pudo eliminar el usuario ' || user_record.email;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERROR: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Función alternativa por ID
CREATE OR REPLACE FUNCTION delete_user_one_click_by_id(user_id UUID)
RETURNS TEXT AS $$
DECLARE
    user_record RECORD;
    deleted_count INTEGER;
BEGIN
    -- Buscar el usuario por ID
    SELECT u.id, u.email, u.first_name, u.last_name INTO user_record
    FROM users u WHERE u.id = user_id;
    
    IF user_record.id IS NULL THEN
        RETURN 'ERROR: Usuario con ID ' || user_id || ' no encontrado';
    END IF;
    
    -- Eliminar el usuario - CASCADE DELETE se encarga de todo automáticamente
    DELETE FROM users WHERE id = user_record.id;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    IF deleted_count > 0 THEN
        RETURN 'SUCCESS: Usuario ' || user_record.email || ' (' || user_record.first_name || ' ' || user_record.last_name || ') eliminado exitosamente con todas sus dependencias';
    ELSE
        RETURN 'ERROR: No se pudo eliminar el usuario ' || user_record.email;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERROR: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Función para listar usuarios disponibles
CREATE OR REPLACE FUNCTION list_users_for_deletion()
RETURNS TABLE(
    id UUID,
    email TEXT,
    full_name TEXT,
    roles TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email::TEXT,
        (u.first_name || ' ' || u.last_name)::TEXT as full_name,
        STRING_AGG(r.name, ', ')::TEXT as roles,
        u.created_at
    FROM users u
    LEFT JOIN user_roles ur ON u.id = ur.user_id AND ur.is_active = true
    LEFT JOIN roles r ON ur.role_id = r.id
    WHERE u.is_active = true
    GROUP BY u.id, u.email, u.first_name, u.last_name, u.created_at
    ORDER BY u.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Ejemplos de uso:
-- SELECT delete_user_one_click('usuario@ejemplo.com');
-- SELECT delete_user_one_click_by_id('uuid-del-usuario');
-- SELECT * FROM list_users_for_deletion();

-- Mostrar las funciones creadas
\df delete_user_one_click*
\df list_users_for_deletion 