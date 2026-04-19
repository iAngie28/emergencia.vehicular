import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base # Importamos el que tiene todos los modelos
from app.api.v1.api import api_router

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(title="SaaS Asistencia Vehicular - IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Frontend Angular (Taller)
        "http://localhost:5000",  # Frontend para pruebas locales
        "http://localhost:8100",  # Ionic (alternativa para mobile)
        "*"  # TEMPORAL: Permite conexiones desde cualquier IP del teléfono en desarrollo
             # IMPORTANTE: En producción, especificar la IP exacta del teléfono
             # Ej: allow_origins=["http://192.168.0.XX:PUERTO", "http://10.0.0.XX:PUERTO"]
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos el router maestro
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API de Asistencia Vehicular funcionando"}