"""
AURAX Orchestrator - Coordinates RAG and LLM operations
"""

import logging
from typing import Dict, Any, Optional, List, Union
from .rag import retriever
from .llm import ollama_client
from .model_router import route_request, ModelType
from .models import qwen3_coder_adapter, stable_diffusion_adapter

logger = logging.getLogger(__name__)


class AuraxOrchestrator:
    """
    Orchestrates the RAG + LLM pipeline for AURAX
    """
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.retriever = retriever
        self.llm_client = ollama_client
        self.qwen3_adapter = qwen3_coder_adapter
        self.sd_adapter = stable_diffusion_adapter
    
    def _format_rag_prompt(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]],
        model_type: ModelType = ModelType.DEFAULT
    ) -> str:
        """
        Format the prompt for LLM with RAG context
        
        Args:
            query: Original user query
            context_docs: List of relevant documents from RAG
            model_type: Type of model to format prompt for
            
        Returns:
            Formatted prompt string
        """
        if not context_docs:
            # No context available - direct query
            if model_type == ModelType.CODE:
                return f"""You are an expert programmer. Please help with the following:

{query}

Provide clean, well-documented code with explanations."""
            else:
                return f"""Pergunta: {query}

Responda da melhor forma possível com base no seu conhecimento."""
        
        # Format context from retrieved documents
        context_text = ""
        for i, doc in enumerate(context_docs, 1):
            text = doc.get("text", "").strip()
            score = doc.get("score", 0)
            if text:
                context_text += f"\n{i}. (Relevância: {score:.2f}) {text}\n"
        
        # Create the formatted prompt based on model type
        if model_type == ModelType.CODE:
            prompt = f"""Relevant code documentation and context:
{context_text}

Coding request: {query}

Based on the provided context, write clean, efficient code that addresses the request. Include explanations and follow best practices. If the context doesn't contain enough information, use your programming knowledge and mention any assumptions."""
        else:
            prompt = f"""Contexto relevante encontrado:
{context_text}

Pergunta: {query}

Com base no contexto fornecido acima, responda à pergunta de forma clara e precisa. Se o contexto não for suficiente para responder completamente, use seu conhecimento geral, mas indique quando está fazendo isso."""
        
        return prompt
    
    async def generate_contextual_response(
        self,
        query: str,
        max_context_docs: int = 3,
        context_score_threshold: float = 0.5,
        model: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using multi-model RAG + LLM pipeline
        
        Args:
            query: User query text
            max_context_docs: Maximum number of context documents to retrieve
            context_score_threshold: Minimum similarity score for context docs
            model: Specific model to use (overrides routing)
            metadata: Additional metadata for routing decisions
            
        Returns:
            Dictionary with response, context, routing info, and metadata
        """
        try:
            # Step 1: Validate input
            if not query.strip():
                return {
                    "success": False,
                    "error": "Empty query provided",
                    "query": query,
                    "context": [],
                    "response": None
                }
            
            # Step 2: Route to appropriate model (unless specific model requested)
            if model:
                # Use specific model requested
                route_result = None
                model_type = ModelType.DEFAULT
                for mt in ModelType:
                    if mt.value == model:
                        model_type = mt
                        break
                logger.info(f"Using requested model: {model}")
            else:
                # Use intelligent routing
                route_result = route_request(query, metadata)
                model_type = route_result.model_type
                logger.info(f"Routed to {model_type.value} with confidence {route_result.confidence:.2f}")
            
            # Step 3: Handle image generation requests
            if model_type == ModelType.IMAGE:
                return await self._handle_image_generation(query, route_result)
            
            # Step 4: Retrieve relevant context using RAG (for text-based models)
            use_rag = model_type in [ModelType.DEFAULT, ModelType.CODE, ModelType.WEB_SEARCH]
            context_docs = []
            
            if use_rag:
                logger.info(f"Retrieving context for query: {query[:100]}...")
                # Adjust threshold for code queries
                threshold = context_score_threshold
                if model_type == ModelType.CODE:
                    threshold = min(threshold, 0.3)  # Lower threshold for code context
                
                context_docs = await self.retriever.search_relevant_context(
                    query_text=query,
                    top_k=max_context_docs,
                    score_threshold=threshold
                )
                logger.info(f"Retrieved {len(context_docs)} context documents")
            
            # Step 5: Generate response based on model type
            if model_type == ModelType.CODE:
                return await self._handle_code_generation(query, context_docs, route_result)
            else:
                return await self._handle_default_generation(query, context_docs, route_result, model)
                
        except Exception as e:
            logger.error(f"Error in generate_contextual_response: {e}")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}",
                "query": query,
                "context": [],
                "response": None
            }
    
    async def _handle_image_generation(
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

    async def _handle_code_generation(
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
                return await self._handle_default_generation(query, context_docs, route_result, None)
                
        except Exception as e:
            logger.error(f"Error in code generation: {e}")
            # Fallback to default model
            logger.info("Falling back to default model due to code generation error")
            return await self._handle_default_generation(query, context_docs, route_result, None)

    async def _handle_default_generation(
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
    
    async def add_knowledge(
        self, 
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of documents to add
            
        Returns:
            Dictionary with operation result
        """
        try:
            success = await self.retriever.add_documents_to_knowledge_base(documents)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully added {len(documents)} documents to knowledge base"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to add documents to knowledge base"
                }
                
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}"
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get status of all system components
        
        Returns:
            Dictionary with system status information
        """
        try:
            # Check LLM availability
            llm_available = await self.llm_client.is_available()
            
            # Get knowledge base info
            kb_info = await self.retriever.get_knowledge_base_info()
            
            # Get available models
            available_models = await self.llm_client.list_models()
            
            return {
                "success": True,
                "components": {
                    "llm": {
                        "available": llm_available,
                        "service": "Ollama",
                        "base_url": self.llm_client.base_url,
                        "default_model": self.llm_client.default_model,
                        "available_models": available_models
                    },
                    "rag": {
                        "available": kb_info is not None,
                        "knowledge_base": kb_info
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}"
            }


# Global orchestrator instance
orchestrator = AuraxOrchestrator()