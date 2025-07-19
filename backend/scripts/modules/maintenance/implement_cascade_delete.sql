-- Script para implementar CASCADE DELETE en relaciones seguras
-- Mejora la mantenibilidad de la base de datos

-- 1. USER_ROLES - Cuando se elimina un usuario, eliminar sus roles
-- Esta es segura porque user_roles es una tabla de relación
ALTER TABLE user_roles 
DROP CONSTRAINT IF EXISTS user_roles_user_id_fkey;

ALTER TABLE user_roles 
ADD CONSTRAINT user_roles_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 2. USER_PACKAGES - Cuando se elimina un usuario, eliminar sus paquetes
-- Esta es segura porque user_packages pertenece al usuario
ALTER TABLE user_packages 
DROP CONSTRAINT IF EXISTS user_packages_user_id_fkey;

ALTER TABLE user_packages 
ADD CONSTRAINT user_packages_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 3. SERVICE_SUBSCRIPTIONS - Cuando se elimina un usuario, eliminar sus suscripciones
ALTER TABLE service_subscriptions 
DROP CONSTRAINT IF EXISTS service_subscriptions_user_id_fkey;

ALTER TABLE service_subscriptions 
ADD CONSTRAINT service_subscriptions_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 4. BILLING_RECORDS - Cuando se elimina un usuario, eliminar sus registros de facturación
ALTER TABLE billing_records 
DROP CONSTRAINT IF EXISTS billing_records_user_id_fkey;

ALTER TABLE billing_records 
ADD CONSTRAINT billing_records_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 5. LOCATION_TRACKING - Cuando se elimina un usuario, eliminar su tracking
ALTER TABLE location_tracking 
DROP CONSTRAINT IF EXISTS location_tracking_user_id_fkey;

ALTER TABLE location_tracking 
ADD CONSTRAINT location_tracking_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 6. GEOFENCES - Cuando se elimina un usuario, eliminar sus geofences
ALTER TABLE geofences 
DROP CONSTRAINT IF EXISTS geofences_user_id_fkey;

ALTER TABLE geofences 
ADD CONSTRAINT geofences_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 7. DEBUG_EVENTS - Cuando se elimina un usuario, eliminar sus eventos de debug
ALTER TABLE debug_events 
DROP CONSTRAINT IF EXISTS debug_events_user_id_fkey;

ALTER TABLE debug_events 
ADD CONSTRAINT debug_events_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 8. CAREGIVER_INSTITUTIONS - Cuando se elimina un usuario, eliminar sus relaciones institucionales
ALTER TABLE caregiver_institutions 
DROP CONSTRAINT IF EXISTS caregiver_institutions_caregiver_id_fkey;

ALTER TABLE caregiver_institutions 
ADD CONSTRAINT caregiver_institutions_caregiver_id_fkey 
FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE CASCADE;

-- 9. CAREGIVER_SCORES - Cuando se elimina un usuario, eliminar sus scores
ALTER TABLE caregiver_scores 
DROP CONSTRAINT IF EXISTS caregiver_scores_caregiver_id_fkey;

ALTER TABLE caregiver_scores 
ADD CONSTRAINT caregiver_scores_caregiver_id_fkey 
FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE CASCADE;

-- 10. CAREGIVER_REVIEWS - Cuando se elimina un cuidador, eliminar sus reviews
ALTER TABLE caregiver_reviews 
DROP CONSTRAINT IF EXISTS caregiver_reviews_caregiver_id_fkey;

ALTER TABLE caregiver_reviews 
ADD CONSTRAINT caregiver_reviews_caregiver_id_fkey 
FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE CASCADE;

-- 11. CAREGIVER_REVIEWS - Cuando se elimina un reviewer, eliminar sus reviews
ALTER TABLE caregiver_reviews 
DROP CONSTRAINT IF EXISTS caregiver_reviews_reviewer_id_fkey;

ALTER TABLE caregiver_reviews 
ADD CONSTRAINT caregiver_reviews_reviewer_id_fkey 
FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE;

-- 12. INSTITUTION_REVIEWS - Cuando se elimina un reviewer, eliminar sus reviews
ALTER TABLE institution_reviews 
DROP CONSTRAINT IF EXISTS institution_reviews_reviewer_id_fkey;

ALTER TABLE institution_reviews 
ADD CONSTRAINT institution_reviews_reviewer_id_fkey 
FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE;

-- 13. DEVICES - Cuando se elimina un usuario, eliminar sus dispositivos
ALTER TABLE devices 
DROP CONSTRAINT IF EXISTS devices_user_id_fkey;

