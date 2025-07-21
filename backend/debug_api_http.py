#!/usr/bin/env python3
"""
Script para consultar el endpoint de suscripciones de paquetes de usuario vía HTTP
Uso:
  python3 debug_api_http.py <user_id|email> [<token>]
Si no se pasa token, se obtiene automáticamente usando admin@cuiot.com / admin123
Si se pasa un email, el script busca el user_id automáticamente.
"""
import sys
import requests
import json
import re

if len(sys.argv) < 2:
    print("Uso: python3 debug_api_http.py <user_id|email> [<token>]")
    sys.exit(1)

user_arg = sys.argv[1]
token = sys.argv[2] if len(sys.argv) > 2 else None

BASE_URL = "http://localhost:8000"
headers = {"Accept": "application/json"}

# Función para obtener token probando varios paths
def get_token_auto():
    print("🔑 Obteniendo token de autenticación para admin@cuiot.com ...")
    login_paths = ["/auth/login", "/api/v1/auth/login"]
    auth_data = {"username": "admin@cuiot.com", "password": "admin123"}
    for path in login_paths:
        auth_url = BASE_URL + path
        print(f"  Probando login en: {auth_url}")
        try:
            resp = requests.post(auth_url, json=auth_data, headers={"Accept": "application/json"})
            if resp.status_code == 200:
                auth_json = resp.json()
                token = auth_json.get("access_token") or auth_json.get("token")
                if not token:
                    print(f"❌ No se encontró access_token en la respuesta de login en {path}: {auth_json}")
                    continue
                print(f"✅ Token obtenido usando {path}")
                return token
            else:
                print(f"  ❌ Login falló en {path}: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"  ❌ Error al probar {path}: {e}")
    print("❌ No se pudo autenticar admin en ninguno de los paths probados.")
    sys.exit(1)

# Si no hay token, obtenerlo usando las credenciales admin
if not token:
    token = get_token_auto()
    headers["Authorization"] = f"Bearer {token}"
else:
    headers["Authorization"] = f"Bearer {token}"

# Si el argumento parece un email, buscar el user_id
email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
if re.match(email_regex, user_arg):
    print(f"🔍 Buscando user_id para el email: {user_arg}")
    users_url = BASE_URL + "/users"
    try:
        resp = requests.get(users_url, headers=headers)
        if resp.status_code == 200:
            users = resp.json()
            user = next((u for u in users if u.get("email") == user_arg), None)
            if not user:
                print(f"❌ No se encontró usuario con email {user_arg}")
                sys.exit(1)
            user_id = user.get("id")
            print(f"✅ user_id encontrado: {user_id}")
        else:
            print(f"❌ Error al obtener usuarios: {resp.status_code} {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error al buscar user_id: {e}")
        sys.exit(1)
else:
    user_id = user_arg

ENDPOINT = f"/packages/user/{user_id}/subscriptions"
url = BASE_URL + ENDPOINT

print(f"🔍 Consultando: {url}")
try:
    resp = requests.get(url, headers=headers)
    print(f"HTTP {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(resp.text)
except Exception as e:
    print(f"❌ Error al consultar el endpoint: {e}")
    sys.exit(1) 