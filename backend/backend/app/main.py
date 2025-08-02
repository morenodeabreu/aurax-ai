from fastapi import FastAPI
from app.core import health
from app.api import generate

app = FastAPI(
    title="AURAX API",
    description="API para o sistema AURAX com RAG e LLMs",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Verificação de saúde do sistema"
        },
        {
            "name": "generate",
            "description": "Endpoint para gerar respostas com LLM"
        }
    ]
)

# Inclui os routers
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(generate.router, prefix="", tags=["generate"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao AURAX API"}
