"""
AURAX Backend - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import logging
from core.rag import retriever

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


class GenerateResponse(BaseModel):
    """Response model for generation endpoint"""
    query: str
    context: List[Dict[str, Any]]
    response: str
    tokens_used: int
    status: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    RAG-enhanced generation endpoint
    Retrieves relevant context from knowledge base before generating response
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        # Retrieve relevant context using RAG
        context_docs = await retriever.search_relevant_context(
            query_text=request.prompt,
            top_k=3,
            score_threshold=0.5
        )
        
        # For MVP, create a simple response incorporating context
        if context_docs:
            context_texts = [doc["text"][:200] + "..." for doc in context_docs]
            response_text = f"Based on relevant context, processing: {request.prompt[:100]}..."
        else:
            context_texts = []
            response_text = f"No relevant context found. Processing: {request.prompt[:100]}..."
        
        return GenerateResponse(
            query=request.prompt,
            context=[{"text": text, "score": doc.get("score", 0)} for text, doc in zip(context_texts, context_docs)],
            response=response_text,
            tokens_used=len(response_text.split()),
            status="success"
        )
        
    except Exception as e:
        logging.error(f"Error in generate endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AURAX API is running", "docs": "/docs"}


@app.get("/rag/info")
async def get_rag_info():
    """Get information about the RAG knowledge base"""
    try:
        info = await retriever.get_knowledge_base_info()
        if info:
            return {"status": "success", "knowledge_base": info}
        else:
            return {"status": "error", "message": "Could not retrieve knowledge base info"}
    except Exception as e:
        logging.error(f"Error getting RAG info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)