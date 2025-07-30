"""
AURAX Backend - Main Application Entry Point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

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
    Temporary test endpoint for content generation
    TODO: Integrate with RAG and LLM models
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    # Placeholder response for MVP testing
    response_text = f"Processed: {request.prompt[:100]}..."
    
    return GenerateResponse(
        response=response_text,
        tokens_used=len(response_text.split()),
        status="success"
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AURAX API is running", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)