import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Provider
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Docker Model Runner Configuration
    DOCKER_RUNNER_BASE_URL = os.getenv(
        "DOCKER_RUNNER_BASE_URL", 
        "http://host.docker.internal:12434/engines/llama.cpp/v1/"
    )
    DOCKER_RUNNER_MODEL = os.getenv("DOCKER_RUNNER_MODEL", "ai/smollm2:latest")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        
        if cls.LLM_PROVIDER not in ["openai", "docker_runner"]:
            raise ValueError("LLM_PROVIDER must be either 'openai' or 'docker_runner'")

config = Config()