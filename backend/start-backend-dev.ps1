#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script para iniciar el backend FastAPI en modo desarrollo con CORS permisivo
    Permite conectividad desde dispositivos físicos en la red local

.DESCRIPTION
    Inicia Uvicorn escuchando en 0.0.0.0:8000 con:
    - CORS habilitado para desarrollo ("*")
    - Auto-reload al cambiar código
    - Logs detallados

.EXAMPLE
    .\start-backend-dev.ps1
    # Inicia backend en http://0.0.0.0:8000 con CORS permitido

.NOTES
    Asegúrate de:
    1. Estar en el directorio backend/
    2. Tener Python activado (virtual env)
    3. Conectar tu celular a la MISMA WiFi
#>

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        🚀 INICIANDO BACKEND - Modo Desarrollo 🚀            ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] ❌ No se encontró main.py" -ForegroundColor Red
    Write-Host "[INFO] Asegúrate de estar en la carpeta: backend/" -ForegroundColor Yellow
    exit 1
}

# Obtener IP de la laptop
Write-Host "[INFO] 🔍 Detectando IP de tu laptop..." -ForegroundColor Yellow
$ipInfo = ipconfig | Select-String -Pattern "IPv4" | Select-Object -First 1
$ipLine = $ipInfo -replace '\s+', ' '
$ipAddress = ($ipLine -split ' ')[-1]

Write-Host "[OK] ✅ IP detectada: $ipAddress" -ForegroundColor Green
Write-Host ""

# Mostrar instrucciones
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📱 PARA CONECTAR DESDE EL CELULAR:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "1. Asegúrate de que tu celular está en la MISMA WiFi" -ForegroundColor White
Write-Host "2. En Flutter, usa la URL: http://$ipAddress`:8000" -ForegroundColor Yellow
Write-Host "3. Backend_config.dart está configurado automáticamente" -ForegroundColor White
Write-Host ""

# Configurar modo desarrollo
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "⚙️  CONFIGURACIÓN:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Configurando: DEBUG=True (CORS: '*' habilitado)" -ForegroundColor White
Write-Host "Host: 0.0.0.0 (escucha en TODAS las interfaces)" -ForegroundColor White
Write-Host "Puerto: 8000" -ForegroundColor White
Write-Host "Auto-reload: Habilitado" -ForegroundColor White
Write-Host ""

# Establecer variable de entorno
$env:DEBUG = "True"

# Iniciar servidor
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🚀 Iniciando servidor..." -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏱️  El servidor debería estar disponible en:" -ForegroundColor Cyan
Write-Host "   → Laptop:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "   → Celular:  http://$ipAddress`:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Acceso a documentación:" -ForegroundColor Cyan
Write-Host "   → Swagger UI: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "   → ReDoc:      http://localhost:8000/redoc" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏹️  Para detener: Presiona Ctrl+C" -ForegroundColor Cyan
Write-Host ""

# Ejecutar uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Si se detiene, mostrar mensaje
Write-Host ""
Write-Host "[INFO] ℹ️  Servidor detenido." -ForegroundColor Yellow
Write-Host "[INFO] Para reiniciar, ejecuta este script de nuevo." -ForegroundColor Yellow
