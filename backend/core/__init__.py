"""
AURAX Core Module
"""

from .rag import qdrant_client, retriever
from .llm import ollama_client
from .orchestrator import orchestrator
from .web_scraper import scrape_and_update_knowledge_base, rag_updater
from .model_router import route_request, ModelRouter
from .models import qwen3_coder_adapter, stable_diffusion_adapter

__all__ = [
    "qdrant_client", 
    "retriever", 
    "ollama_client", 
    "orchestrator",
    "scrape_and_update_knowledge_base", 
    "rag_updater",
    "route_request",
    "ModelRouter",
    "qwen3_coder_adapter",
    "stable_diffusion_adapter"
]