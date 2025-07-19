-- Script SQL para eliminar usuarios específicos problemáticos
-- Ejecutar con cuidado, esto eliminará permanentemente los datos

-- Lista de usuarios problemáticos identificados
DO $$
DECLARE
    user_record RECORD;
    current_user_id UUID;
    problematic_users UUID[] := ARRAY[
        '65800ff4-5328-4969-8615-19e99592d227'
    ];
BEGIN
    -- Iterar sobre cada usuario problemático
    FOREACH current_user_id IN ARRAY problematic_users
    LOOP
        -- Verificar si el usuario existe
        SELECT u.id, u.email, u.first_name, u.last_name INTO user_record
        FROM users u WHERE u.id = current_user_id;
        
        IF user_record.id IS NOT NULL THEN
            RAISE NOTICE 'Eliminando usuario problemático: % (%)', user_record.email, user_record.first_name || ' ' || user_record.last_name;
            
            -- Eliminar en orden de dependencias (de más específica a más general)
            
            -- 1. Eliminar billing_records relacionados con user_packages
            DELETE FROM billing_records 
            WHERE user_package_id IN (
                SELECT id FROM user_packages WHERE user_id = current_user_id
            );
            
            -- 2. Eliminar user_package_add_ons
            DELETE FROM user_package_add_ons 
            WHERE user_package_id IN (
                SELECT id FROM user_packages WHERE user_id = current_user_id
            );
            
            -- 3. Eliminar user_packages
            DELETE FROM user_packages WHERE user_id = current_user_id;
            
            -- 4. Eliminar service_subscriptions
            DELETE FROM service_subscriptions WHERE user_id = current_user_id;
            
            -- 5. Eliminar billing_records directos del usuario
            DELETE FROM billing_records WHERE user_id = current_user_id;
            
            -- 6. Eliminar location_tracking
            DELETE FROM location_tracking WHERE user_id = current_user_id;
            
            -- 7. Eliminar geofences
            DELETE FROM geofences WHERE user_id = current_user_id;
            
            -- 8. Eliminar debug_events
            DELETE FROM debug_events WHERE user_id = current_user_id;
            
            -- 9. Eliminar caregiver_institutions
            DELETE FROM caregiver_institutions WHERE caregiver_id = current_user_id;
            
            -- 10. Eliminar caregiver_scores
            DELETE FROM caregiver_scores WHERE caregiver_id = current_user_id;
            
            -- 11. Eliminar caregiver_reviews donde es caregiver
            DELETE FROM caregiver_reviews WHERE caregiver_id = current_user_id;
            
            -- 12. Eliminar caregiver_reviews donde es reviewer
            DELETE FROM caregiver_reviews WHERE reviewer_id = current_user_id;
            
            -- 13. Eliminar institution_reviews donde es reviewer
            DELETE FROM institution_reviews WHERE reviewer_id = current_user_id;
            
            -- 14. Eliminar vital_signs relacionados con shift_observations
            DELETE FROM vital_signs 
            WHERE shift_observation_id IN (
                SELECT id FROM shift_observations WHERE caregiver_id = current_user_id
            );
            
            -- 15. Eliminar shift_observations donde es caregiver
            DELETE FROM shift_observations WHERE caregiver_id = current_user_id;
            
            -- 16. Eliminar vital_signs relacionados con shift_observations verified_by
            DELETE FROM vital_signs 
            WHERE shift_observation_id IN (
                SELECT id FROM shift_observations WHERE verified_by = current_user_id
            );
            
            -- 17. Eliminar shift_observations donde es verified_by
            DELETE FROM shift_observations WHERE verified_by = current_user_id;
            
            -- 18. Eliminar caregiver_assignments donde es caregiver
            DELETE FROM caregiver_assignments WHERE caregiver_id = current_user_id;
            
            -- 19. Eliminar cared_person_institutions donde es registered_by
            DELETE FROM cared_person_institutions WHERE registered_by = current_user_id;
            
            -- 20. Eliminar devices del usuario
            DELETE FROM devices WHERE user_id = current_user_id;
            
            -- 21. Eliminar events del usuario
            DELETE FROM events WHERE user_id = current_user_id;
            
            -- 22. Eliminar alerts del usuario
            DELETE FROM alerts WHERE user_id = current_user_id;
            
            -- 23. Eliminar reminders del usuario
            DELETE FROM reminders WHERE user_id = current_user_id;
            
            -- 24. Eliminar diagnoses relacionados con cared_persons
            DELETE FROM diagnoses 
            WHERE cared_person_id IN (
                SELECT id FROM cared_persons WHERE user_id = current_user_id
            );
            
            -- 25. Eliminar vital_signs relacionados con shift_observations de cared_persons
            DELETE FROM vital_signs 
            WHERE shift_observation_id IN (
                SELECT id FROM shift_observations 
                WHERE cared_person_id IN (
                    SELECT id FROM cared_persons WHERE user_id = current_user_id
                )
            );
            
            -- 26. Eliminar shift_observations relacionados con cared_persons
            DELETE FROM shift_observations 
            WHERE cared_person_id IN (
                SELECT id FROM cared_persons WHERE user_id = current_user_id
            );
            
            -- 27.1. Eliminar caregiver_assignments donde cared_person_id corresponde a cared_persons del usuario
            DELETE FROM caregiver_assignments WHERE cared_person_id IN (
                SELECT id FROM cared_persons WHERE user_id = current_user_id
            );

            -- 27.2. Eliminar location_tracking donde cared_person_id corresponde a cared_persons del usuario
            DELETE FROM location_tracking WHERE cared_person_id IN (
                SELECT id FROM cared_persons WHERE user_id = current_user_id
            );

            -- 28. Eliminar cared_persons del usuario
            DELETE FROM cared_persons WHERE user_id = current_user_id;
            
            -- 29. Eliminar medication_logs donde confirmed_by es el usuario
            DELETE FROM medication_logs WHERE confirmed_by = current_user_id;

            -- 30. Eliminar user_roles
            DELETE FROM user_roles WHERE user_id = current_user_id;
            
            -- 31. Finalmente eliminar el usuario
            DELETE FROM users WHERE id = current_user_id;
            
            RAISE NOTICE 'Usuario problemático % eliminado exitosamente', user_record.email;
        ELSE
            RAISE NOTICE 'Usuario con ID % no encontrado', current_user_id;
        END IF;
        
    END LOOP;
    
    RAISE NOTICE 'Proceso de eliminación de usuarios problemáticos completado';
END $$;

-- Verificar que los usuarios problemáticos fueron eliminados
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name
FROM users u
WHERE u.id IN (
    '65800ff4-5328-4969-8615-19e99592d227'
); 