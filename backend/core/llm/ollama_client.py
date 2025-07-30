"""
Ollama Client for AURAX LLM Operations
"""

import httpx
import json
import logging
from typing import Optional, Dict, Any
from config.settings import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for interacting with Ollama API
    """
    
    def __init__(self):
        """Initialize Ollama client with settings configuration"""
        self.base_url = settings.ollama_base_url
        self.default_model = settings.default_model
        self.timeout = settings.ollama_timeout
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
    
    async def is_available(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            bool: True if Ollama is responding
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error checking Ollama availability: {e}")
            return False
    
    async def list_models(self) -> Optional[Dict[str, Any]]:
        """
        Get list of available models from Ollama
        
        Returns:
            Dictionary with available models or None if error
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Error listing models: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return None
    
    async def generate_response(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Optional[str]:
        """
        Generate response using Ollama model
        
        Args:
            prompt: The input prompt for generation
            model: Model name (uses default if None)
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Generated text response or None if error
        """
        if not prompt.strip():
            logger.warning("Empty prompt provided")
            return None
        
        # Use defaults if parameters not provided
        model_name = model or self.default_model
        max_tokens_val = max_tokens or self.max_tokens
        temperature_val = temperature or self.temperature
        
        request_data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens_val,
                "temperature": temperature_val,
                "stop": ["\n\n", "Human:", "Assistant:"]
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Generating response with model: {model_name}")
                
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "").strip()
                    
                    if generated_text:
                        logger.info(f"Successfully generated response ({len(generated_text)} chars)")
                        return generated_text
                    else:
                        logger.warning("Empty response generated")
                        return None
                else:
                    logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout generating response (>{self.timeout}s)")
            return None
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    async def generate_streaming_response(
        self, 
        prompt: str, 
        model: Optional[str] = None
    ):
        """
        Generate streaming response using Ollama model
        
        Args:
            prompt: The input prompt for generation
            model: Model name (uses default if None)
            
        Yields:
            Generated text chunks
        """
        if not prompt.strip():
            logger.warning("Empty prompt provided for streaming")
            return
        
        model_name = model or self.default_model
        
        request_data = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_predict": self.max_tokens,
                "temperature": self.temperature
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Starting streaming generation with model: {model_name}")
                
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status_code != 200:
                        logger.error(f"Streaming API error: {response.status_code}")
                        return
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                chunk = json.loads(line)
                                if "response" in chunk:
                                    yield chunk["response"]
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
    
    async def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model to Ollama
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            bool: True if model was pulled successfully
        """
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minutes timeout for download
                logger.info(f"Pulling model: {model_name}")
                
                response = await client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model_name},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully pulled model: {model_name}")
                    return True
                else:
                    logger.error(f"Error pulling model: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False


# Global Ollama client instance
ollama_client = OllamaClient()