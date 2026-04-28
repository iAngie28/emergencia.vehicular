#!/usr/bin/env python
"""Check SQLite indexes"""
import sqlite3

conn = sqlite3.connect('emergencias.db')
cursor = conn.cursor()

# Verificar índices en tabla usuario
cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='usuario'")
indices = cursor.fetchall()

print("[INFO] Índices en tabla usuario:")
for idx in indices:
    print(f"  - {idx[0]}")

if not any('correo' in str(idx) for idx in indices):
    print("\n[WARN] ⚠️ No hay índice en el campo correo!")
    print("[INFO] Esto explica el delay en búsqueda de usuarios")
else:
    print("\n[OK] ✅ Índice correo existe")
    print("[INFO] La búsqueda debería ser rápida (50-100ms)")

conn.close()
