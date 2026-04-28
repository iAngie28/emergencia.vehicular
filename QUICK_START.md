# ⚡ REFERENCIA RÁPIDA - COMANDOS DE EJECUCIÓN

## 🎬 Ejecución Rápida (Opción Automática - RECOMENDADO)

### Terminal 1: Backend
```powershell
cd backend
.\start-backend-dev.ps1
```

### Terminal 2: Flutter
```powershell
cd movil
.\start-flutter-app.ps1
```

---

## 🎬 Ejecución Manual (Opción Completa)

### Terminal 1: Backend
```powershell
# Paso 1: Ir a directorio backend
cd backend

# Paso 2: Obtener tu IP (copia el IPv4 Address)
ipconfig

# Paso 3: Habilitar CORS "*" (importante para desarrollo)
$env:DEBUG="True"

# Paso 4: Iniciar servidor (escucha en todas las interfaces)
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Salida esperada:**
```
[⚠️  DESARROLLO] CORS configurado con '*' - ¡NO usar en producción!
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

### Terminal 2: Flutter
```powershell
# Paso 1: Conecta tu celular por USB con USB Debugging activado

# Paso 2: Ir a directorio mobile
cd movil

# Paso 3: Verificar dispositivos conectados
flutter devices

# Paso 4: IMPORTANTE - Editar backend_config.dart si tu IP ≠ 192.168.56.1
# Edita: movil/lib/backend_config.dart
# Línea ~17: static const String _localNetworkIp = '192.168.56.1';
# Reemplaza con tu IP si es diferente

# Paso 5: Ejecutar app en dispositivo
flutter run --verbose
```

---

## 🧪 Verificación de Conectividad

### Desde Laptop:
```bash
# Probar backend está corriendo
curl http://localhost:8000/
# Respuesta: {"message":"API de Asistencia Vehicular funcionando"}

# Acceder a documentación
# Navegador: http://localhost:8000/docs
# o: http://localhost:8000/redoc
```

### Desde Celular:
```
1. Abre la app Flutter
2. Debería mostrar pantalla de login
3. Logs en terminal muestran: "http://192.168.56.1:8000"
4. Intenta login: cliente_0@correo.com / password123
```

---

## 📋 Variables de Entorno (Si necesitas)

### Activar CORS "*" para desarrollo:
```powershell
$env:DEBUG="True"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Cambiar Puerto (si 8000 está ocupado):
```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload
# Luego edita: movil/lib/backend_config.dart
# Línea ~6: static const String _defaultPort = '9000';
```

### Usar URL personalizada en Flutter:
```powershell
cd movil
flutter run --dart-define=BACKEND_URL=http://192.168.1.100:8000
```

---

## 🔧 Editar URLs si tu IP es diferente

### Si tu IP NO es 192.168.56.1:

**1. Edita Flutter:**
```dart
// Archivo: movil/lib/backend_config.dart
// Línea ~17:
static const String _localNetworkIp = '192.168.56.1';  // ← CAMBIA A TU IP
```

**2. Edita Backend (opcional, para claridad):**
```python
# Archivo: backend/main.py
# Línea ~20:
"http://192.168.56.1:8000",  # ← CAMBIA A TU IP
```

---

## 🎮 Atajos en Flutter Durante Ejecución

```
r  → Hot reload (recarga código sin reiniciar app)
R  → Hot restart (reinicia app completamente)
w  → Show widget code location
t  → Trace widget
q  → Quit (salir)
s  → Screenshot
```

---

## 🐛 Comandos de Diagnóstico

### Ver dispositivos conectados:
```bash
flutter devices
```

### Ver logs detallados:
```bash
flutter run --verbose
```

### Limpiar build anterior:
```bash
flutter clean
flutter pub get
flutter run
```

### Ver logs del backend en tiempo real:
```bash
# En Terminal 1 (backend está corriendo):
# Los logs aparecen automáticamente
```

---

## 📊 URLs de Acceso

| Contexto | URL | Puerto |
|----------|-----|--------|
| **Laptop - Backend** | `http://localhost:8000` | 8000 |
| **Laptop - Angular** | `http://localhost:4200` | 4200 |
| **Laptop - Swagger** | `http://localhost:8000/docs` | 8000 |
| **Celular - Backend** | `http://192.168.56.1:8000` | 8000 |
| **Celular - Swagger** | `http://192.168.56.1:8000/docs` | 8000 |
| **Emulador Android** | `http://10.0.2.2:8000` | 8000 |
| **iOS Simulator** | `http://localhost:8000` | 8000 |

---

## ✅ Credenciales de Prueba

```
Email: cliente_0@correo.com
Contraseña: password123

Rol: Cliente
Acceso: Móvil ✅
```

---

## ⚠️ Errores Comunes y Soluciones

### Error: "Connection refused"
```bash
# Solución: Backend no está corriendo
# Terminal 1: Inicia backend con start-backend-dev.ps1
```

### Error: "CORS error" en app
```bash
# Solución: CORS no está habilitado
# Terminal 1: $env:DEBUG="True" antes de ejecutar
```

### Error: "No hay dispositivos"
```bash
# Solución: Celular no conectado
# 1. Conecta por USB
# 2. flutter devices
# 3. flutter run
```

### Error: "Timeout en login"
```bash
# Solución: Laptop y celular no en misma WiFi
# 1. Verifica ambos conectados a MISMA red WiFi
# 2. Verifica firewall no bloquea puerto 8000
```

---

## 🚀 One-Liner (Ejecución Rápida)

### Backend:
```powershell
cd backend && $env:DEBUG="True" && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Flutter:
```powershell
cd movil && flutter run --verbose
```

---

## 📌 Checklist Previo

- [ ] Laptop IP: _______________  (ejecuta: `ipconfig`)
- [ ] Backend_config.dart actualizado con IP correcta
- [ ] Backend corriendo en Terminal 1
- [ ] Celular conectado por USB
- [ ] USB Debugging activado en celular
- [ ] Misma WiFi en laptop y celular
- [ ] DEBUG=True configurado en Terminal 1
- [ ] Flutter run ejecutándose en Terminal 2

---

**¡Listo! La app debería conectarse en ~30 segundos. 🚀**
