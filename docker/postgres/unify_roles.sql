-- Unificar y limpiar roles duplicados

-- 1. Asegúrate de que los roles destino existen
INSERT INTO roles (id, name, description, permissions, is_system, created_at, updated_at, is_active)
SELECT gen_random_uuid(), 'institution_admin', 'Administrador de institución', '{}', false, NOW(), NOW(), true
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'institution_admin');

INSERT INTO roles (id, name, description, permissions, is_system, created_at, updated_at, is_active)
SELECT gen_random_uuid(), 'cared_person_self', 'Persona en autocuidado', '{}', false, NOW(), NOW(), true
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'cared_person_self');

-- 2. Actualiza los user_roles
UPDATE user_roles SET role_id = (SELECT id FROM roles WHERE name = 'institution_admin')
WHERE role_id = (SELECT id FROM roles WHERE name = 'admin_institution');

UPDATE user_roles SET role_id = (SELECT id FROM roles WHERE name = 'cared_person_self')
WHERE role_id = (SELECT id FROM roles WHERE name = 'self_cared_person');

-- 3. Elimina los roles duplicados
DELETE FROM roles WHERE name = 'admin_institution';
DELETE FROM roles WHERE name = 'self_cared_person'; 