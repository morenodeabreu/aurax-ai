from fastapi import FastAPI
from app.core import health

app = FastAPI(
    title="AURAX API",
    description="API para o sistema AURAX com RAG e LLMs",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Verificação de saúde do sistema"
        }
    ]
)

# Inclui os routers
app.include_router(health.router, prefix="", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao AURAX API"}
