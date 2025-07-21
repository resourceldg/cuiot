import json
import urllib.request
import sys
import re

BASE_URL = "http://localhost:8000"
LOGIN_PATHS = ["/auth/login", "/api/v1/auth/login"]
USER_EMAIL = "admin@cuiot.com"
USER_PASS = "admin123"

if len(sys.argv) < 2:
    print("Uso: python3 debug_api_minimal.py <user_id|email>")
    sys.exit(1)

user_arg = sys.argv[1]

# 1. Obtener token
print("🔑 Obteniendo token de autenticación para admin@cuiot.com ...")
token = None
for path in LOGIN_PATHS:
    url = BASE_URL + path
    req = urllib.request.Request(
        url,
        data=json.dumps({"email": USER_EMAIL, "password": USER_PASS}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
            token = data.get("access_token") or data.get("token")
            if token:
                print(f"✅ Token obtenido usando {path}")
                break
    except Exception as e:
        print(f"  ❌ Login falló en {path}: {e}")

if not token:
    print("❌ No se pudo obtener token")
    exit(1)

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# 2. Si el argumento es email, buscar user_id
email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
if re.match(email_regex, user_arg):
    print(f"🔍 Buscando user_id para el email: {user_arg}")
    users_url = BASE_URL + "/api/v1/users"
    req = urllib.request.Request(users_url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            users = json.load(resp)
            user = next((u for u in users if u.get("email") == user_arg), None)
            if not user:
                print(f"❌ No se encontró usuario con email {user_arg}")
                sys.exit(1)
            user_id = user.get("id")
            print(f"✅ user_id encontrado: {user_id}")
    except Exception as e:
        print(f"❌ Error al buscar user_id: {e}")
        sys.exit(1)
else:
    user_id = user_arg

if user_arg == 'list':
    # Listar todos los usuarios
    print('🔍 Consultando lista de usuarios en /api/v1/users ...')
    req = urllib.request.Request(
        BASE_URL + '/api/v1/users',
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Error al consultar /api/v1/users: {e}")
    sys.exit(0)

# 3. Consultar suscripciones
url = f"{BASE_URL}/api/v1/packages/user/{user_id}/subscriptions"
print(f"🔍 Consultando: {url}")
req = urllib.request.Request(url, headers=headers, method="GET")
try:
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
        print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Error al consultar suscripciones: {e}")
    sys.exit(1) 