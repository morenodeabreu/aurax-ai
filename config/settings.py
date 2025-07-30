"""
AURAX Configuration Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings"""
    
    # API Configuration
    api_title: str = "AURAX API"
    api_version: str = "0.1.0"
    debug: bool = False
    
    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "aurax_knowledge_base"
    qdrant_vector_size: int = 384  # all-MiniLM-L6-v2 embedding size
    qdrant_distance_metric: str = "Cosine"
    
    # LLM Configuration
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "mistral:7b-instruct-q4_K_M"
    ollama_timeout: int = 120  # seconds
    max_tokens: int = 2000
    temperature: float = 0.7
    
    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour in seconds
    
    # CORS Configuration
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()