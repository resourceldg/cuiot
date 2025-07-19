-- Script de prueba para demostrar las nuevas funciones de eliminación
-- NO ejecutar en producción - solo para demostración

-- Crear un usuario de prueba
INSERT INTO users (id, email, first_name, last_name, password_hash, is_freelance, is_verified, is_active, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'test.user.cascade@cuiot.com',
    'Test',
    'User',
    'pbkdf2:sha256:dummyhash',
    false,
    false,
    true,
    NOW(),
    NOW()
) RETURNING id, email;

-- Asignar un rol al usuario de prueba
INSERT INTO user_roles (user_id, role_id, assigned_at, is_active, created_at, updated_at)
SELECT 
    u.id,
    r.id,
    NOW(),
    true,
    NOW(),
    NOW()
FROM users u, roles r
WHERE u.email = 'test.user.cascade@cuiot.com'
AND r.name = 'family_member';

-- Verificar que el usuario fue creado
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name,
    COUNT(ur.id) as roles_count
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
WHERE u.email = 'test.user.cascade@cuiot.com'
GROUP BY u.id, u.email, u.first_name, u.last_name;

-- Ahora probar la función de eliminación
SELECT delete_user_complete(
    (SELECT id FROM users WHERE email = 'test.user.cascade@cuiot.com')
);

-- Verificar que el usuario fue eliminado
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name
FROM users u
WHERE u.email = 'test.user.cascade@cuiot.com';

-- Verificar que los roles también fueron eliminados (CASCADE DELETE)
SELECT 
    ur.id,
    ur.user_id,
    ur.role_id
FROM user_roles ur
WHERE ur.user_id = (SELECT id FROM users WHERE email = 'test.user.cascade@cuiot.com');

-- Mostrar estadísticas de las funciones
SELECT 
    proname as function_name,
    prosrc as source_code_length
FROM pg_proc 
WHERE proname IN ('delete_user_complete', 'delete_multiple_users')
ORDER BY proname; 