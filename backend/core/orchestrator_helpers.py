"""
Helper methods for AuraxOrchestrator - Multi-model handling
"""

import logging
from typing import Dict, Any, Optional, List, Union
from .model_router import ModelType

logger = logging.getLogger(__name__)


async def handle_image_generation(
    self, 
    query: str, 
    route_result: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Handle image generation requests
    
    Args:
        query: User query for image generation
        route_result: Routing decision result
        
    Returns:
        Dictionary with image generation result
    """
    try:
        logger.info(f"Generating image for query: {query[:100]}...")
        
        # Extract parameters from route result if available
        params = route_result.suggested_parameters if route_result else {}
        
        # Generate image
        image_result = await self.sd_adapter.generate_image(
            prompt=query,
            width=params.get("width", 512),
            height=params.get("height", 512),
            steps=params.get("steps", 30),
            guidance_scale=params.get("guidance_scale", 7.5)
        )
        
        if image_result:
            return {
                "success": True,
                "query": query,
                "context": [],
                "response": image_result,
                "response_type": "image",
                "metadata": {
                    "model_used": "stable-diffusion",
                    "routing": route_result.__dict__ if route_result else None,
                    "generation_params": image_result
                }
            }
        else:
            return {
                "success": False,
                "error": "Failed to generate image",
                "query": query,
                "context": [],
                "response": None
            }
            
    except Exception as e:
        logger.error(f"Error in image generation: {e}")
        return {
            "success": False,
            "error": f"Image generation error: {str(e)}",
            "query": query,
            "context": [],
            "response": None
        }


async def handle_code_generation(
    self, 
    query: str, 
    context_docs: List[Dict[str, Any]], 
    route_result: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Handle code generation requests
    
    Args:
        query: User query for code generation
        context_docs: Retrieved context documents
        route_result: Routing decision result
        
    Returns:
        Dictionary with code generation result
    """
    try:
        logger.info("Generating code response...")
        
        # Format context for code generation
        context_text = ""
        if context_docs:
            context_texts = [doc.get("text", "") for doc in context_docs]
            context_text = "\n\n".join(context_texts)
        
        # Generate code response
        code_response = await self.qwen3_adapter.generate_code_response(
            prompt=query,
            context=context_text if context_text else None,
            temperature=route_result.suggested_parameters.get("temperature", 0.3) if route_result else 0.3
        )
        
        if code_response:
            return {
                "success": True,
                "query": query,
                "context": context_docs,
                "response": code_response,
                "response_type": "code",
                "metadata": {
                    "model_used": "qwen3:coder",
                    "context_docs_count": len(context_docs),
                    "routing": route_result.__dict__ if route_result else None
                }
            }
        else:
            # Fallback to default model if Qwen3 fails
            logger.warning("Qwen3 Coder failed, falling back to default model")
            return await handle_default_generation(self, query, context_docs, route_result, None)
            
    except Exception as e:
        logger.error(f"Error in code generation: {e}")
        # Fallback to default model
        logger.info("Falling back to default model due to code generation error")
        return await handle_default_generation(self, query, context_docs, route_result, None)


async def handle_default_generation(
    self, 
    query: str, 
    context_docs: List[Dict[str, Any]], 
    route_result: Optional[Any] = None,
    specific_model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Handle default text generation requests
    
    Args:
        query: User query
        context_docs: Retrieved context documents
        route_result: Routing decision result
        specific_model: Specific model to use
        
    Returns:
        Dictionary with generation result
    """
    try:
        # Determine model type for prompt formatting
        model_type = route_result.model_type if route_result else ModelType.DEFAULT
        
        # Format prompt with context
        formatted_prompt = self._format_rag_prompt(query, context_docs, model_type)
        
        # Check LLM availability
        llm_available = await self.llm_client.is_available()
        if not llm_available:
            return {
                "success": False,
                "error": "LLM service (Ollama) not available",
                "query": query,
                "context": context_docs,
                "response": None
            }
        
        # Generate response using default LLM
        logger.info("Generating response with default LLM...")
        llm_response = await self.llm_client.generate_response(
            prompt=formatted_prompt,
            model=specific_model
        )
        
        if llm_response is None:
            return {
                "success": False,
                "error": "Failed to generate response from LLM",
                "query": query,
                "context": context_docs,
                "response": None
            }
        
        # Return successful response
        return {
            "success": True,
            "query": query,
            "context": context_docs,
            "response": llm_response,
            "response_type": "text",
            "metadata": {
                "context_docs_count": len(context_docs),
                "model_used": specific_model or self.llm_client.default_model,
                "prompt_length": len(formatted_prompt),
                "routing": route_result.__dict__ if route_result else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error in default generation: {e}")
        return {
            "success": False,
            "error": f"Generation error: {str(e)}",
            "query": query,
            "context": context_docs,
            "response": None
        }