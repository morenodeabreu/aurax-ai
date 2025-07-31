"""
AURAX Backend - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import logging
from core.orchestrator import orchestrator
from core.web_scraper import scrape_and_update_knowledge_base, rag_updater

app = FastAPI(
    title="AURAX API",
    description="Sistema autônomo de IA para geração de aplicações completas",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configurar origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    """Request model for generation endpoint"""
    prompt: str
    max_tokens: Optional[int] = 1000
    model: Optional[str] = None
    context_threshold: Optional[float] = 0.5


class ScrapeRequest(BaseModel):
    """Request model for scraping endpoint"""
    url: str
    metadata: Optional[Dict[str, Any]] = None


class BatchScrapeRequest(BaseModel):
    """Request model for batch scraping endpoint"""
    urls: List[str]
    metadata: Optional[Dict[str, Any]] = None


class GenerateResponse(BaseModel):
    """Response model for generation endpoint"""
    success: bool
    query: str
    context: List[Dict[str, Any]]
    response: Optional[str]
    metadata: Optional[Dict[str, Any]]
    error: Optional[str] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    RAG-enhanced generation endpoint with LLM integration
    Retrieves relevant context and generates contextual responses using LLM
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Use orchestrator for RAG + LLM pipeline
        result = await orchestrator.generate_contextual_response(
            query=request.prompt,
            max_context_docs=3,
            context_score_threshold=request.context_threshold or 0.5,
            model=request.model
        )
        
        if not result["success"]:
            # Return error response but don't raise HTTP exception
            return GenerateResponse(
                success=False,
                query=request.prompt,
                context=result.get("context", []),
                response=None,
                metadata=None,
                error=result.get("error", "Unknown error")
            )
        
        return GenerateResponse(
            success=True,
            query=result["query"],
            context=result["context"],
            response=result["response"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        logging.error(f"Error in generate endpoint: {e}")
        return GenerateResponse(
            success=False,
            query=request.prompt,
            context=[],
            response=None,
            metadata=None,
            error="Internal server error"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AURAX API is running", 
        "version": "0.1.0",
        "features": ["RAG", "LLM Integration", "Knowledge Base", "Web Scraping"],
        "docs": "/docs"
    }


@app.get("/system/status")
async def get_system_status():
    """Get comprehensive system status including LLM and RAG components"""
    try:
        status = await orchestrator.get_system_status()
        return status
    except Exception as e:
        logging.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/rag/info")
async def get_rag_info():
    """Get information about the RAG knowledge base (legacy endpoint)"""
    try:
        status = await orchestrator.get_system_status()
        if status["success"]:
            return {
                "status": "success", 
                "knowledge_base": status["components"]["rag"]["knowledge_base"]
            }
        else:
            return {"status": "error", "message": "Could not retrieve system status"}
    except Exception as e:
        logging.error(f"Error getting RAG info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/knowledge/add")
async def add_knowledge(documents: List[Dict[str, Any]]):
    """Add documents to the knowledge base"""
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        result = await orchestrator.add_knowledge(documents)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    """Scrape a URL and add content to the knowledge base"""
    try:
        if not request.url.strip():
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        # Validate URL format
        if not (request.url.startswith('http://') or request.url.startswith('https://')):
            raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
        
        # Perform scraping and RAG update
        result = await scrape_and_update_knowledge_base(request.url, request.metadata)
        
        if result["success"]:
            return result
        else:
            return {
                "success": False,
                "url": request.url,
                "error": result.get("error", "Unknown error"),
                "timestamp": result.get("timestamp")
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in scrape endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/scrape/batch")
async def scrape_batch_urls(request: BatchScrapeRequest):
    """Scrape multiple URLs and add content to the knowledge base"""
    try:
        if not request.urls:
            raise HTTPException(status_code=400, detail="No URLs provided")
        
        if len(request.urls) > 10:  # Limit batch size for safety
            raise HTTPException(status_code=400, detail="Maximum 10 URLs per batch")
        
        # Validate URLs
        for url in request.urls:
            if not url.strip():
                raise HTTPException(status_code=400, detail="Empty URL found in batch")
            if not (url.startswith('http://') or url.startswith('https://')):
                raise HTTPException(status_code=400, detail=f"Invalid URL format: {url}")
        
        # Perform batch scraping
        result = await rag_updater.scrape_multiple_urls(request.urls, request.metadata)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in batch scrape endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/scrape/stats")
async def get_scraping_stats():
    """Get statistics about scraped content in the knowledge base"""
    try:
        stats = await rag_updater.get_scraping_statistics()
        return stats
    except Exception as e:
        logging.error(f"Error getting scraping stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)