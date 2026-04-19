# 📱 Guía de Implementación - App Móvil Emergencia Vehicular

## ✅ Implementado

### **Servicios**
- ✅ **IncidenteService**: Reportar, ver estado, listar mis incidentes
- ✅ **VehiculoService**: Registrar, listar, actualizar, eliminar vehículos
- ✅ **PagoService**: Ver historial de pagos, facturas pendientes
- ✅ **NotificacionService**: Gestión de notificaciones y tokens FCM
- ✅ **UsuarioService**: Gestión de perfil del usuario
- ✅ **TallerService**: Obtener talleres activos (búsqueda de talleres cercanos pendiente)

### **Providers (Estado Global)**
- ✅ AuthProvider
- ✅ IncidenteProvider
- ✅ VehiculoProvider
- ✅ PagoProvider
- ✅ NotificacionProvider
- ✅ UsuarioProvider

### **Pantallas**
- ✅ LoginPage - Autenticación con backend
- ✅ HomePage - Pantalla principal con 3 tabs (Inicio, Historial, Perfil)
- ✅ ReportarIncidenteScreen - Formulario para reportar incidente
- ✅ MisIncidentesScreen - Historial de incidentes del cliente
- ✅ MisVehiculosScreen - Listado y gestión de vehículos
- ✅ RegistrarVehiculoScreen - Formulario para registrar vehículo
- ✅ PagosScreen - Historial de pagos y facturas pendientes
- ✅ PerfilScreen - Perfil del usuario con opciones de editar

### **Configuración Backend**
- ✅ CORS actualizado para permitir conexiones desde mobile

---

## 🚀 Pasos para Ejecutar y Probar

### **1. Configurar la URL del Backend**

Edita `lib/main.dart` línea 40:

```dart
const String backendUrl = 'http://localhost:5000'; 
// Cambiar a tu configuración:
// - Localhost: http://localhost:5000
// - IP Local: http://192.168.X.X:5000
// - Servidor remoto: https://api.ejemplo.com
```

### **2. Asegurar CORS en Backend**

El `main.py` del backend ya tiene CORS configurado con `"*"` para desarrollo.
En **producción**, cambiar a IP específica:

```python
allow_origins=[
    "http://192.168.0.XX:PUERTO_APP",
]
```

### **3. Ejecutar el Backend (FastAPI)**

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### **4. Ejecutar la App Móvil (Flutter)**

```bash
cd movil
flutter pub get
flutter run
```

---

## 🧪 Flujo de Pruebas Recomendado

### **Prueba 1: Autenticación**
1. Abre la app
2. Ingresa credenciales de usuario cliente
3. Verifica que accedas a HomePage

### **Prueba 2: Registrar Vehículo**
1. Ve a "Mis Vehículos"
2. Toca "+" o "Registrar Vehículo"
3. Llena todos los datos
4. Verifica que aparezca en la lista

### **Prueba 3: Reportar Incidente**
1. Ve a "Reportar Incidente"
2. Selecciona un vehículo
3. Llena descripción y ubicación
4. Toca "Reportar Incidente"
5. Verifica en "Historial"

### **Prueba 4: Ver Pagos**
1. Ve a "Pagos y Facturas"
2. Verifica historial de pagos
3. Verifica facturas pendientes

### **Prueba 5: Perfil**
1. Toca el tab de "Perfil"
2. Edita información del usuario
3. Cambia contraseña
4. Verifica cambios

---

## ⚠️ FUNCIONALIDADES NO DISPONIBLES (Pendientes)

### **Búsqueda de Talleres Cercanos**
**Estado**: ⏳ Pendiente para próxima versión

**Por implementar**:
- [ ] Servicio de geolocalización (package: `geolocator`)
- [ ] Cálculo de distancia entre usuario y talleres
- [ ] Mostrar talleres ordenados por proximidad al incidente
- [ ] Endpoint `/talleres/cercanos` en backend

**Código placeholder**: `TallerService.obtenerTalleresCercanos()`

**Cómo se usará**:
```dart
final talleresCercanos = await tallerService.obtenerTalleresCercanos(
  latitud: usuarioLat,
  longitud: usuarioLng,
  radioKm: 5.0,
);
```

### **Notificaciones Push (FCM)**
**Estado**: ⏳ Integración básica lista, requiere configuración Firebase

**Configurar**:
1. Crear proyecto en Firebase Console
2. Descargar `google-services.json` (Android)
3. Descargar `GoogleService-Info.plist` (iOS)
4. Ubicar en carpetas correspondientes del proyecto Flutter

---

## 🔄 Flujo de Datos

