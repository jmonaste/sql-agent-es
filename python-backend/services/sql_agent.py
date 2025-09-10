import os
import logging
from typing import Dict, Any
from models.llm_client import LLMClient

logger = logging.getLogger(__name__)

class SQLAgent:
    def __init__(self):
        self.llm_client = LLMClient()
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'system-prompt.md')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("system-prompt.md not found, using basic prompt")
            return self._get_basic_system_prompt()
        except Exception as e:
            logger.error(f"Error loading system prompt: {e}")
            return self._get_basic_system_prompt()
    
    def _get_basic_system_prompt(self) -> str:
        """Basic fallback system prompt"""
        return """
Eres un especialista en SQL para la base de datos Sakila_es (sistema de videoclub en español).

Tu función es convertir consultas en lenguaje natural a SQL preciso y optimizado.

Base de datos: sakila_es
Principales tablas: actor, cliente, pelicula, alquiler, pago, inventario, categoria

Responde SOLO con la consulta SQL, sin explicaciones adicionales.
"""
    
    async def process_query(self, natural_language_query: str) -> Dict[str, Any]:
        """Process natural language query and return SQL"""
        try:
            if not natural_language_query or not natural_language_query.strip():
                return {
                    "success": False,
                    "error": "Query cannot be empty"
                }
            
            # Generate SQL using LLM
            result = await self.llm_client.generate_sql(
                user_query=natural_language_query,
                system_prompt=self.system_prompt
            )
            
            if result["success"]:
                sql_query = result["sql_query"]
                
                # Basic validation
                validation_result = self._validate_sql(sql_query)
                
                return {
                    "success": True,
                    "sql_query": sql_query,
                    "natural_query": natural_language_query,
                    "llm_info": {
                        "provider": result["provider"],
                        "model": result["model"]
                    },
                    "validation": validation_result
                }
            else:
                return {
                    "success": False,
                    "error": result["error"],
                    "natural_query": natural_language_query
                }
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}",
                "natural_query": natural_language_query
            }
    
    def _validate_sql(self, sql_query: str) -> Dict[str, Any]:
        """Basic SQL validation"""
        try:
            sql_lower = sql_query.lower().strip()
            
            # Check for dangerous operations
            dangerous_keywords = ['drop', 'delete', 'truncate', 'alter', 'create']
            has_dangerous = any(keyword in sql_lower for keyword in dangerous_keywords)
            
            # Check if it's a select query
            is_select = sql_lower.startswith('select')
            
            # Basic structure validation
            has_semicolon = sql_query.strip().endswith(';')
            
            return {
                "is_select": is_select,
                "has_dangerous_keywords": has_dangerous,
                "has_semicolon": has_semicolon,
                "is_valid": is_select and not has_dangerous,
                "warnings": self._get_validation_warnings(sql_lower)
            }
            
        except Exception as e:
            return {
                "is_valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
    def _get_validation_warnings(self, sql_lower: str) -> list:
        """Get validation warnings"""
        warnings = []
        
        if not sql_lower.startswith('select'):
            warnings.append("Solo se permiten consultas SELECT por seguridad")
            
        if 'drop' in sql_lower or 'delete' in sql_lower:
            warnings.append("Consulta contiene operaciones peligrosas")
            
        return warnings
    
    def test_connection(self) -> Dict[str, Any]:
        """Test LLM connection"""
        return self.llm_client.test_connection()
    
    def test_connection_fast(self) -> Dict[str, Any]:
        """Fast LLM connection test for health checks"""
        return self.llm_client.test_connection_fast()