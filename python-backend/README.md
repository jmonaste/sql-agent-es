# Python Backend - SQL Agent

Backend Python para convertir consultas en lenguaje natural a SQL usando OpenAI API o Docker Model Runner.

## Instalación

1. **Instalar dependencias:**
```bash
cd python-backend
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tu configuración
```

3. **Ejecutar localmente:**
```bash
python app.py
```

## Configuración

### OpenAI Provider
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-4
```

### Docker Model Runner
```env
LLM_PROVIDER=docker_runner
DOCKER_RUNNER_MODEL=ai/smollm2:latest
```

## Docker

### Solo backend Python (con OpenAI):
```bash
docker-compose up python-backend
```

### Con Docker Model Runner:
```bash
docker-compose --profile with-llm up
```

### Sistema completo:
```bash
docker-compose --profile full up
```

## API Endpoints

- `GET /` - Información básica
- `GET /health` - Health check
- `POST /generate-sql` - Generar SQL desde lenguaje natural
- `GET /test-llm` - Test conexión LLM

### Ejemplo de uso:
```bash
curl -X POST http://localhost:5000/generate-sql \
  -H "Content-Type: application/json" \
  -d '{"query": "Mostrar todas las películas de acción"}'
```