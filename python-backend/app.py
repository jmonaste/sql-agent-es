from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
import uvicorn

from config import config
from services.sql_agent import SQLAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO if config.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SQL Agent API",
    description="Convert natural language queries to SQL for Sakila database",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQL Agent
sql_agent = SQLAgent()

# Request/Response models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    success: bool
    sql_query: str = None
    natural_query: str = None
    llm_info: Dict[str, Any] = None
    validation: Dict[str, Any] = None
    error: str = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SQL Agent API",
        "version": "1.0.0",
        "provider": config.LLM_PROVIDER
    }

@app.get("/health/basic")
async def basic_health_check():
    """Basic health check endpoint - only verifies FastAPI is running"""
    return {
        "status": "ok",
        "service": "SQL Agent API",
        "provider": config.LLM_PROVIDER
    }

@app.get("/health")
async def health_check():
    """Full health check endpoint - includes LLM connection test"""
    try:
        # Basic service status
        status = {
            "status": "ok",
            "service": "SQL Agent API",
            "provider": config.LLM_PROVIDER,
            "model": sql_agent.llm_client.model if sql_agent.llm_client else "unknown"
        }
        
        # Test LLM connection with timeout
        try:
            llm_test = sql_agent.test_connection_fast()
            status["llm_connection"] = llm_test["success"]
            
            if not llm_test["success"]:
                status["status"] = "degraded"
                status["llm_error"] = llm_test.get("error", "Unknown LLM error")
                
        except Exception as llm_error:
            logger.warning(f"LLM health check failed: {llm_error}")
            status["status"] = "degraded"
            status["llm_connection"] = False
            status["llm_error"] = str(llm_error)
        
        return status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/generate-sql", response_model=QueryResponse)
async def generate_sql(request: QueryRequest):
    """Generate SQL from natural language query"""
    try:
        logger.info(f"Processing query: {request.query[:100]}...")
        
        result = await sql_agent.process_query(request.query)
        
        if result["success"]:
            logger.info("SQL generation successful")
            return QueryResponse(**result)
        else:
            logger.warning(f"SQL generation failed: {result['error']}")
            raise HTTPException(
                status_code=400, 
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error"
        )

@app.get("/test-llm")
async def test_llm():
    """Test LLM connection endpoint"""
    return sql_agent.test_connection()

if __name__ == "__main__":
    try:
        # Validate configuration
        config.validate()
        logger.info(f"Starting SQL Agent API with {config.LLM_PROVIDER} provider")
        
        uvicorn.run(
            "app:app", 
            host="0.0.0.0", 
            port=config.PORT, 
            reload=config.DEBUG
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        exit(1)