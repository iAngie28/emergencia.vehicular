# ✅ Checklist de Pruebas - App Móvil Emergencia Vehicular

## 🔧 Configuración Previa

- [ ] Backend (FastAPI) está corriendo en puerto 5000
- [ ] URL del backend actualizada en `lib/main.dart`
- [ ] CORS configurado en backend `main.py`
- [ ] Flutter dependencies instaladas (`flutter pub get`)
- [ ] Emulador o dispositivo conectado

---

## 🧪 Pruebas Unitarias

### **Autenticación**
- [ ] Login exitoso con credenciales válidas
- [ ] Rechazo de login con credenciales inválidas
- [ ] Token se guarda localmente en SharedPreferences
- [ ] Usuario se redirige a HomePage después del login
- [ ] Logout limpia el token

### **Vehículos**
- [ ] Registrar vehículo exitosamente
- [ ] Validación de campos requeridos
- [ ] Lista se actualiza después de registrar
- [ ] Ver detalles del vehículo
- [ ] Editar información del vehículo
- [ ] Eliminar vehículo de la lista

### **Incidentes**
- [ ] Reportar incidente con todos los datos
- [ ] Validación de vehículo seleccionado
- [ ] Validación de descripción
- [ ] Validación de ubicación
- [ ] Incidente aparece en "Mis Incidentes"
- [ ] Ver estado del incidente
- [ ] Ver detalles del incidente

### **Pagos**
- [ ] Ver historial de pagos realizados
- [ ] Ver facturas pendientes
- [ ] Mostrar total pendiente
- [ ] Ver detalles de pago
- [ ] (Futuro) Realizar pago

### **Perfil**
- [ ] Cargar perfil del usuario
- [ ] Editar información del perfil
- [ ] Cambiar contraseña
- [ ] Ver información actualizada
- [ ] Cerrar sesión

### **Notificaciones**
- [ ] (Futuro) Recibir notificación push
- [ ] Ver notificaciones no leídas
- [ ] Marcar notificación como leída
- [ ] Ver historial de notificaciones

---

## 🔌 Pruebas de Conectividad

- [ ] App conecta exitosamente al backend
- [ ] Manejo correcto de errores de conexión
- [ ] Timeout se maneja apropiadamente
- [ ] Re-intentos funcionan
- [ ] Headers Authorization se envían correctamente

---

## 🎨 Pruebas de UI/UX

### **Navegación**
- [ ] Bottom navigation bar funciona correctamente
- [ ] Transiciones entre pantallas son suaves
- [ ] Back button funciona
- [ ] Ingreso/salida de datos es intuitivo

### **Validaciones**
- [ ] Mensajes de error se muestran claramente
- [ ] Campos requeridos están marcados
- [ ] Loading spinner aparece durante carga
- [ ] Mensajes de éxito se muestran

### **Responsive Design**
- [ ] Pantalla se ve bien en diferentes tamaños
- [ ] Elementos no se sobreponen
- [ ] Scroll funciona donde es necesario

---

## 📊 Pruebas de Datos

- [ ] Los datos se sincronizan correctamente
- [ ] Los cambios se reflejan en tiempo real
- [ ] No hay corrupción de datos
- [ ] Cache se limpia cuando corresponde

---

## 🐛 Pruebas de Casos Límite

- [ ] Descripciones muy largas se manejan
- [ ] Nombres con caracteres especiales
- [ ] Conexión lenta (throttling)
- [ ] Conexión perdida durante operación
- [ ] App se reinicia inesperadamente

---

## 📱 Pruebas en Dispositivo Real

### **Android**
- [ ] Aceptar permisos de ubicación (si aplica)
- [ ] App funciona en API 21+
- [ ] Keyboard se abre/cierra correctamente
- [ ] Back button del sistema funciona

### **iOS**
- [ ] App lanza exitosamente
- [ ] Safe area respetada
- [ ] Touch ID/Face ID (si se implementa)
- [ ] Cerrar app desde multitask no causa crashes

---

## 📋 Pruebas de Integración

- [ ] Login → HomePage
- [ ] Registrar Vehículo → Aparece en Mis Vehículos
- [ ] Seleccionar Vehículo → Reportar Incidente
- [ ] Reportar Incidente → Ver en Historial
- [ ] Ver Incidente → Mostrar Estado
- [ ] Cerrar Sesión → Volver a Login

---

## 🚨 Casos de Error Esperados

- [ ] Backend offline → Mostrar mensaje de error
- [ ] Respuesta malformada del servidor → Manejo correcto
- [ ] Token expirado → Pedir login nuevamente
- [ ] Validación fallida en servidor → Mostrar error específico
- [ ] Archivo muy grande → Limite o rechazar

---

## 📝 Notas de Pruebas

```
Fecha: ________________
Dispositivo: __________
SO: ___________________
Versión App: __________

Resultados:
_________________________________________________
_________________________________________________
_________________________________________________

Bugs encontrados:
_________________________________________________
_________________________________________________
_________________________________________________

Mejoras sugeridas:
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## ✨ Estado General

**Todas las pruebas pasadas**: [ ]

**Bloqueadores encontrados**: [ ]

**Listo para producción**: [ ]

---

**Última actualización**: 19 de abril de 2026
