import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

# Cargar .env solo si existe (en Render se usan Variables de Entorno del Dashboard)
if os.path.exists(".env"):
    load_dotenv()

app = FastAPI(title="Taller Pro - Gestión de Emergencias")

# --- CONFIGURACIÓN DE CORS ---
# Obtenemos la URL del frontend desde el entorno para no dejar "*" en producción
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://taller-pro-client.onrender.com")
DEVELOPMENT_MODE = os.getenv("DEBUG", "False").lower() == "true"

origins = [
    # Frontend Web (Angular)
    "http://localhost:4200",
    "https://emergencia-vehicular-1.onrender.com",
    FRONTEND_URL,
    # Frontend Mobile (Ionic/Angular)
    "http://localhost:8100",
    # Flutter Mobile - Android Emulator
    "http://10.0.2.2:8000",
    # Flutter Mobile - iOS Simulator
    "http://localhost:8000",
    # Flutter Mobile - Dispositivo Físico (IP local) ⭐ TU LAPTOP
    "http://192.168.56.1:8000",
    "http://192.168.56.1:4200",
    # Otros rangos comunes en redes locales
    "http://192.168.1.0:8000",
    "http://10.0.0.0:8000",
    # Variables de entorno para testing dinámico
    os.getenv("LOCAL_IP_URL", ""),
]

# Filtrar URLs vacías
origins = [origin for origin in origins if origin.strip()]

# En DESARROLLO: permitir "*" para facilitar testing en red local
if DEVELOPMENT_MODE:
    print("[⚠️  DESARROLLO] CORS configurado con '*' - ¡NO usar en producción!")
    origins = ["*"]  # Permite todas las URLs en desarrollo

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS PÚBLICOS (Revividor) ---

@app.get("/api/v1/health")
def health_check():
    """Endpoint para el revividor de GitHub Actions. 
    No requiere auth y no genera registros en Bitácora."""
    return {
        "status": "online",
        "service": "Taller Pro API",
        "tenant_mode": "multi-tenant-enabled"
    }

# --- ROUTER PRINCIPAL ---
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API de Asistencia Vehicular funcionando"}