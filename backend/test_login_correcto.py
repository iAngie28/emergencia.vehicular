#!/usr/bin/env python
"""Test login endpoint with correct credentials"""
import requests
import json
import time

print("[TEST] Intentando login al backend con credenciales correctas...\n")

# Usuarios de prueba del seeder
test_users = [
    {'email': 'admin1@taller.com', 'tipo': 'Admin'},
    {'email': 'tec_1_0@taller.com', 'tipo': 'Técnico'},
    {'email': 'cliente_0@correo.com', 'tipo': 'Cliente'},
]

data = {
    'client_id': 'movil'  # Cliente móvil
}

for user in test_users:
    email = user['email']
    tipo = user['tipo']
    
    data['username'] = email
    data['password'] = 'password123'
    
    print(f"[TEST] {tipo}: {email}")
    
    try:
        start = time.time()
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data=data,
            timeout=10,
            headers={'Accept': 'application/json'}
        )
        elapsed = time.time() - start
        
        print(f"       Status: {response.status_code} | Time: {elapsed:.2f}s", end="")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token', 'N/A')
            print(f" | ✅ Token: {token[:30]}...")
        else:
            err = response.json().get('detail', 'Unknown error')
            print(f" | ❌ {err}")
            
    except requests.Timeout:
        print(f"       ⏱️  TIMEOUT - Servidor tardó > 10s")
    except Exception as e:
        print(f"       ❌ {type(e).__name__}: {str(e)[:100]}")
    
    print()
