from openai import OpenAI
from typing import Dict, Any
import logging
import json
import re
from config import config

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.client = None
        self.model = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client based on provider configuration"""
        try:
            if config.LLM_PROVIDER == "openai":
                self.client = OpenAI(api_key=config.OPENAI_API_KEY)
                self.model = config.OPENAI_MODEL
                logger.info("Initialized OpenAI client")
                
            elif config.LLM_PROVIDER == "docker_runner":
                self.client = OpenAI(
                    base_url=config.DOCKER_RUNNER_BASE_URL,
                    api_key="anything"  # Docker runner doesn't validate API key
                )
                self.model = config.DOCKER_RUNNER_MODEL
                logger.info("Initialized Docker Model Runner client")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise
    
    async def generate_sql(self, user_query: str, system_prompt: str) -> Dict[str, Any]:
        """Generate SQL query from natural language with structured JSON output"""
        try:
            # JSON Schema para salida estructurada
            sql_response_schema = {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The generated SQL query only, without formatting or markdown"
                    },
                    "explanation": {
                        "type": "string", 
                        "description": "Brief explanation of what the query does and how it works"
                    },
                    "considerations": {
                        "type": "string",
                        "description": "Performance considerations, indexes used, or optimization notes"
                    },
                    "alternatives": {
                        "type": "string",
                        "description": "Alternative approaches or variations of the query"
                    }
                },
                "required": ["sql_query", "explanation", "considerations", "alternatives"],
                "additionalProperties": False
            }
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            # Usar Structured Outputs si el modelo lo soporta
            if config.LLM_PROVIDER == "openai" and self.model in ["gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4o-mini-2024-07-18"]:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=1500,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "sql_response",
                            "schema": sql_response_schema,
                            "strict": True
                        }
                    }
                )
                
                # Parsear respuesta JSON estructurada
                content = response.choices[0].message.content
                sql_data = json.loads(content)
                
                return {
                    "success": True,
                    "sql_query": sql_data["sql_query"],
                    "explanation": sql_data["explanation"],
                    "considerations": sql_data["considerations"], 
                    "alternatives": sql_data["alternatives"],
                    "model": self.model,
                    "provider": config.LLM_PROVIDER,
                    "structured": True
                }
                
            else:
                # Fallback para modelos que no soportan structured outputs
                # Forzar formato JSON para modelos locales
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=1500,
                    response_format={"type": "json_object"} if config.LLM_PROVIDER == "docker_runner" else None
                )
                
                content = response.choices[0].message.content.strip()
                logger.info(f"Raw response from {config.LLM_PROVIDER}: {content[:200]}...")
                
                # Usar parsing robusto
                sql_data = self._robust_json_parse(content)
                
                if sql_data:
                    return {
                        "success": True,
                        "sql_query": sql_data.get("sql_query", ""),
                        "explanation": sql_data.get("explanation", ""),
                        "considerations": sql_data.get("considerations", ""),
                        "alternatives": sql_data.get("alternatives", ""),
                        "model": self.model,
                        "provider": config.LLM_PROVIDER,
                        "structured": False
                    }
                else:
                    # Último recurso: retornar como antes pero con logging
                    logger.error(f"Failed to parse JSON from {config.LLM_PROVIDER}: {content}")
                    return {
                        "success": True,
                        "sql_query": content,
                        "explanation": "",
                        "considerations": "",
                        "alternatives": "",
                        "model": self.model,
                        "provider": config.LLM_PROVIDER,
                        "structured": False
                    }
            
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model,
                "provider": config.LLM_PROVIDER
            }
    
    def _robust_json_parse(self, content: str) -> Dict[str, str]:
        """Parse JSON with multiple fallback strategies"""
        if not content:
            return None
            
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
            
        # Strategy 2: Clean and try again
        try:
            # Remove markdown code blocks if present
            cleaned = re.sub(r'```(?:json)?\s*', '', content)
            cleaned = re.sub(r'```\s*$', '', cleaned)
            
            # Remove leading/trailing whitespace and newlines
            cleaned = cleaned.strip()
            
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
            
        # Strategy 3: Extract JSON from text using regex
        try:
            # Find JSON object in the text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError):
            pass
            
        # Strategy 4: Try to extract individual fields if JSON structure is broken
        try:
            result = {}
            
            # Extract sql_query
            sql_match = re.search(r'["\']sql_query["\']\s*:\s*["\']([^"\']*)["\'"]', content, re.DOTALL)
            if sql_match:
                result["sql_query"] = sql_match.group(1)
                
            # Extract explanation
            exp_match = re.search(r'["\']explanation["\']\s*:\s*["\']([^"\']*)["\'"]', content, re.DOTALL)
            if exp_match:
                result["explanation"] = exp_match.group(1)
                
            # Extract considerations
            con_match = re.search(r'["\']considerations["\']\s*:\s*["\']([^"\']*)["\'"]', content, re.DOTALL)
            if con_match:
                result["considerations"] = con_match.group(1)
                
            # Extract alternatives
            alt_match = re.search(r'["\']alternatives["\']\s*:\s*["\']([^"\']*)["\'"]', content, re.DOTALL)
            if alt_match:
                result["alternatives"] = alt_match.group(1)
                
            # Return if we got at least sql_query
            if "sql_query" in result and result["sql_query"]:
                logger.warning(f"Used regex fallback parsing for {config.LLM_PROVIDER}")
                return result
                
        except Exception as e:
            logger.error(f"Regex parsing failed: {e}")
            
        # All strategies failed
        logger.error(f"All JSON parsing strategies failed for content: {content[:500]}...")
        return None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test LLM client connection - full test"""
        try:
            test_messages = [
                {"role": "user", "content": "Test connection. Respond with 'OK'"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=test_messages,
                max_tokens=10
            )
            
            return {
                "success": True,
                "provider": config.LLM_PROVIDER,
                "model": self.model,
                "response": response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "provider": config.LLM_PROVIDER,
                "model": self.model,
                "error": str(e)
            }
    
    def test_connection_fast(self) -> Dict[str, Any]:
        """Fast connection test for health checks"""
        try:
            # For OpenAI, just verify client is configured
            if config.LLM_PROVIDER == "openai":
                if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
                    return {
                        "success": False,
                        "provider": config.LLM_PROVIDER,
                        "model": self.model,
                        "error": "OpenAI API key not configured"
                    }
            
            # For Docker Runner, test if service is reachable
            elif config.LLM_PROVIDER == "docker_runner":
                import requests
                try:
                    # Quick ping to model runner health endpoint
                    response = requests.get(f"{config.DOCKER_RUNNER_BASE_URL.rstrip('/v1/')}/health", timeout=3)
                    if response.status_code != 200:
                        return {
                            "success": False,
                            "provider": config.LLM_PROVIDER,
                            "model": self.model,
                            "error": f"Docker Model Runner not healthy: {response.status_code}"
                        }
                except requests.exceptions.RequestException as e:
                    return {
                        "success": False,
                        "provider": config.LLM_PROVIDER,
                        "model": self.model,
                        "error": f"Docker Model Runner unreachable: {str(e)}"
                    }
            
            # If basic checks pass, return success
            return {
                "success": True,
                "provider": config.LLM_PROVIDER,
                "model": self.model,
                "test_type": "fast"
            }
            
        except Exception as e:
            return {
                "success": False,
                "provider": config.LLM_PROVIDER,
                "model": self.model,
                "error": str(e)
            }