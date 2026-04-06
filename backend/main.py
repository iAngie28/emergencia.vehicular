from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base # Importamos el que tiene todos los modelos
from app.api.v1.api import api_router

app = FastAPI(title="SaaS Asistencia Vehicular - IA")

# Incluimos el router maestro
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API de Asistencia Vehicular funcionando"}