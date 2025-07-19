-- Script simplificado para eliminar usuarios con CASCADE DELETE
-- Ahora mucho más simple gracias a las restricciones implementadas

-- Función para eliminar un usuario y todas sus dependencias automáticamente
CREATE OR REPLACE FUNCTION delete_user_complete(user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    user_record RECORD;
    deleted_count INTEGER;
BEGIN
    -- Verificar si el usuario existe
    SELECT u.id, u.email, u.first_name, u.last_name INTO user_record
    FROM users u WHERE u.id = user_id;
    
    IF user_record.id IS NULL THEN
        RAISE NOTICE 'Usuario con ID % no encontrado', user_id;
        RETURN FALSE;
    END IF;
    
    RAISE NOTICE 'Eliminando usuario: % (%)', user_record.email, user_record.first_name || ' ' || user_record.last_name;
    
    -- Eliminar registros que NO tienen CASCADE DELETE
    -- Estos necesitan eliminación manual porque tienen dependencias complejas
    
    -- 1. Eliminar vital_signs relacionados con shift_observations de cared_persons del usuario
    DELETE FROM vital_signs 
    WHERE shift_observation_id IN (
        SELECT id FROM shift_observations 
        WHERE cared_person_id IN (
            SELECT id FROM cared_persons WHERE user_id = user_id
        )
    );
    
    -- 2. Eliminar shift_observations relacionados con cared_persons del usuario
    DELETE FROM shift_observations 
    WHERE cared_person_id IN (
        SELECT id FROM cared_persons WHERE user_id = user_id
    );
    
    -- 3. Eliminar caregiver_assignments donde cared_person_id corresponde a cared_persons del usuario
    DELETE FROM caregiver_assignments WHERE cared_person_id IN (
        SELECT id FROM cared_persons WHERE user_id = user_id
    );
    
    -- 4. Eliminar location_tracking donde cared_person_id corresponde a cared_persons del usuario
    DELETE FROM location_tracking WHERE cared_person_id IN (
        SELECT id FROM cared_persons WHERE user_id = user_id
    );
    
    -- 5. Eliminar diagnoses relacionados con cared_persons del usuario
    DELETE FROM diagnoses 
    WHERE cared_person_id IN (
        SELECT id FROM cared_persons WHERE user_id = user_id
    );
    
    -- 6. Eliminar billing_records relacionados con user_packages del usuario
    DELETE FROM billing_records 
    WHERE user_package_id IN (
        SELECT id FROM user_packages WHERE user_id = user_id
    );
    
    -- 7. Eliminar user_package_add_ons del usuario
    DELETE FROM user_package_add_ons 
    WHERE user_package_id IN (
        SELECT id FROM user_packages WHERE user_id = user_id
    );
    
    -- 8. Eliminar location_tracking donde cared_person_id corresponde a cared_persons del usuario
    DELETE FROM location_tracking WHERE cared_person_id IN (
        SELECT id FROM cared_persons WHERE user_id = user_id
    );
    
    -- 9. Eliminar vital_signs relacionados con shift_observations verified_by
    DELETE FROM vital_signs 
    WHERE shift_observation_id IN (
        SELECT id FROM shift_observations WHERE verified_by = user_id
    );
    
    -- 10. Eliminar shift_observations donde es verified_by
    DELETE FROM shift_observations WHERE verified_by = user_id;
    
    -- 11. Eliminar vital_signs relacionados con shift_observations caregiver_id
    DELETE FROM vital_signs 
    WHERE shift_observation_id IN (
        SELECT id FROM shift_observations WHERE caregiver_id = user_id
    );
    
    -- 12. Eliminar shift_observations donde es caregiver_id
    DELETE FROM shift_observations WHERE caregiver_id = user_id;
    
    -- Ahora eliminar el usuario - esto activará CASCADE DELETE automáticamente
    DELETE FROM users WHERE id = user_id;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    IF deleted_count > 0 THEN
        RAISE NOTICE 'Usuario % eliminado exitosamente con todas sus dependencias', user_record.email;
        RETURN TRUE;
    ELSE
        RAISE NOTICE 'No se pudo eliminar el usuario %', user_record.email;
        RETURN FALSE;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error al eliminar usuario %: %', user_record.email, SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso:
-- SELECT delete_user_complete('user-id-aqui');

-- Función para eliminar múltiples usuarios
CREATE OR REPLACE FUNCTION delete_multiple_users(user_ids UUID[])
RETURNS TABLE(user_id UUID, email TEXT, success BOOLEAN, message TEXT) AS $$
DECLARE
    current_user_id UUID;
    user_record RECORD;
    success BOOLEAN;
    message TEXT;
BEGIN
    FOREACH current_user_id IN ARRAY user_ids
    LOOP
        -- Obtener información del usuario
        SELECT u.id, u.email INTO user_record
        FROM users u WHERE u.id = current_user_id;
        
        IF user_record.id IS NULL THEN
            user_id := current_user_id;
            email := 'Usuario no encontrado';
            success := FALSE;
            message := 'Usuario no existe en la base de datos';
        ELSE
            -- Intentar eliminar el usuario
            SELECT delete_user_complete(current_user_id) INTO success;
            
            user_id := current_user_id;
            email := user_record.email;
            
            IF success THEN
                message := 'Usuario eliminado exitosamente';
            ELSE
                message := 'Error al eliminar usuario';
            END IF;
        END IF;
        
        RETURN NEXT;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso para múltiples usuarios:
-- SELECT * FROM delete_multiple_users(ARRAY['user-id-1', 'user-id-2', 'user-id-3']);

-- Mostrar las funciones creadas
\df delete_user_complete
\df delete_multiple_users 