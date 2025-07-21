#!/usr/bin/env python3
"""
Script para consultar el endpoint de suscripciones de paquetes de usuario vía HTTP
Uso:
  python3 debug_api_http.py <user_id> [<token>]
Si no se pasa token, se obtiene automáticamente usando admin@cuiot.com / admin123
"""
import sys
import requests
import json

if len(sys.argv) < 2:
    print("Uso: python3 debug_api_http.py <user_id> [<token>]")
    sys.exit(1)

user_id = sys.argv[1]
token = sys.argv[2] if len(sys.argv) > 2 else None

BASE_URL = "http://localhost:8000"
ENDPOINT = f"/packages/user/{user_id}/subscriptions"
url = BASE_URL + ENDPOINT

headers = {"Accept": "application/json"}

# Si no hay token, obtenerlo usando las credenciales admin
if not token:
    print("🔑 Obteniendo token de autenticación para admin@cuiot.com ...")
    auth_url = BASE_URL + "/auth/login"
    auth_data = {"username": "admin@cuiot.com", "password": "admin123"}
    try:
        resp = requests.post(auth_url, json=auth_data, headers={"Accept": "application/json"})
        if resp.status_code == 200:
            auth_json = resp.json()
            token = auth_json.get("access_token") or auth_json.get("token")
            if not token:
                print("❌ No se encontró access_token en la respuesta de login:", auth_json)
                sys.exit(1)
            print("✅ Token obtenido")
            headers["Authorization"] = f"Bearer {token}"
        else:
            print(f"❌ Error al autenticar admin: {resp.status_code} {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error al obtener token: {e}")
        sys.exit(1)
else:
    headers["Authorization"] = f"Bearer {token}"

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