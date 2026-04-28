#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test PostgreSQL connection"""
import psycopg2
from psycopg2 import OperationalError

try:
    print("[INFO] Conectando a PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="password",
        client_encoding="UTF8"
    )
    print("[OK] Conexion exitosa!")
    print(f"[OK] Database version: {conn.get_parameter_status('server_version')}")
    conn.close()
except OperationalError as e:
    print(f"[ERROR OperationalError] {e}")
except Exception as e:
    print(f"[ERROR {type(e).__name__}] {e}")
