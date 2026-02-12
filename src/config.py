"""Configuration management using Pydantic settings."""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # LLM Provider
    llm_provider: Literal["ollama", "groq"] = Field(
        default="ollama",
        description="LLM provider to use"
    )
    
    # Ollama Settings
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL"
    )
    ollama_model: str = Field(
        default="qwen2.5-coder:7b",
        description="Ollama model to use"
    )
    
    # Groq Settings
    groq_api_key: str = Field(
        default="",
        description="Groq API key (optional)"
    )
    groq_model: str = Field(
        default="llama-3.1-70b-versatile",
        description="Groq model to use"
    )
    
    # Explanation Settings
    explanation_depth: Literal["simple", "detailed", "deep", "all"] = Field(
        default="all",
        description="Default explanation depth"
    )
    generate_diagrams: bool = Field(
        default=True,
        description="Whether to generate diagrams"
    )
    max_diagram_nodes: int = Field(
        default=50,
        description="Maximum nodes in generated diagrams"
    )
    
    # Code Analysis Settings
    max_file_size_kb: int = Field(
        default=500,
        description="Maximum file size to analyze in KB"
    )
    supported_languages: str = Field(
        default="python,javascript,typescript,rust",
        description="Comma-separated list of supported languages"
    )
    
    # Cache Settings
    enable_cache: bool = Field(
        default=True,
        description="Enable response caching"
    )
    cache_ttl_seconds: int = Field(
        default=3600,
        description="Cache TTL in seconds"
    )
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )
    
    @property
    def supported_languages_list(self) -> list[str]:
        """Get supported languages as a list."""
        return [lang.strip() for lang in self.supported_languages.split(",")]
    
    def is_groq_available(self) -> bool:
        """Check if Groq API is configured."""
        return bool(self.groq_api_key and self.llm_provider == "groq")


# Global settings instance
settings = Settings()