```
┌─────────────────────────────────────────────────────┐
│           Flutter Mobile App                        │
│  ┌──────────────────────────────────────────────┐  │
│  │ UI Screens (main.dart, screens/)             │  │
│  └─────────────────┬──────────────────────────┘  │
│                    │                              │
│  ┌─────────────────▼──────────────────────────┐  │
│  │ Providers (state management)               │  │
│  │ - AuthProvider                             │  │
│  │ - IncidenteProvider                        │  │
│  │ - VehiculoProvider, PagoProvider, etc.     │  │
│  └─────────────────┬──────────────────────────┘  │
│                    │                              │
│  ┌─────────────────▼──────────────────────────┐  │
│  │ Services (business logic)                  │  │
│  │ - AuthService, IncidenteService            │  │
│  │ - VehiculoService, PagoService, etc.       │  │
│  └─────────────────┬──────────────────────────┘  │
│                    │                              │
│  ┌─────────────────▼──────────────────────────┐  │
│  │ ApiService (HTTP client)                   │  │
│  │ - GET, POST, PUT, PATCH, DELETE            │  │
│  └─────────────────┬──────────────────────────┘  │
└────────────────────┼──────────────────────────────┘
                     │ HTTP (JSON)
                     │
         ┌───────────▼──────────┐
         │  FastAPI Backend     │
         │  /api/v1/*           │
         │  (main.py)           │
         └──────────────────────┘
```

---

## 📝 Notas Importantes

### **URL del Backend**
- **Desarrollo**: `http://localhost:5000`
- **Pruebas en Teléfono**: `http://192.168.X.X:5000` (IP local del PC)
- **ID de Usuario Temporal**: Actualmente se usa `usuarioId = 1` para pruebas

### **Endpoints Disponibles**
```
POST   /api/v1/auth/login                    (Login)
POST   /api/v1/incidentes/                   (Reportar)
GET    /api/v1/incidentes/mis-reportes       (Mis incidentes)
GET    /api/v1/incidentes/{id}/estado        (Estado de incidente)
POST   /api/v1/vehiculos/                    (Registrar vehículo)
GET    /api/v1/vehiculos/usuario/{id}        (Mis vehículos)
PUT    /api/v1/vehiculos/{id}                (Actualizar vehículo)
DELETE /api/v1/vehiculos/{id}                (Eliminar vehículo)
GET    /api/v1/pagos/mi-historial            (Mis pagos)
GET    /api/v1/pagos/pendientes              (Facturas pendientes)
GET    /api/v1/usuarios/me                   (Mi perfil)
PUT    /api/v1/usuarios/me                   (Actualizar perfil)
POST   /api/v1/notificaciones/tokens         (Registrar token FCM)
GET    /api/v1/notificaciones/usuario/{id}/pendientes  (Notificaciones)
GET    /api/v1/talleres/activos              (Talleres disponibles)
```

### **Estructura de Carpetas**
```
movil/lib/
├── main.dart                    (Entrada principal)
├── screens/                     (Pantallas)
│   ├── incidentes/
│   ├── vehiculos/
│   ├── pagos/
│   └── perfil/
├── services/                    (Lógica de API)
│   ├── api_service.dart
│   ├── auth_service.dart
│   ├── incidente_service.dart
│   ├── vehiculo_service.dart
│   ├── pago_service.dart
│   ├── notificacion_service.dart
│   ├── usuario_service.dart
│   └── taller_service.dart
├── providers/                   (Estado global)
│   ├── auth_provider.dart
│   ├── incidente_provider.dart
│   ├── vehiculo_provider.dart
│   ├── pago_provider.dart
│   ├── notificacion_provider.dart
│   └── usuario_provider.dart
└── theme/
    └── colors.dart
```

---

## 🔍 Debugging

### **Ver logs de la API**
```bash
flutter logs
```

### **Ver respuestas HTTP**
En ApiService, agregar print:
```dart
print('Response: ${response.body}');
```

### **Revisar token JWT**
```dart
final token = await authProvider.authService.getToken();
print('Token: $token');
```

---

## ✨ Próximas Mejoras

- [ ] Integrar geolocalización para búsqueda de talleres cercanos
- [ ] Configurar Firebase Cloud Messaging para notificaciones push
- [ ] Agregar autenticación de fotografías para incidentes
- [ ] Implementar sistema de chat con taller
- [ ] Modo offline (sincronización local)
- [ ] Temas oscuros/claros
- [ ] Internacionalización (i18n)

---

## 📞 Soporte

Si encuentras errores:
1. Revisa los logs: `flutter logs`
2. Verifica que el backend esté corriendo
3. Confirma la URL del backend en `main.dart`
4. Limpia caché: `flutter clean && flutter pub get`

**¡Listo para probar en tu teléfono!** 🚀
