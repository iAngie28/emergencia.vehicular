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

origins = [
    "http://localhost:4200",
    "http://localhost:8100",
    FRONTEND_URL, # Dominio de producción
]

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