## Próximo Sprint
Ahora procederemos a crear el backend minimalista de python.
La idea es que la consulta escrita en lenguaje natural en el frontend de node.js se envía a la api del backend de python. el backend de python recibe el texto en lenguaje natural, ejecuta la consulta al LLM

La idea es que podamos usar la api de openAI o bien el docker desktop runner según la configuración del entorno, que podamos configurar en el docker desktop.yml

El frontend luego recibirá la consulta SQL para ser ejecutada, y mostrará los resultados por pantalla.

El agente que recibe la consulta en lenguaje natural y devuelve la query la podemos implementar en langchain o langraph, según sea más optimo.



## Documentacion que deberás leer
Documentacion de api de openAI: https://platform.openai.com/docs/guides/text
quickstart: https://platform.openai.com/docs/quickstart
Structured model outputs: https://platform.openai.com/docs/guides/structured-outputs
Docker Model Runner: https://docs.docker.com/ai/model-runner/
Documentacion oficial de langraph: https://langchain-ai.github.io/langgraph/concepts/why-langgraph/


## Informacion sobre el Docker Desktop Runner
Docker Model Runner

Para correr modelos LLM en local. Por ejemplo Ollama. Es compatible con el compliance de la OpenAI API.

**API compatible con OpenAI (“OpenAI-compatible API”)**

Esto se refiere a cualquier API —propia, de otro proveedor o self-hosted— que sigue el mismo esquema de **solicitudes/respuestas** (endpoints, autenticación) que la API oficial de OpenAI. La ventaja es que puedes intercambiar fácilmente el proveedor (o modelo) sin reescribir tu código cliente [BentoML](https://bentoml.com/llm/llm-inference-basics/openai-compatible-api?utm_source=chatgpt.com).

¿Por qué es útil?

- Evita el lock-in tecnológico: puedes cambiar entre OpenAI, modelos auto-hospedados o de otros proveedores sin modificar tu aplicación.
- Muchas infraestructuras y herramientas ya están diseñadas para trabajar con esa interfaz estándar.

Frameworks y servidores como **vLLM**, **BentoML**, **Together**, o incluso servicios como **Cloudflare Workers AI**, ofrecen endpoints compatibles con los de OpenAI (`/v1/chat/completions`, `/v1/embeddings`, etc.)

Como estamos usando Docker, no tenemos que instalar CUDA, ni drivers, lo usamos directamente. Podemos hacer un pull directamente del DockerHub. En esta parte veremos con usar el Docker Model Runner.

¿Qué necesitamos?

- Docker Desktop Instalado.
    
    Nos vamos a pestaña de Settings/Beta features/Enable Docker Model Runner
    
    Enable host-side TCP support (puerto 12343) —> Necesario si lo queremos usar desde nuestro código de Python
    
- Una vez habilitado el Docker Model Runner, veremos a opción de ‘Models (beta)’ en el menú lateral de Docker
    - Aquí podremos ver las opciones de ‘Local’, ‘Docker Hub’, ‘Logs’.
    - En Docker Hub podemos hacer un pull de algunos modelos. Veremos varias opciones.
    - También podemos hacer pull desde HugingFace.
    - Podemos ejecutar el modelo directamente y se abre una interfaz en DockerDesktop
    - También podemo ejecutarlo desde la terminal
        
        ```python
        docker model # para ver qué comandos hay
        
        docker model pull <MODEL_NAME> # para descargar un modelo
        
        docker model list # lista los modelos que tenems
        
        docker model run ai/gemma3 # ejecuta en consola el modelo seleccionado
        ```
        
        También podemos hacer un push de algún modelo nuestro.
        
    
    Nota IMPORTANTE:
    
    > Los modelos de Docker no se ejecutan en contenedores, se ejecutan en la máquina host, es decir, en nuestro PC, no en un contendero. ¿Por qué? para aprovechar al máximo los recursos.
    > 
    
    En cualquier caso, las diferencias por ejemplo entre Ollama y Docker Runner son las siguientes:
    
    | **Característica** | **DOCKER MODEL RUNNER** | **OLLAMA** |
    | --- | --- | --- |
    | **1. Arquitectura** | ▸ El modelo se ejecuta en el host, no en el contenedor | ▸ El modelo se ejecuta dentro de un servicio gestionado por Ollama (vía contenedor o binario) |
    | **2. Integración** | ▸ Se integra sin problemas con Docker Desktop, Compose, etc. | ▸ Aplicación independiente con CLI y API básica |
    | **3. Acceso a la API** | ▸ Endpoint compatible con OpenAI: `http://localhost:12434` | ▸ Endpoint compatible con OpenAI: `http://localhost:11434` |
    | **4. Encaje en el ecosistema** | ▸ Nativo del ecosistema Docker, funciona con Compose + Prometheus + Grafana | ▸ Autocontenido pero menos personalizable |
    
    Para usar el Model Runner desde el código,  podemos hacer lo siguiente:
    
    ```python
    from openai import OpenAI
    import os
    
    # Configuration for local Docker Model Runner
    BASE_URL = "http://localhost:12434/engines/llama.cpp/v1/"
    
    # Instantiate the OpenAI client
    client = OpenAI(base_url=BASE_URL, api_key="anything")
    
    # Define the model and prompt
    MODEL_NAME = "ai/smoiln2:latest"  # or "llama3:8b-instruct" depending on the model you've pulled
    PROMPT = "Explain how transformers work."
    
    # Prepare the chat messages
    messages = [
        {"role": "user", "content": PROMPT}
    ]
    ```
    
    La línea importante es:
    
    ```python
    # Configuration for local Docker Model Runner
    BASE_URL = "http://localhost:12434/engines/llama.cpp/v1/"
    ```
    
    Ya que es la que apunta al modelo local. Pero, si queremos acceder DESDE un contenedor, tenemos que cambiar esto:
    
    ```python
    # Configuration for local Docker Model Runner para ser accedido desde un contenedor
    BASE_URL = "http://local.docker.internal:12434/engines/llama.cpp/v1/"
    MODEL=ai/smollm2:latest
    ```
    
    Ya hemos explicado que esto es así porque el model, en el Docker Model Runner se ejecuta en la máquina host, no en un contendor. ‘local.docker.internal’ Docker sabe que tiene que ir al host, en lugar de buscar alguna instancia de una aplicación contenerizada.
    
    El docker-compose.yml se puede ver así:
    
    ```docker
    services:
      app:
        build: ./app
        env_file: 'backend.env'
        ports:
          - "8501:8501"
        depends_on:
          - llm
    
      llm:
        provider:
          type: model
          options:
            model: ${LM_MODEL_NAME:-ai/smo11m2:latest}
    ```
    
    El servicio depende del LLM, por eso ponemos la dependencia. La razón de esto es que vamos a necesitar comunicarcos con el Docker Desktop Runner (DDR) y tenemos que decirle a la app que vamos a usar el LLM. Luego, simplemente especificamos el servicio LLM. El modelo puede venir de un .env o ponerlo manualmente.