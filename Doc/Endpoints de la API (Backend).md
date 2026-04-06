Este documento describe exclusivamente las puertas de enlace y servicios expuestos por la API (Backend) del SaaS de Asistencia Vehicular.

Todas las rutas detalladas a continuación tienen el prefijo `/api/v1/`. La documentación interactiva completa y lista para ser probada (Swagger UI) se encuentra en la ruta raíz `/docs`.

> **Nota de Desarrollo:** El enrutamiento del Frontend y el módulo de Autenticación (`/auth/login`) se encuentran en fase de implementación. Actualmente, las pruebas de los endpoints se realizan inyectando identificadores de prueba o directamente desde Swagger.

## 1. Módulo de Incidentes (Core con IA)

|   |   |   |
|---|---|---|
|**Endpoint**|**Método**|**Función**|
|`/incidentes/reportar`|`POST`|(Cliente) Recibe audio, procesa IA (transcripción/resumen) y crea reporte.|
|`/incidentes/`|`GET`|(Taller) Lista incidentes activos filtrados por el taller.|
|`/incidentes/{id}/estado`|`PATCH`|(Taller) Actualiza el estado de un incidente (En Proceso, Atendido).|
|`/incidentes/{id}/evidencia`|`POST`|Permite adjuntar fotos o archivos multimedia al incidente.|

## 2. Módulo de Administración (Talleres y Usuarios)

|   |   |   |
|---|---|---|
|**Endpoint**|**Método**|**Función**|
|`/talleres/`|`GET/POST`|Gestión del catálogo maestro de talleres y comisiones.|
|`/vehiculos/`|`GET/POST`|CRUD de vehículos (Registro de marca, modelo, placa única).|
|`/pagos/`|`POST`|Registra una transacción económica validando restricciones.|

## 3. Notas para QA y Evaluación

1. **Aislamiento Multitenant (Pendiente de Auth):** Una vez integrado el JWT, rutas como `GET /incidentes/` inferirán automáticamente el `taller_id` del token. Durante esta fase, el ID puede ser proporcionado manualmente o mediante un usuario mock.
    
2. **Validaciones Swagger:** Todos los endpoints cuentan con validación estricta de Pydantic. Si se envían datos con formatos incorrectos (como un ID de vehículo inexistente), la API responderá de inmediato con errores descriptivos `422 Unprocessable Entity` o `400 Bad Request` gracias a nuestra configuración de Integridad Referencial en Postgres.