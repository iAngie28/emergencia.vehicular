Este archivo detalla las dependencias y herramientas utilizadas en el ecosistema del proyecto (Backend y Frontend).

## 🖥️ Backend (Python / FastAPI)

|   |   |   |
|---|---|---|
|**Librería**|**Propósito**|**Resumen de Uso**|
|**FastAPI**|Framework Web|Motor principal de la API REST. Proveedor de validación automática y documentación Swagger.|
|**Uvicorn**|Servidor ASGI|Servidor web ultra-rápido que ejecuta la aplicación FastAPI.|
|**SQLAlchemy**|ORM (Base de Datos)|Mapea las clases de Python a tablas de PostgreSQL y maneja la integridad referencial.|
|**Alembic**|Migraciones|Controla el versionado de la base de datos (creación y modificación de tablas).|
|**Pydantic**|Validación de Datos|Define los Schemas. Asegura que los JSON de entrada/salida tengan los tipos correctos y campos obligatorios.|
|**Passlib / Bcrypt**|Seguridad (Hashing)|Encripta contraseñas de forma segura (algoritmo bcrypt).|
|**python-jose**|Seguridad (JWT)|Generación, firmado y verificación de Tokens de sesión.|
|**psycopg2-binary**|Driver PostgreSQL|Conector nativo para hablar con el motor de base de datos.|
|**OpenAI / httpx**|Inteligencia Artificial|Consumo de APIs externas (ej. modelo Whisper para voz a texto y LLMs para clasificación).|

## 📱 Frontend (React / Web)

|   |   |   |
|---|---|---|
|**Librería**|**Propósito**|**Resumen de Uso**|
|**React**|Biblioteca de UI|Gestiona los componentes visuales y el estado de la aplicación.|
|**React Router DOM**|Enrutamiento|Permite la navegación entre Login, Reporte y Dashboard sin recargar la página.|
|**Axios / Fetch**|Cliente HTTP|Realiza las peticiones a la API e incluye interceptores para inyectar el token JWT.|
|**Tailwind CSS**|Estilizado (CSS)|Framework de utilidades para diseño rápido y responsivo adaptable a móviles.|
|**Lucide React**|Iconografía|Proporciona iconos vectoriales ligeros para la interfaz.|