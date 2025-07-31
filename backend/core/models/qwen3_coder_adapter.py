"""
Qwen3 Coder Adapter for AURAX
Specialized adapter for code generation and programming tasks
"""

import logging
from typing import Optional, Dict, Any
from ..llm.ollama_client import OllamaClient
from config.settings import settings

logger = logging.getLogger(__name__)


class Qwen3CoderAdapter:
    """
    Adapter for Qwen3 Coder model specialized in programming tasks
    """
    
    def __init__(self):
        """Initialize the Qwen3 Coder adapter"""
        self.ollama_client = OllamaClient()
        self.model_name = "qwen2.5-coder:7b"  # Updated to available model
        self.default_temperature = 0.3  # Lower temperature for more precise code
        self.default_max_tokens = 3000  # More tokens for code explanations
    
    async def is_model_available(self) -> bool:
        """
        Check if Qwen3 Coder model is available in Ollama
        
        Returns:
            bool: True if model is available
        """
        try:
            available_models = await self.ollama_client.list_models()
            if not available_models:
                return False
            
            # Check if our target model is in the list
            model_names = [model.get("name", "") for model in available_models.get("models", [])]
            return any(self.model_name in name for name in model_names)
            
        except Exception as e:
            logger.error(f"Error checking Qwen3 Coder availability: {e}")
            return False
    
    async def pull_model_if_needed(self) -> bool:
        """
        Pull the Qwen3 Coder model if it's not available
        
        Returns:
            bool: True if model is available after pulling
        """
        try:
            if await self.is_model_available():
                return True
            
            logger.info(f"Pulling {self.model_name} model...")
            success = await self.ollama_client.pull_model(self.model_name)
            
            if success:
                logger.info(f"Successfully pulled {self.model_name}")
                return True
            else:
                logger.error(f"Failed to pull {self.model_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error pulling Qwen3 Coder model: {e}")
            return False
    
    def _format_code_prompt(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Format prompt specifically for code generation tasks
        
        Args:
            prompt: Original user prompt
            context: Optional context from RAG
            
        Returns:
            Formatted prompt optimized for code generation
        """
        formatted_prompt = ""
        
        if context:
            formatted_prompt += f"Context and documentation:\n{context}\n\n"
        
        formatted_prompt += f"""You are an expert programmer and code assistant. Your task is to provide accurate, efficient, and well-documented code solutions.

User request: {prompt}

Please provide:
1. Clean, readable code that follows best practices
2. Clear explanations of your approach
3. Comments in the code where appropriate
4. If applicable, mention any dependencies or setup requirements

Response:"""
        
        return formatted_prompt
    
    async def generate_code_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Generate code-focused response using Qwen3 Coder
        
        Args:
            prompt: User prompt for code generation
            context: Optional context from RAG
            temperature: Generation temperature (default: 0.3)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated code response or None if error
        """
        try:
            # Ensure model is available
            if not await self.is_model_available():
                logger.warning("Qwen3 Coder not available, attempting to pull...")
                if not await self.pull_model_if_needed():
                    logger.error("Could not make Qwen3 Coder available")
                    return None
            
            # Format the prompt for code generation
            formatted_prompt = self._format_code_prompt(prompt, context)
            
            # Use specialized parameters for code generation
            response = await self.ollama_client.generate_response(
                prompt=formatted_prompt,
                model=self.model_name,
                temperature=temperature or self.default_temperature,
                max_tokens=max_tokens or self.default_max_tokens
            )
            
            if response:
                logger.info(f"Generated code response using {self.model_name}")
                return response
            else:
                logger.error("No response generated from Qwen3 Coder")
                return None
                
        except Exception as e:
            logger.error(f"Error generating code response: {e}")
            return None
    
    async def generate_streaming_code_response(
        self,
        prompt: str,
        context: Optional[str] = None
    ):
        """
        Generate streaming code response using Qwen3 Coder
        
        Args:
            prompt: User prompt for code generation
            context: Optional context from RAG
            
        Yields:
            Generated code chunks
        """
        try:
            # Ensure model is available
            if not await self.is_model_available():
                if not await self.pull_model_if_needed():
                    logger.error("Could not make Qwen3 Coder available for streaming")
                    return
            
            # Format the prompt for code generation
            formatted_prompt = self._format_code_prompt(prompt, context)
            
            # Generate streaming response
            async for chunk in self.ollama_client.generate_streaming_response(
                prompt=formatted_prompt,
                model=self.model_name
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error in streaming code generation: {e}")
    
    async def analyze_code(self, code: str, question: str) -> Optional[str]:
        """
        Analyze existing code and answer questions about it
        
        Args:
            code: Code to analyze
            question: Question about the code
            
        Returns:
            Analysis response or None if error
        """
        try:
            analysis_prompt = f"""You are an expert code reviewer and analyst. Analyze the following code and answer the question.

Code to analyze:
```
{code}
```

Question: {question}

Please provide a detailed analysis including:
1. Code functionality and purpose
2. Potential issues or improvements
3. Best practices recommendations
4. Answer to the specific question

Response:"""
            
            return await self.ollama_client.generate_response(
                prompt=analysis_prompt,
                model=self.model_name,
                temperature=0.2  # Very low temperature for analysis
            )
            
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            return None


# Global Qwen3 Coder adapter instance
qwen3_coder_adapter = Qwen3CoderAdapter()