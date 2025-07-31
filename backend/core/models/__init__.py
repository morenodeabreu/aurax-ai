"""
AURAX Specialized Model Adapters
"""

from .qwen3_coder_adapter import Qwen3CoderAdapter
from .stable_diffusion_adapter import StableDiffusionAdapter

__all__ = [
    "Qwen3CoderAdapter",
    "StableDiffusionAdapter"
]