"""
AURAX Orchestrator - Coordinates RAG and LLM operations
"""

import logging
from typing import Dict, Any, Optional, List
from .rag import retriever
from .llm import ollama_client

logger = logging.getLogger(__name__)


class AuraxOrchestrator:
    """
    Orchestrates the RAG + LLM pipeline for AURAX
    """
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.retriever = retriever
        self.llm_client = ollama_client
    
    def _format_rag_prompt(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]]
    ) -> str:
        """
        Format the prompt for LLM with RAG context
        
        Args:
            query: Original user query
            context_docs: List of relevant documents from RAG
            
        Returns:
            Formatted prompt string
        """
        if not context_docs:
            # No context available - direct query
            return f"""Pergunta: {query}

Responda da melhor forma possível com base no seu conhecimento."""
        
        # Format context from retrieved documents
        context_text = ""
        for i, doc in enumerate(context_docs, 1):
            text = doc.get("text", "").strip()
            score = doc.get("score", 0)
            if text:
                context_text += f"\n{i}. (Relevância: {score:.2f}) {text}\n"
        
        # Create the formatted prompt
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
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using RAG + LLM pipeline
        
        Args:
            query: User query text
            max_context_docs: Maximum number of context documents to retrieve
            context_score_threshold: Minimum similarity score for context docs
            model: LLM model to use (optional)
            
        Returns:
            Dictionary with response, context, and metadata
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
            
            # Step 2: Retrieve relevant context using RAG
            logger.info(f"Retrieving context for query: {query[:100]}...")
            context_docs = await self.retriever.search_relevant_context(
                query_text=query,
                top_k=max_context_docs,
                score_threshold=context_score_threshold
            )
            
            logger.info(f"Retrieved {len(context_docs)} context documents")
            
            # Step 3: Format prompt with context
            formatted_prompt = self._format_rag_prompt(query, context_docs)
            
            # Step 4: Check LLM availability
            llm_available = await self.llm_client.is_available()
            if not llm_available:
                return {
                    "success": False,
                    "error": "LLM service (Ollama) not available",
                    "query": query,
                    "context": context_docs,
                    "response": None
                }
            
            # Step 5: Generate response using LLM
            logger.info("Generating response with LLM...")
            llm_response = await self.llm_client.generate_response(
                prompt=formatted_prompt,
                model=model
            )
            
            if llm_response is None:
                return {
                    "success": False,
                    "error": "Failed to generate response from LLM",
                    "query": query,
                    "context": context_docs,
                    "response": None
                }
            
            # Step 6: Return successful response
            return {
                "success": True,
                "query": query,
                "context": context_docs,
                "response": llm_response,
                "metadata": {
                    "context_docs_count": len(context_docs),
                    "model_used": model or self.llm_client.default_model,
                    "prompt_length": len(formatted_prompt)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in generate_contextual_response: {e}")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}",
                "query": query,
                "context": [],
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