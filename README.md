# 🤖 SQL Agent - Traductor de Lenguaje Natural a SQL

[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)

> **SQL Agent** es una aplicación web que permite convertir consultas en lenguaje natural a consultas SQL utilizando modelos de inteligencia artificial. Diseñada para facilitar el acceso a bases de datos sin necesidad de conocer SQL en profundidad.

## 🚀 ¿Qué es SQL Agent?

SQL Agent es un sistema completo que combina:
- **Frontend web intuitivo** donde escribes en español natural
- **Backend inteligente** que traduce tu consulta usando IA
- **Base de datos de ejemplo** (SAKILA) lista para usar

**Ejemplo de uso:**
- Tú escribes: *"Los 5 clientes que más han gastado"*
- SQL Agent genera: `SELECT c.nombre, c.apellidos, SUM(p.cantidad) as total...`
- Ves los resultados en una tabla clara

## ✨ Características

- 🗣️ **Consultas en español natural** - Escribe como hablas
- 🤖 **IA avanzada** - Utiliza OpenAI GPT-4 o modelos locales
- 📊 **Resultados visuales** - Tablas claras con los datos
- 💡 **Explicaciones detalladas** - Entiende qué hace cada consulta
- 🔒 **Seguridad** - Solo consultas SELECT (lectura)
- 🐳 **Fácil instalación** - Todo con Docker
- 🌐 **Base de datos incluida** - SAKILA en español lista para usar

## 📋 Requisitos Previos

### 1. Docker Desktop (Última Versión)

**⚠️ IMPORTANTE**: Debes instalar Docker Desktop en su **última versión** para poder usar los modelos de IA locales.

1. **Descargar Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Instalar y ejecutar** Docker Desktop
3. **Habilitar Docker Model Runner**:
   - Ve a `Settings` → `Beta features`
   - Activa `Enable Docker Model Runner`
   - Activa `Enable host-side TCP support`

### 2. Modelo de IA Local (Opcional)

Si quieres usar modelos locales sin API keys:

1. **Abre Docker Desktop**
2. **Ve a la pestaña "Models (beta)"**
3. **Busca y descarga**: `ai/gpt-oss:latest`
   - Ve a "Docker Hub"
   - Busca "ai/gpt-oss"
   - Haz clic en "Pull" para descargar

## 🛠️ Instalación

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sql-agent.git
cd sql-agent
```

### Paso 2: Configurar Variables de Entorno
```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tu editor favorito
notepad .env  # Windows
nano .env     # Linux/Mac
```

### Paso 3: Configurar el archivo .env

**Para usar OpenAI API (Recomendado)**:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=tu_api_key_de_openai_aqui
OPENAI_MODEL=gpt-4
```

**Para usar modelo local (Gratis)**:
```bash
LLM_PROVIDER=docker_runner
DOCKER_RUNNER_MODEL=ai/gpt-oss:latest
```

### Paso 4: Ejecutar el Proyecto

**Con OpenAI API**:
```bash
docker-compose up -d
```

**Con modelo local**:
```bash
docker-compose --profile with-llm up -d
```

### Paso 5: Acceder a la Aplicación

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000
- **Base de datos**: localhost:3307

## 💻 Cómo Usar SQL Agent

1. **Abre tu navegador** en http://localhost:8080
2. **Escribe tu consulta** en español natural:
   - "Los actores de la película Titanic"
   - "Cuánto ha gastado cada cliente"
   - "Las películas más alquiladas"
3. **Haz clic en "Traducir a SQL"**
4. **Revisa la consulta** generada y haz clic en "Ejecutar SQL"
5. **Ve los resultados** en la tabla

## 🗃️ Base de Datos SAKILA

El proyecto incluye la **base de datos SAKILA** completamente configurada en español. SAKILA es una base de datos de ejemplo que simula un sistema de videoclub con:

### Tablas Principales:
- **actor** - Actores de las películas
- **pelicula** - Catálogo de películas
- **cliente** - Clientes del videoclub
- **alquiler** - Registros de alquileres
- **pago** - Historial de pagos
- **inventario** - Stock de películas
- **categoria** - Géneros cinematográficos

### Fuentes de la Base de Datos:
- **Esquema en español**: https://gist.github.com/josejuansanchez/b44d3d1f84800eb07e188958e99de9bc
- **Datos en español**: https://gist.github.com/josejuansanchez/122675071cdacce7f7ba61051707dae3

### Información de Conexión:
- **Host**: localhost
- **Puerto**: 3307
- **Base de datos**: sakila_es
- **Usuario**: root
- **Contraseña**: sakila_password

## 🔧 Troubleshooting

### Problema: Algunos servicios no arrancan

**Solución 1: Reintentar**
```bash
docker-compose up -d
```

**Solución 2: Revisar desde Docker Desktop**
1. Abre Docker Desktop
2. Ve a la pestaña "Containers"
3. Busca los contenedores parados
4. Haz clic en "Start" para levantarlos manualmente

**Solución 3: Revisar logs**
```bash
docker-compose logs -f nombre-del-servicio
```

### Problema: Los servicios siguen sin funcionar

**Limpieza completa de Docker** (empezar desde cero):
```bash
# Detener todos los servicios
docker-compose down

# Limpiar todo Docker
docker builder prune -af
docker container prune -f
docker network prune -f
docker volume prune -f

# Volver a ejecutar
docker-compose up -d
```

### Problema: Error de puertos ocupados

Si los puertos 8080, 5000 o 3307 están ocupados:
```bash
# Ver qué está usando los puertos
netstat -tulpn | grep :8080
netstat -tulpn | grep :5000
netstat -tulpn | grep :3307

# Detener el proceso o cambiar puertos en docker-compose.yml
```

### Problema: El modelo local no funciona

1. **Verifica que Docker Model Runner esté habilitado**
2. **Asegúrate de haber descargado** `ai/gpt-oss:latest`
3. **Revisa que el archivo .env** tenga `LLM_PROVIDER=docker_runner`

## 🏗️ Arquitectura del Proyecto

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Backend        │    │   Base de       │
│   (Node.js)     │◄──►│  (Python)       │◄──►│   Datos         │
│   Puerto: 8080  │    │  Puerto: 5000   │    │   (MySQL)       │
│                 │    │                 │    │   Puerto: 3307  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Modelo IA     │
                    │   (OpenAI/Local)│
                    └─────────────────┘
```

### Tecnologías Utilizadas:

**Frontend**:
- Node.js + Express
- HTML5 + CSS3 + JavaScript
- Interface web responsive

**Backend**:
- Python + FastAPI
- OpenAI API / Docker Model Runner
- Parsing inteligente de JSON

**Base de Datos**:
- MySQL 8.0
- Base de datos SAKILA en español
- Esquema optimizado con índices

**Infraestructura**:
- Docker + Docker Compose
- Contenedores aislados
- Variables de entorno seguras

## 📞 Soporte

Si tienes problemas:
1. **Revisa la sección de Troubleshooting** arriba
2. **Verifica que Docker Desktop** esté ejecutándose
3. **Comprueba los logs** con `docker-compose logs -f`
4. **Asegúrate de tener** la última versión de Docker Desktop

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo libremente para proyectos personales o comerciales.

---

⭐ **¡Dale una estrella si te gusta el proyecto!** ⭐