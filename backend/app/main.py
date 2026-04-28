from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base # Importamos el que tiene todos los modelos
from app.api.v1.api import api_router

app = FastAPI(title="SaaS Asistencia Vehicular - IA")

app = FastAPI(title="SaaS Emergencias Vehiculares")

# --- CONFIGURACIÓN DE CORS ---
# Esta es la lista de "invitados" permitidos
origins = [
    "http://localhost:4200", # Tu frontend de Angular
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Permite Angular
    allow_credentials=True,
    allow_methods=["*"],              # Permite POST, GET, etc.
    allow_headers=["*"],              # Permite todos los headers
)
# -----------------------------

# Incluimos el router maestro
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API de Asistencia Vehicular funcionando"}