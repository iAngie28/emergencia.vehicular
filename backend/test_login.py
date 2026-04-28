#!/usr/bin/env python
"""Test login endpoint response time"""
import requests
import json
import time

print("[TEST] Intentando login al backend...")
print("[INFO] URL: http://localhost:8000/api/v1/auth/login\n")

# Datos de prueba - usuario de prueba del seeder
data = {
    'username': 'cliente1@test.com',  # Email de cliente de prueba
    'password': 'password123',         # Contraseña de prueba
    'client_id': 'movil'              # Cliente móvil
}

try:
    start = time.time()
    response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        data=data,
        timeout=10,
        headers={'Accept': 'application/json'}
    )
    elapsed = time.time() - start
    
    print(f"[INFO] Status Code: {response.status_code}")
    print(f"[INFO] Response Time: {elapsed:.2f}s")
    print(f"[INFO] Response Size: {len(response.text)} bytes\n")
    
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] Login exitoso!")
        token = result.get('access_token', 'N/A')
        print(f"[TOKEN] {token[:50]}...")
        print(f"[TYPE] {result.get('token_type', 'N/A')}")
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(f"[ERROR] Response: {response.text[:500]}")
        
except requests.Timeout:
    print("[ERROR] ⏱️  TIMEOUT - El servidor tarda MÁS DE 10 segundos en responder!")
    print("[ERROR] Esto explica por qué la app móvil tarda tanto en login")
except requests.ConnectionError as e:
    print(f"[ERROR] 🔌 Connection Error: {str(e)[:200]}")
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)[:200]}")
