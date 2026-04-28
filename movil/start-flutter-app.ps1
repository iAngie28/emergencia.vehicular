#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script para iniciar la app Flutter en dispositivo físico conectado
    Configura automáticamente la URL del backend basada en tu IP local

.DESCRIPTION
    Detecta:
    1. Tu IP de laptop
    2. Dispositivos Flutter conectados
    3. Ejecuta la app con logs detallados

.EXAMPLE
    .\start-flutter-app.ps1
    # Inicia app en dispositivo física

.NOTES
    Requisitos:
    1. Celular conectado por USB con USB Debugging habilitado
    2. Flutter SDK instalado
    3. Backend corriendo en tu laptop (start-backend-dev.ps1)
#>

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       📱 INICIANDO APP FLUTTER EN DISPOSITIVO FÍSICO 📱      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Verificar que estamos en directorio correcto
if (-not (Test-Path "pubspec.yaml")) {
    Write-Host "[ERROR] ❌ No se encontró pubspec.yaml" -ForegroundColor Red
    Write-Host "[INFO] Asegúrate de estar en: movil/" -ForegroundColor Yellow
    exit 1
}

# Obtener IP
Write-Host "[INFO] 🔍 Detectando IP de tu laptop..." -ForegroundColor Yellow
$ipInfo = ipconfig | Select-String -Pattern "IPv4" | Select-Object -First 1
$ipLine = $ipInfo -replace '\s+', ' '
$ipAddress = ($ipLine -split ' ')[-1]

Write-Host "[OK] ✅ IP detectada: $ipAddress" -ForegroundColor Green
Write-Host ""

# Detectar dispositivos
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔎 Escaneando dispositivos..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan

$devices = flutter devices 2>&1

if ($devices -match "0 connected devices") {
    Write-Host "[ERROR] ❌ No hay dispositivos conectados!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Soluciones:" -ForegroundColor Yellow
    Write-Host "1. Conecta tu celular por USB" -ForegroundColor White
    Write-Host "2. Habilita USB Debugging en el celular" -ForegroundColor White
    Write-Host "3. Acepta los permisos de conexión" -ForegroundColor White
    Write-Host ""
    Write-Host "Después, ejecuta de nuevo:" -ForegroundColor Cyan
    Write-Host "  flutter devices" -ForegroundColor Yellow
    exit 1
}

Write-Host $devices
Write-Host ""

# Mostrar configuración
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "⚙️  CONFIGURACIÓN AUTOMÁTICA:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Backend URL: http://$ipAddress`:8000" -ForegroundColor Green
Write-Host "Backend_config.dart: Ya configurado automáticamente ✅" -ForegroundColor Green
Write-Host ""

# Preguntar sobre clean build
Write-Host "¿Limpiar build anterior? (recomendado para primer run)" -ForegroundColor Yellow
$choice = Read-Host "Escribe 's' para sí, 'n' para no [n]"

if ($choice -eq 's' -or $choice -eq 'S') {
    Write-Host "[INFO] Limpiando build..." -ForegroundColor Yellow
    flutter clean
    flutter pub get
    Write-Host "[OK] ✅ Build limpiado" -ForegroundColor Green
    Write-Host ""
}

# Iniciar app
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🚀 Iniciando app en dispositivo..." -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Monitoreo:" -ForegroundColor Cyan
Write-Host "   → Puedes ver logs en tiempo real" -ForegroundColor Yellow
Write-Host "   → Presiona 'r' para hot-reload" -ForegroundColor Yellow
Write-Host "   → Presiona 'R' para hot-restart" -ForegroundColor Yellow
Write-Host "   → Presiona 'q' para salir" -ForegroundColor Yellow
Write-Host ""

# Ejecutar app
flutter run --verbose

Write-Host ""
Write-Host "[INFO] ℹ️  App detenida." -ForegroundColor Yellow
Write-Host "[INFO] Para reiniciar, ejecuta este script de nuevo." -ForegroundColor Yellow