ALTER TABLE devices 
ADD CONSTRAINT devices_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 14. EVENTS - Cuando se elimina un usuario, eliminar sus eventos
ALTER TABLE events 
DROP CONSTRAINT IF EXISTS events_user_id_fkey;

ALTER TABLE events 
ADD CONSTRAINT events_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 15. ALERTS - Cuando se elimina un usuario, eliminar sus alertas
ALTER TABLE alerts 
DROP CONSTRAINT IF EXISTS alerts_user_id_fkey;

ALTER TABLE alerts 
ADD CONSTRAINT alerts_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 16. REMINDERS - Cuando se elimina un usuario, eliminar sus recordatorios
ALTER TABLE reminders 
DROP CONSTRAINT IF EXISTS reminders_user_id_fkey;

ALTER TABLE reminders 
ADD CONSTRAINT reminders_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 17. CARED_PERSONS - Cuando se elimina un usuario, eliminar sus personas cuidadas
ALTER TABLE cared_persons 
DROP CONSTRAINT IF EXISTS cared_persons_user_id_fkey;

ALTER TABLE cared_persons 
ADD CONSTRAINT cared_persons_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 18. MEDICATION_LOGS - Cuando se elimina un usuario que confirmó, eliminar sus logs
ALTER TABLE medication_logs 
DROP CONSTRAINT IF EXISTS medication_logs_confirmed_by_fkey;

ALTER TABLE medication_logs 
ADD CONSTRAINT medication_logs_confirmed_by_fkey 
FOREIGN KEY (confirmed_by) REFERENCES users(id) ON DELETE CASCADE;

-- 19. CARED_PERSON_INSTITUTIONS - Cuando se elimina un usuario que registró, eliminar sus registros
ALTER TABLE cared_person_institutions 
DROP CONSTRAINT IF EXISTS cared_person_institutions_registered_by_fkey;

ALTER TABLE cared_person_institutions 
ADD CONSTRAINT cared_person_institutions_registered_by_fkey 
FOREIGN KEY (registered_by) REFERENCES users(id) ON DELETE CASCADE;

-- 20. SHIFT_OBSERVATIONS - Cuando se elimina un cuidador, eliminar sus observaciones
ALTER TABLE shift_observations 
DROP CONSTRAINT IF EXISTS shift_observations_caregiver_id_fkey;

ALTER TABLE shift_observations 
ADD CONSTRAINT shift_observations_caregiver_id_fkey 
FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE CASCADE;

-- 21. SHIFT_OBSERVATIONS - Cuando se elimina un verificador, eliminar sus verificaciones
ALTER TABLE shift_observations 
DROP CONSTRAINT IF EXISTS shift_observations_verified_by_fkey;

ALTER TABLE shift_observations 
ADD CONSTRAINT shift_observations_verified_by_fkey 
FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE CASCADE;

-- 22. CAREGIVER_ASSIGNMENTS - Cuando se elimina un cuidador, eliminar sus asignaciones
ALTER TABLE caregiver_assignments 
DROP CONSTRAINT IF EXISTS caregiver_assignments_caregiver_id_fkey;

ALTER TABLE caregiver_assignments 
ADD CONSTRAINT caregiver_assignments_caregiver_id_fkey 
FOREIGN KEY (caregiver_id) REFERENCES users(id) ON DELETE CASCADE;

-- 23. USER_ROLES - Cuando se elimina quien asignó el rol, mantener el rol pero limpiar assigned_by
-- Esta es una relación opcional, así que la dejamos como SET NULL
ALTER TABLE user_roles 
DROP CONSTRAINT IF EXISTS user_roles_assigned_by_fkey;

ALTER TABLE user_roles 
ADD CONSTRAINT user_roles_assigned_by_fkey 
FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL;

-- 24. USER_PACKAGES - Cuando se elimina el representante legal, limpiar la referencia
ALTER TABLE user_packages 
DROP CONSTRAINT IF EXISTS user_packages_legal_representative_id_fkey;

ALTER TABLE user_packages 
ADD CONSTRAINT user_packages_legal_representative_id_fkey 
FOREIGN KEY (legal_representative_id) REFERENCES users(id) ON DELETE SET NULL;

-- Verificar que las restricciones se aplicaron correctamente
SELECT 
    tc.table_name, 
    tc.constraint_name, 
    tc.constraint_type,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.delete_rule
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
JOIN information_schema.referential_constraints AS rc
    ON tc.constraint_name = rc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND ccu.table_name = 'users'
    AND rc.delete_rule IN ('CASCADE', 'SET NULL')
ORDER BY tc.table_name, kcu.column_name; 