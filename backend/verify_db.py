#!/usr/bin/env python
import os
f = "emergencias.db"
if os.path.exists(f):
    size = os.path.getsize(f)
    print(f"[OK] Database: {f}")
    print(f"[OK] Size: {size:,} bytes ({size/1024:.1f} KB)")
else:
    print("[ERROR] Database file not found")
