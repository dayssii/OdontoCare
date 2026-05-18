# OdontoCare — Sistema de Gestión de una Clínica Dental

API RESTful distribuida en microservicios para gestión de citas dentales.
Proyecto final del curso Python C1 - Escuela de Programación UOC.

## Arquitectura

El sistema está dividido en dos microservicios independientes:

- **service_admin** (puerto 5000): gestiona usuarios, doctores, pacientes y centros médicos
- **service_citas** (puerto 5001): gestiona las citas médicas, comunicándose con service_admin para validar datos

## Requisitos
Para ejecutar el proyecto se requiere la instalación de:
- Python 3.11+
- pip
- Docker y Docker Compose (opcional)

## Instalación y ejecución en local
Para arrancar cada servicio tenemos los comandos:
### service_admin
```bash
cd service_admin
pip install -r requirements.txt
python app.py
```

### service_citas
```bash
cd service_citas
pip install -r requirements.txt
python app.py
```

### Cliente
```bash
cd cliente
python carga_inicial.py
```

## Ejecución con Docker

```bash
docker-compose up --build
```

## Endpoints
Rutas del API, método HTTP y que realiza cada tabla:
### Auth (service_admin :5000)
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /auth/login | Login, devuelve JWT |

### Admin (service_admin :5000) — requiere rol admin
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /admin/usuario | Crear usuario admin o secretaria |
| POST | /admin/doctores | Crear doctor |
| GET | /admin/doctores | Listar doctores |
| GET | /admin/doctores/<id> | Obtener doctor por ID |
| POST | /admin/pacientes | Crear paciente |
| GET | /admin/pacientes | Listar pacientes |
| GET | /admin/pacientes/<id> | Obtener paciente por ID |
| POST | /admin/centros | Crear centro médico |
| GET | /admin/centros | Listar centros |
| GET | /admin/centros/<id> | Obtener centro por ID |

### Citas (service_citas :5001) — requiere JWT
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /citas | Agendar cita |
| GET | /citas | Listar citas |
| GET | /citas/<id> | Obtener cita por ID |
| PUT | /citas/<id> | Cancelar cita |

## Autenticación

Todos los endpoints protegidos requieren el header: Authorization: Bearer <token>

## Usuario por defecto
Al arrancar por primera vez se crea automáticamente:
- **username:** admin
- **password:** admin123