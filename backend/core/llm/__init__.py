"""
AURAX LLM (Large Language Model) Module
"""

from .ollama_client import ollama_client, OllamaClient

__all__ = [
    "ollama_client",
    "OllamaClient"
]