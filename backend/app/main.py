"""
VialIA Backend - Emergency Vehicle Assistance System with AI Integration

Production-ready FastAPI application for emergency vehicle reporting with:
- Multimodal AI processing (audio transcription + image analysis)
- Hugging Face Inference API integration
- Comprehensive CORS configuration for Flutter mobile + Angular frontend
- Environment-based deployment (development/staging/production on Render)

Author: VialIA Team
License: MIT
"""

import os
import logging
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base  # Importamos el que tiene todos los modelos
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# APPLICATION INITIALIZATION
# ============================================================
app = FastAPI(
    title="VialIA - Sistema de Asistencia Vehicular",
    description="Emergency vehicle reporting with AI-powered multimodal analysis",
    version="1.0.0",
)

# ============================================================
# CORS CONFIGURATION
# Production-ready CORS with support for:
# - Local development (Angular + Flutter emulator/simulator)
# - Mobile devices (physical Android/iOS)
# - Production frontend (Render deployment)
# ============================================================

# Get environment variables with sensible defaults
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "")

# Build CORS origins list
cors_origins = [
    # === LOCAL DEVELOPMENT ===
    # Angular Frontend (Web)
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    # Ionic Frontend (Mobile Web)
    "http://localhost:8100",
    "http://127.0.0.1:8100",
    # Flutter Mobile - Android Emulator
    "http://10.0.2.2:8000",
    "http://10.0.2.2:3000",
    # Flutter Mobile - iOS Simulator
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Local network access (physical devices on development machine)
    "http://192.168.56.1:8000",
    "http://192.168.56.1:3000",
    # Alternative local network patterns
    "http://192.168.*:*",
]

# === PRODUCTION URLS ===
if RENDER_EXTERNAL_URL:
    cors_origins.append(RENDER_EXTERNAL_URL)
    logger.info(f"Added Render production URL: {RENDER_EXTERNAL_URL}")

if FRONTEND_URL:
    cors_origins.append(FRONTEND_URL)
    logger.info(f"Added custom frontend URL: {FRONTEND_URL}")

# For production, you can add your production domain here
# Example:
# cors_origins.append("https://vialia-frontend.onrender.com")
# cors_origins.append("https://app.vialia.com")

# Log CORS configuration
logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Permite Angular
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (Content-Type, Authorization, etc.)
    max_age=3600,  # Cache CORS preflight for 1 hour
)

# ============================================================
# API ROUTES
# ============================================================
# Incluimos el router maestro con todos los endpoints
app.include_router(api_router, prefix="/api/v1")


# ============================================================
# HEALTH CHECK ENDPOINTS
# ============================================================
@app.get("/")
def root():
    """Root endpoint - API status check."""
    return {
        "message": "API de Asistencia Vehicular funcionando",
        "service": "VialIA Backend with AI Integration",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and deployment verification."""
    return {
        "status": "healthy",
        "service": "vialia-backend",
        "ai_enabled": os.getenv("HF_API_TOKEN") is not None,
    }


@app.get("/ready")
def readiness_check():
    """Readiness check endpoint - ensures all dependencies are available."""
    try:
        # Check database connection
        from app.db.session import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "ready": True,
            "database": "connected",
            "ai_service": "available" if os.getenv("HF_API_TOKEN") else "disabled",
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return {
            "ready": False,
            "error": str(e),
        }


# ============================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("=== VialIA Backend Starting ===")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"CORS Configuration: {len(cors_origins)} allowed origins")
    
    # Check AI service configuration
    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token:
        logger.info("✓ Hugging Face API Token configured - AI features enabled")
    else:
        logger.warning("✗ Hugging Face API Token not configured - AI features disabled")
    
    # Initialize database
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("VialIA Backend shutting down...")