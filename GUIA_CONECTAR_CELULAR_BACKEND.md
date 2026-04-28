# 📱 GUÍA: CONECTAR CELULAR FÍSICO AL BACKEND EN LAPTOP

## 🎯 Resumen de Cambios

✅ **Flutter (backend_config.dart):**
- URL centralizada con soporte para dispositivos físicos
- IP configurada: `192.168.56.1:8000`
- Detecta automáticamente plataforma

✅ **Backend (main.py - CORS):**
- Acepta peticiones desde `192.168.56.1:8000` ✓
- Modo desarrollo con `CORS: "*"` habilitado ✓
- Compatible con emuladores, simuladores y dispositivos físicos

---

## 🚀 PASO 1: Obtener tu IP Real

En **PowerShell** (en tu laptop):

```powershell
ipconfig
```

Busca tu **IPv4 Address** en tu adaptador de red (WiFi o Ethernet).

**Ejemplo de salida:**
```
Adaptador de Ethernet:
   Dirección IPv4 . . . . . . . . : 192.168.56.1  ← ESTA ES TU IP
```

**❗ SI TU IP ES DIFERENTE DE `192.168.56.1`:**

Edita `movil/lib/backend_config.dart` y reemplaza:
```dart
static const String _localNetworkIp = '192.168.56.1';  // ← Cambia aquí
```

---

## 🚀 PASO 2: Iniciar Backend con Uvicorn

### Opción A: Desarrollo Local (RECOMENDADO para testing)

```bash
# Terminal en: backend/

# Con CORS permisivo ("*") para testing fácil
$env:DEBUG="True"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Salida esperada:**
```
[⚠️  DESARROLLO] CORS configurado con '*' - ¡NO usar en producción!
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Opción B: Producción (sin CORS permisivo)

```bash
# Sin CORS "*", solo IPs específicas
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Diferencia:**
- `--host 0.0.0.0` → Escucha en TODAS las interfaces de red
- `--port 8000` → Puerto del servidor
- `--reload` → Reinicia automático al cambiar código

---

## 🎮 PASO 3: Ejecutar App en Celular

### Con dispositivo conectado por USB:

```bash
# Terminal en: movil/

# Detecta dispositivos conectados
flutter devices

# Ejecutar app
flutter run
```

### Con el emulador ya corriendo:

```bash
flutter run -d <device-id>
```

**Ejemplo:**
```bash
flutter run -d "192.168.56.1"  # Si tu dispositivo se identifica así
```

---

## ✅ Verificación de Conectividad

### Desde tu Laptop:

Verifica que el backend está escuchando:

```bash
curl http://localhost:8000/
# Debería retornar: {"message":"API de Asistencia Vehicular funcionando"}
```

### Desde tu Celular (en la misma red WiFi):

En la terminal de la app Flutter, debería mostrar:

```
[CONFIG] Android - Dispositivo físico: http://192.168.56.1:8000
```

Luego prueba login:
```
Email: cliente_0@correo.com
Contraseña: password123
```

---

## 📊 Tabla de Conectividad

| Escenario | Host Backend | Puerto | URL |
|-----------|-------------|--------|-----|
| **Desarrollo Local** | 0.0.0.0 | 8000 | `http://localhost:8000` |
| **Dispositivo Físico** | 0.0.0.0 | 8000 | `http://192.168.56.1:8000` |
| **Emulador Android** | 0.0.0.0 | 8000 | `http://10.0.2.2:8000` |
| **Simulador iOS** | 0.0.0.0 | 8000 | `http://localhost:8000` |

---

## 🔧 Comandos Completos

### Backend - Desarrollo con CORS permisivo:
```bash
cd backend
$env:DEBUG="True"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Backend - Producción (sin CORS "*"):
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Flutter - Ejecutar en dispositivo:
```bash
cd movil
flutter run
```

### Flutter - Con URL personalizada (si necesitas override):
```bash
cd movil
flutter run --dart-define=BACKEND_URL=http://192.168.1.100:8000
```

---

## 🐛 Solución de Problemas

### ❌ "Connection refused" (conexión rechazada)

**Causa:** Backend no está escuchando en `0.0.0.0` o puerto diferente

**Solución:**
```bash
# Verifica que está corriendo
curl http://192.168.56.1:8000/

# Si no funciona, reinicia backend:
# 1. Cierra terminal con Ctrl+C
# 2. Inicia de nuevo con el comando anterior
```

### ❌ "CORS error" en app mobile

**Causa:** IP no está en lista blanca de CORS

**Solución:**
```bash
# 1. Asegúrate de tener CORS permitido:
$env:DEBUG="True"
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# 2. O agrega manualmente en backend/main.py:
origins = ["*"]
```

### ❌ "Network timeout" (timeout de red)

**Causa:** Celular y laptop no están en la misma WiFi

**Solución:**
1. Conecta ambos a la MISMA red WiFi
2. Verifica con: `ping 192.168.56.1` (desde celular si es posible)
3. Desactiva firewall temporalmente en laptop

### ❌ Error 403 "Acceso denegado: Use el Panel Web"

**Causa:** Intentas loguear como Admin desde móvil (no permitido)

**Solución:** Usa credenciales de Cliente o Técnico:
```
cliente_0@correo.com / password123
tec_1_0@taller.com / password123
```

---

## 📝 Checklist de Setup

- [ ] Backend corriendo con `--host 0.0.0.0`
- [ ] Obtuviste tu IP con `ipconfig`
- [ ] Actualiza `backend_config.dart` si tu IP ≠ 192.168.56.1
- [ ] Celular y laptop en MISMA WiFi
- [ ] CORS habilitado con `$env:DEBUG="True"`
- [ ] App Flutter ejecutándose en celular
- [ ] Logs muestran `http://192.168.56.1:8000`
- [ ] Login exitoso con `cliente_0@correo.com`

---

## 🎓 Notas Técnicas

### ¿Por qué `0.0.0.0`?
- `0.0.0.0` = Escucha en TODAS las interfaces (localhost, IPv4, IPv6)
- `localhost` o `127.0.0.1` = Solo conexiones locales (no desde red)

### ¿Por qué `192.168.56.1` es especial?
- Tu laptop en la red local tiene esta IP
- El celular se conecta a tu laptop usando esta dirección
- Es como si pusieran ambos en la misma mesa local

### ¿Qué es `CORS: "*"`?
- Permite peticiones desde CUALQUIER origen (temporalmente)
- Seguridad: 0% (solo para desarrollo)
- Producción: Desactiva esto y usa IPs específicas

---

**Próximo paso:** Ejecuta el backend y prueba desde el celular. ¡Deberíamos ver "Conexión Exitosa"! 🚀
