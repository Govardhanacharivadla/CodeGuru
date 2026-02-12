"""LLM client with support for Ollama (local) and Groq (free API)."""

import json
import hashlib
from typing import Optional, Literal
from abc import ABC, abstractmethod
from pydantic import BaseModel

from .config import settings
from .utils import logger


class Concept(BaseModel):
    """A key concept extracted from code."""
    name: str
    definition: str
    related_topics: list[str] = []


class Explanation(BaseModel):
    """Structured explanation response."""
    summary: str
    simple_explanation: str
    detailed_explanation: str
    deep_dive: str
    key_concepts: list[Concept]
    common_mistakes: list[str]
    best_practices: list[str]
    related_resources: list[str]


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[type[BaseModel]] = None
    ) -> str:
        """Generate completion from LLM."""
        pass


class OllamaClient(LLMClient):
    """Client for local Ollama models."""
    
    def __init__(self, model: str = None, base_url: str = None):
        """Initialize Ollama client."""
        try:
            import ollama
            # ollama.Client() doesn't need parameters in newer versions
            self.client = ollama
        except ImportError:
            raise ImportError(
                "Ollama package not installed. Install with: pip install ollama"
            )
        
        self.model = model or settings.ollama_model
        self.base_url = base_url or settings.ollama_base_url
        logger.info(f"Initialized Ollama client with model: {self.model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[type[BaseModel]] = None
    ) -> str:
        """Generate completion from Ollama."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            # Request JSON format if response_format is specified
            if response_format:
                # Add instruction to prompt for JSON
                messages[-1]["content"] += "\n\nRespond in valid JSON format."
            
            # Use module-level chat function
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            content = response['message']['content']
            
            # Validate JSON if format specified
            if response_format:
                try:
                    # Try to parse and validate
                    json_data = json.loads(content)
                    # Validate against Pydantic model
                    response_format(**json_data)
                except (json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Response not valid JSON, returning as-is: {e}")
            
            return content
            
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise


class GroqClient(LLMClient):
    """Client for Groq free API."""
    
    def __init__(self, model: str = None, api_key: str = None):
        """Initialize Groq client."""
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key or settings.groq_api_key)
        except ImportError:
            raise ImportError(
                "Groq package not installed. Install with: pip install groq"
            )
        
        self.model = model or settings.groq_model
        logger.info(f"Initialized Groq client with model: {self.model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[type[BaseModel]] = None
    ) -> str:
        """Generate completion from Groq."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            # Groq supports JSON mode
            extra_params = {}
            if response_format:
                extra_params["response_format"] = {"type": "json_object"}
                messages[-1]["content"] += "\n\nRespond in valid JSON format."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **extra_params
            )
            
            content = response.choices[0].message.content
            
            # Validate JSON if format specified
            if response_format:
                try:
                    json_data = json.loads(content)
                    response_format(**json_data)
                except (json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Response not valid JSON: {e}")
            
            return content
            
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise


class LLMManager:
    """Manages LLM clients and handles failover."""
    
    def __init__(self):
        """Initialize LLM manager."""
        self.primary_client: Optional[LLMClient] = None
        self.fallback_client: Optional[LLMClient] = None
        self.cache: dict[str, str] = {}
        
        # Initialize primary client
        if settings.llm_provider == "groq" and settings.groq_api_key:
            try:
                self.primary_client = GroqClient()
            except Exception as e:
                logger.warning(f"Failed to initialize Groq: {e}")
        
        # Default to Ollama
        if self.primary_client is None:
            try:
                self.primary_client = OllamaClient()
            except Exception as e:
                logger.error(f"Failed to initialize Ollama: {e}")
                raise RuntimeError(
                    "No LLM client available. Please install Ollama or configure Groq API."
                )
        
        # Set up fallback if using Groq
        if isinstance(self.primary_client, GroqClient):
            try:
                self.fallback_client = OllamaClient()
            except Exception:
                pass  # Fallback not available
    
    def _get_cache_key(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate cache key from prompts."""
        content = f"{system_prompt or ''}{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[type[BaseModel]] = None,
        use_cache: bool = True
    ) -> str:
        """Generate completion with caching and fallback."""
        
        # Check cache
        if use_cache and settings.enable_cache:
            cache_key = self._get_cache_key(prompt, system_prompt)
            if cache_key in self.cache:
                logger.debug("Using cached response")
                return self.cache[cache_key]
        
        # Try primary client
        try:
            response = await self.primary_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                response_format=response_format
            )
            
            # Cache successful response
            if use_cache and settings.enable_cache:
                self.cache[cache_key] = response
            
            return response
            
        except Exception as e:
            logger.warning(f"Primary client failed: {e}")
            
            # Try fallback
            if self.fallback_client:
                logger.info("Attempting fallback client...")
                try:
                    response = await self.fallback_client.generate(
                        prompt=prompt,
                        system_prompt=system_prompt,
                        response_format=response_format
                    )
                    
                    if use_cache and settings.enable_cache:
                        self.cache[cache_key] = response
                    
                    return response
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback client also failed: {fallback_error}")
            
            raise RuntimeError(f"All LLM clients failed. Last error: {e}")
    
    def select_model_for_task(
        self, 
        task_type: Literal["simple", "detailed", "deep"]
    ) -> None:
        """Select appropriate model based on task complexity."""
        if isinstance(self.primary_client, OllamaClient):
            if task_type == "simple":
                self.primary_client.model = "llama3.2:3b"  # Fast model
            elif task_type == "detailed":
                self.primary_client.model = "qwen2.5-coder:7b"  # Code specialist
            else:  # deep
                self.primary_client.model = "qwen2.5-coder:14b"  # Best quality
            
            logger.debug(f"Selected model: {self.primary_client.model}")


# Global LLM manager instance
llm_manager = LLMManager()
