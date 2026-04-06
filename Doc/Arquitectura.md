# Arquitectura del Sistema (Clean Architecture en FastAPI)
![Request Invalido](https://github.com/user-attachments/assets/2222a2c4-d772-49bd-bcf2-9f84e5e440d4)
![Request Valido](https://github.com/user-attachments/assets/7e1d2f9d-048a-48c3-b378-4a604db36852)

Este documento detalla la arquitectura del sistema SaaS de Asistencia Vehicular, explicando cómo se comunican las diferentes capas, el propósito de cada herramienta y la estructura de carpetas.

El sistema sigue una arquitectura **Desacoplada (Decoupled Architecture)**, donde el Frontend (React/Vue/App) y el Backend (FastAPI) son aplicaciones completamente independientes que se comunican exclusivamente mediante una **API REST** usando formato JSON.

En el Backend, aplicamos los principios de **Clean Architecture** (arquitectura por capas) para separar las responsabilidades de red, validación, reglas de negocio e infraestructura.

## 1. Arquitectura del Backend (FastAPI + API REST)

FastAPI actúa puramente como un motor de lógica asíncrona, proveedor de datos e integrador de Inteligencia Artificial (OpenAI/Whisper).

### 🧠 El Corazón de la Arquitectura: Routers, Schemas, Services y CRUD

Para que el sistema sea escalable y fácil de mantener, el procesamiento de cada petición se divide en cuatro actores principales:

1. **El Router (El Orquestador - `app/api/`):**
    
    - **Función:** Es la puerta de entrada HTTP. Recibe la petición, verifica el token JWT mediante Dependencias, llama al Servicio y devuelve la respuesta.
        
    - **Regla:** _No contiene lógica de negocio ni consultas SQL._
        
2. **El Schema / Pydantic (El Traductor y Filtro - `app/schemas/`):**
    
    - **Función:** Es la "Aduana" de QA. Valida que los datos de entrada sean correctos (ej. correos válidos, tipos de datos correctos) y serializa los objetos de base de datos a JSON para la salida.
        
3. **El Servicio (El Cerebro - `app/services/`):**
    
    - **Función:** Aquí vive la inteligencia del sistema. Ejecuta llamadas a la IA (transcripción de audio, resumen), calcula comisiones o asigna prioridades.
        
    - **Regla:** _No sabe qué es una base de datos directamente, delega la persistencia al CRUD._
        
4. **El CRUD (Acceso a Datos - `app/crud/`):**
    
    - **Función:** Se encarga exclusivamente de hablar con PostgreSQL usando SQLAlchemy.
        
    - **Regla:** _Aquí se aplica el filtro Multitenant inyectando el `taller_id` en las consultas._
        

### 🔄 ¿Cómo funciona el flujo de una petición?

1. **La Petición:** El Frontend envía una petición HTTP (ej. `POST /api/v1/incidentes/reportar`) adjuntando el JWT y el archivo de audio.
    
2. **El Router & Dependencias:** FastAPI recibe la petición, lee el JWT, identifica al usuario y su `taller_id` asociado.
    
3. **El Schema:** Pydantic valida que la petición tenga el formato correcto.
    
4. **El Servicio:** Se envía el audio a la IA (Whisper) para obtener el texto.
    
5. **El CRUD:** El Servicio le pide al CRUD que guarde el nuevo Incidente en la BD (`app/models/`), vinculándolo al `usuario_id` y `vehiculo_id`.
    
6. **La Respuesta:** El objeto creado se traduce a JSON a través del Schema y FastAPI responde con un `201 Created`.
    

## 2. Arquitectura del Frontend

El Frontend es una **Single Page Application (SPA)**. Carga una sola vez y actualiza las partes necesarias solicitando datos al Backend asíncronamente.

### 🔄 ¿Cómo funciona el flujo en el Cliente?

1. **Rutas:** El enrutador lee la URL y decide qué componente mostrar (ej. Vista de Mecánico vs. Vista de Cliente).
    
2. **Estado:** El componente declara su estado local o lee el estado global (Context/Store).
    
3. **Efecto:** Al cargar la pantalla de Incidentes, dispara una petición vía **Axios/Fetch** al Backend, adjuntando el Token automáticamente mediante Interceptores.
    
4. **Renderizado:** Al recibir la respuesta JSON, actualiza la interfaz mostrando los reportes priorizados por la IA.
