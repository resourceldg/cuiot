#!/usr/bin/env python3
"""
Script para probar la API de usuarios
"""

import requests
import json

def test_users_api():
    """Probar la API de usuarios"""
    try:
        print("🧪 Probando API de usuarios...")
        
        # Probar endpoint de usuarios
        response = requests.get("http://localhost:8000/api/v1/users")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Usuarios encontrados: {len(data)}")
            
            # Mostrar primeros 5 usuarios
            for i, user in enumerate(data[:5]):
                print(f"   {i+1}. {user.get('email', 'N/A')} - {user.get('first_name', 'N/A')} {user.get('last_name', 'N/A')}")
            
            if len(data) > 5:
                print(f"   ... y {len(data) - 5} usuarios más")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")

if __name__ == "__main__":
    test_users_api() 