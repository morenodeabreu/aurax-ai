"""
Stable Diffusion Adapter for AURAX
Specialized adapter for image generation tasks
"""

import logging
import io
import base64
from typing import Optional, Dict, Any, Union
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
from config.settings import settings

logger = logging.getLogger(__name__)


class StableDiffusionAdapter:
    """
    Adapter for Stable Diffusion model specialized in image generation
    """
    
    def __init__(self):
        """Initialize the Stable Diffusion adapter"""
        self.pipeline = None
        self.model_id = "runwayml/stable-diffusion-v1-5"  # Default model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.default_steps = 30
        self.default_guidance_scale = 7.5
        self.default_width = 512
        self.default_height = 512
        self.is_loaded = False
    
    async def load_model(self) -> bool:
        """
        Load the Stable Diffusion model
        
        Returns:
            bool: True if model loaded successfully
        """
        try:
            if self.is_loaded and self.pipeline is not None:
                return True
            
            logger.info(f"Loading Stable Diffusion model: {self.model_id}")
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,  # Disable for faster inference
                requires_safety_checker=False
            )
            
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(self.pipeline, 'enable_attention_slicing'):
                self.pipeline.enable_attention_slicing()
            
            # Enable CPU offload if using CUDA
            if self.device == "cuda" and hasattr(self.pipeline, 'enable_sequential_cpu_offload'):
                self.pipeline.enable_sequential_cpu_offload()
            
            self.is_loaded = True
            logger.info(f"Stable Diffusion model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading Stable Diffusion model: {e}")
            self.is_loaded = False
            return False
    
    def _preprocess_prompt(self, prompt: str) -> str:
        """
        Preprocess and enhance the prompt for better image generation
        
        Args:
            prompt: Original user prompt
            
        Returns:
            Enhanced prompt
        """
        # Add quality enhancers for better results
        quality_enhancers = [
            "high quality",
            "detailed",
            "sharp focus",
            "professional"
        ]
        
        enhanced_prompt = prompt
        
        # Add quality enhancers if not already present
        for enhancer in quality_enhancers:
            if enhancer.lower() not in prompt.lower():
                enhanced_prompt += f", {enhancer}"
        
        return enhanced_prompt
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64 encoded image string
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_base64
    
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        seed: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate an image from text prompt
        
        Args:
            prompt: Text description of desired image
            negative_prompt: Things to avoid in the image
            width: Image width (default: 512)
            height: Image height (default: 512)
            steps: Number of inference steps (default: 30)
            guidance_scale: How closely to follow the prompt (default: 7.5)
            seed: Random seed for reproducibility
            
        Returns:
            Dictionary with image data and metadata, or None if error
        """
        try:
            # Load model if not already loaded
            if not self.is_loaded:
                if not await self.load_model():
                    return None
            
            if self.pipeline is None:
                logger.error("Pipeline not available")
                return None
            
            # Use defaults if parameters not provided
            width = width or self.default_width
            height = height or self.default_height
            steps = steps or self.default_steps
            guidance_scale = guidance_scale or self.default_guidance_scale
            
            # Preprocess prompt for better results
            enhanced_prompt = self._preprocess_prompt(prompt)
            
            # Set default negative prompt if not provided
            if negative_prompt is None:
                negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy"
            
            logger.info(f"Generating image with prompt: {enhanced_prompt[:100]}...")
            
            # Set seed for reproducibility if provided
            if seed is not None:
                torch.manual_seed(seed)
            
            # Generate image
            with torch.autocast(self.device):
                result = self.pipeline(
                    prompt=enhanced_prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    num_images_per_prompt=1
                )
            
            # Get the generated image
            image = result.images[0]
            
            # Convert to base64 for API response
            image_base64 = self._image_to_base64(image)
            
            logger.info(f"Successfully generated image ({width}x{height})")
            
            return {
                "image_base64": image_base64,
                "format": "PNG",
                "width": width,
                "height": height,
                "prompt": enhanced_prompt,
                "negative_prompt": negative_prompt,
                "steps": steps,
                "guidance_scale": guidance_scale,
                "seed": seed,
                "model": self.model_id
            }
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    async def generate_multiple_images(
        self,
        prompt: str,
        num_images: int = 2,
        **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Generate multiple images from the same prompt
        
        Args:
            prompt: Text description of desired image
            num_images: Number of images to generate
            **kwargs: Additional parameters for generation
            
        Returns:
            List of image dictionaries, or None if error
        """
        try:
            if num_images <= 0 or num_images > 4:  # Limit to prevent resource exhaustion
                logger.warning(f"Invalid number of images requested: {num_images}")
                return None
            
            images = []
            for i in range(num_images):
                # Use different seeds for variety
                seed = kwargs.get('seed')
                if seed is not None:
                    kwargs['seed'] = seed + i
                
                image_result = await self.generate_image(prompt, **kwargs)
                if image_result:
                    image_result['image_index'] = i
                    images.append(image_result)
                else:
                    logger.warning(f"Failed to generate image {i+1}/{num_images}")
            
            return images if images else None
            
        except Exception as e:
            logger.error(f"Error generating multiple images: {e}")
            return None
    
    def unload_model(self):
        """Unload the model to free memory"""
        try:
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.is_loaded = False
            logger.info("Stable Diffusion model unloaded")
            
        except Exception as e:
            logger.error(f"Error unloading model: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_id": self.model_id,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "default_width": self.default_width,
            "default_height": self.default_height,
            "default_steps": self.default_steps,
            "default_guidance_scale": self.default_guidance_scale,
            "cuda_available": torch.cuda.is_available()
        }


# Global Stable Diffusion adapter instance
stable_diffusion_adapter = StableDiffusionAdapter()