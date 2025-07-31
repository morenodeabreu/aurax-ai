"""
Intelligent Model Router for AURAX Multi-Model System
"""

import re
import logging
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ModelType(str, Enum):
    """Supported model types in AURAX"""
    DEFAULT = "default"  # Mistral 7B for general tasks
    CODE = "qwen3:coder"  # Qwen3 Coder for programming tasks
    IMAGE = "stable-diffusion"  # Stable Diffusion for image generation
    WEB_SEARCH = "web-enhanced"  # Enhanced with fresh web content


class RouteResult(BaseModel):
    """Result of model routing decision"""
    model_type: ModelType
    confidence: float  # 0.0 to 1.0
    reasoning: str
    suggested_parameters: Dict[str, Any]


class ModelRouter:
    """
    Intelligent router to determine the best model for a given request
    """
    
    def __init__(self):
        """Initialize the model router with classification patterns"""
        self._code_patterns = [
            # Programming languages
            r'\b(python|javascript|java|c\+\+|rust|go|typescript|php|ruby|swift|kotlin)\b',
            # Code-related keywords
            r'\b(function|class|method|variable|algorithm|code|script|program|debug|bug|error|exception)\b',
            # Development terms
            r'\b(api|database|framework|library|package|module|import|export|compile|deploy)\b',
            # Code artifacts
            r'\b(if|else|for|while|return|def|var|let|const|public|private|static)\b',
            # File extensions
            r'\.(py|js|java|cpp|rs|go|ts|php|rb|swift|kt|html|css|sql)\b',
            # Development activities
            r'\b(implement|code|program|develop|build|create.*(function|class|method|api))\b',
            r'\b(fix.*(bug|error)|debug|refactor|optimize.*(code|algorithm))\b'
        ]
        
        self._image_patterns = [
            # Image generation requests
            r'\b(generate|create|make|draw|design|produce).*(image|picture|photo|illustration|artwork|graphic)\b',
            r'\b(image|picture|photo|illustration|artwork|graphic|drawing|painting|sketch).*(of|showing|depicting)\b',
            # Visual content
            r'\b(visualize|visual|graphic|art|artistic|creative|aesthetic)\b',
            # Specific image requests
            r'\b(logo|icon|banner|poster|diagram|chart|infographic)\b',
            # Art styles
            r'\b(realistic|cartoon|anime|abstract|minimalist|vintage|modern)\b',
            # Image actions
            r'\b(draw|paint|sketch|render|design|illustrate)\b'
        ]
        
        self._web_search_patterns = [
            # Current information requests
            r'\b(latest|recent|current|new|today|this (week|month|year)|2024|2025)\b',
            r'\b(news|updates|trends|developments|happenings)\b',
            # Real-time information
            r'\b(what.*(happening|going on)|current (status|situation|state))\b',
            r'\b(price|stock|market|weather|score|result)\b',
            # Information that changes frequently
            r'\b(events|schedule|calendar|availability|status)\b'
        ]
    
    def _analyze_code_intent(self, prompt: str) -> float:
        """
        Analyze if the prompt is related to programming/coding
        
        Args:
            prompt: User prompt to analyze
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        prompt_lower = prompt.lower()
        matches = 0
        total_patterns = len(self._code_patterns)
        
        for pattern in self._code_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                matches += 1
        
        confidence = min(matches / total_patterns * 2.0, 1.0)  # Scale to max 1.0
        
        # Boost confidence for explicit code requests
        if re.search(r'\b(write|create|implement|build).*(code|function|class|script)\b', prompt_lower):
            confidence = min(confidence + 0.3, 1.0)
        
        return confidence
    
    def _analyze_image_intent(self, prompt: str) -> float:
        """
        Analyze if the prompt is requesting image generation
        
        Args:
            prompt: User prompt to analyze
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        prompt_lower = prompt.lower()
        matches = 0
        total_patterns = len(self._image_patterns)
        
        for pattern in self._image_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                matches += 1
        
        confidence = min(matches / total_patterns * 3.0, 1.0)  # Scale to max 1.0
        
        # Boost confidence for explicit image requests
        if re.search(r'\b(generate|create|make|draw).*(image|picture|photo)\b', prompt_lower):
            confidence = min(confidence + 0.4, 1.0)
        
        return confidence
    
    def _analyze_web_search_intent(self, prompt: str) -> float:
        """
        Analyze if the prompt requires current/fresh information
        
        Args:
            prompt: User prompt to analyze
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        prompt_lower = prompt.lower()
        matches = 0
        total_patterns = len(self._web_search_patterns)
        
        for pattern in self._web_search_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                matches += 1
        
        confidence = min(matches / total_patterns * 2.5, 1.0)  # Scale to max 1.0
        
        return confidence
    
    def _get_model_parameters(self, model_type: ModelType, prompt: str) -> Dict[str, Any]:
        """
        Get suggested parameters for the selected model
        
        Args:
            model_type: Selected model type
            prompt: User prompt
            
        Returns:
            Dictionary with suggested parameters
        """
        base_params = {
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if model_type == ModelType.CODE:
            # More precise for code generation
            base_params.update({
                "temperature": 0.3,
                "max_tokens": 3000,
                "top_p": 0.9
            })
        elif model_type == ModelType.IMAGE:
            # Image generation parameters
            base_params.update({
                "steps": 30,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            })
        elif model_type == ModelType.WEB_SEARCH:
            # Enhanced context retrieval
            base_params.update({
                "temperature": 0.6,
                "use_fresh_data": True,
                "context_threshold": 0.3  # Lower threshold for more context
            })
        
        return base_params
    
    def route_request(
        self, 
        prompt: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> RouteResult:
        """
        Route a request to the most appropriate model
        
        Args:
            prompt: User prompt/request
            metadata: Optional metadata that might influence routing
            
        Returns:
            RouteResult with model selection and reasoning
        """
        try:
            if not prompt or not prompt.strip():
                return RouteResult(
                    model_type=ModelType.DEFAULT,
                    confidence=1.0,
                    reasoning="Empty prompt, using default model",
                    suggested_parameters=self._get_model_parameters(ModelType.DEFAULT, prompt)
                )
            
            # Check if model is explicitly specified in metadata
            if metadata and "preferred_model" in metadata:
                preferred = metadata["preferred_model"]
                if preferred in [e.value for e in ModelType]:
                    return RouteResult(
                        model_type=ModelType(preferred),
                        confidence=1.0,
                        reasoning=f"Explicitly requested model: {preferred}",
                        suggested_parameters=self._get_model_parameters(ModelType(preferred), prompt)
                    )
            
            # Analyze intent with different model types
            code_confidence = self._analyze_code_intent(prompt)
            image_confidence = self._analyze_image_intent(prompt)
            web_confidence = self._analyze_web_search_intent(prompt)
            
            # Determine the best model based on confidence scores
            confidences = [
                (ModelType.CODE, code_confidence, "Code-related keywords and patterns detected"),
                (ModelType.IMAGE, image_confidence, "Image generation request detected"),
                (ModelType.WEB_SEARCH, web_confidence, "Current information request detected"),
                (ModelType.DEFAULT, 0.5, "General query, using default model")  # Fallback
            ]
            
            # Sort by confidence and select the highest
            confidences.sort(key=lambda x: x[1], reverse=True)
            selected_model, confidence, reasoning = confidences[0]
            
            # Apply minimum confidence threshold
            if confidence < 0.4 and selected_model != ModelType.DEFAULT:
                selected_model = ModelType.DEFAULT
                confidence = 0.5
                reasoning = "Low confidence in specialized model, defaulting to general model"
            
            logger.info(f"Routed prompt to {selected_model.value} with confidence {confidence:.2f}")
            
            return RouteResult(
                model_type=selected_model,
                confidence=confidence,
                reasoning=reasoning,
                suggested_parameters=self._get_model_parameters(selected_model, prompt)
            )
            
        except Exception as e:
            logger.error(f"Error in model routing: {e}")
            return RouteResult(
                model_type=ModelType.DEFAULT,
                confidence=0.5,
                reasoning=f"Error in routing, defaulting to general model: {str(e)}",
                suggested_parameters=self._get_model_parameters(ModelType.DEFAULT, prompt)
            )


# Global router instance
model_router = ModelRouter()


# Convenience function for direct usage
def route_request(
    prompt: str, 
    metadata: Optional[Dict[str, Any]] = None
) -> RouteResult:
    """
    Convenience function to route a request to the appropriate model
    
    Args:
        prompt: User prompt/request
        metadata: Optional metadata for routing
        
    Returns:
        RouteResult with model selection and reasoning
    """
    return model_router.route_request(prompt, metadata)