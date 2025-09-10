# SQL Agent - Base de Datos SAKILA

## Requisitos Previos

- Docker
- Docker Compose

## Configuración de la Base de Datos

La base de datos SAKILA está completamente configurada y lista para usar. Los archivos de esquema y datos en español ya están incluidos en el repositorio.

**Fuentes de la base de datos:**
- Esquema en español: https://gist.github.com/josejuansanchez/b44d3d1f84800eb07e188958e99de9bc
- Datos en español: https://gist.github.com/josejuansanchez/122675071cdacce7f7ba61051707dae3

### Levantar la base de datos MySQL con SAKILA

```bash
docker-compose up -d
```

### Detener la base de datos

```bash
docker-compose down
```

## Información de Conexión

- **Host**: localhost
- **Puerto**: 3307
- **Base de datos**: sakila
- **Usuario**: root
- **Contraseña**: sakila_password

## Conexión desde aplicación Node.js

```javascript
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',
  port: 3307,
  user: 'root',
  password: 'sakila_password',
  database: 'sakila'
});
```

## Backend Python - SQL Agent

El sistema incluye un backend Python que convierte consultas en lenguaje natural a SQL usando OpenAI API o Docker Model Runner.

### Configuración

1. **Configura el archivo .env**:
   ```bash
   # Copia el archivo de ejemplo y edítalo con tu API key
   cp .env.example .env
   # Edita .env y coloca tu OPENAI_API_KEY real
   ```

2. **Variables de entorno en .env**:
   ```bash
   # Para usar OpenAI
   LLM_PROVIDER=openai
   OPENAI_API_KEY=tu_api_key_aqui
   OPENAI_MODEL=gpt-4

   # Para usar modelo local
   LLM_PROVIDER=docker_runner
   DOCKER_RUNNER_MODEL=ai/smollm2:latest
   ```

### Opciones de ejecución:

#### Con OpenAI API (recomendado):
```bash
# Asegúrate de tener configurado OPENAI_API_KEY en .env
docker-compose up -d
```

#### Con Docker Model Runner (modelo local):
```bash
# Habilitar Docker Model Runner en Docker Desktop primero
# Cambiar LLM_PROVIDER=docker_runner en .env
docker-compose --profile with-llm up -d
```

#### Sistema completo con modelo local:
```bash
docker-compose --profile full up -d
```

### Puertos

- **Frontend**: http://localhost:8080
- **Backend Python**: http://localhost:5000
- **Base de datos**: localhost:3307

El frontend ya está preparado con `callPythonService()` en puerto 5000 para conectarse automáticamente al backend Python.