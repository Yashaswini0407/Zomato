"""
Configuration management for the restaurant recommendation system.

Uses pydantic-settings to load configuration from environment variables.
"""

from typing import Literal
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        llm_provider: The LLM provider to use (groq, openai, anthropic, ollama)
        llm_api_key: API key for the LLM provider
        llm_model: Model name to use with the LLM provider
        data_path: Path to the processed restaurant data file
        max_candidates: Maximum number of candidates to send to LLM
        budget_low_max: Maximum cost for low budget band (INR)
        budget_medium_max: Maximum cost for medium budget band (INR)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Configuration
    llm_provider: Literal["groq", "openai", "anthropic", "ollama"] = Field(
        default="groq",
        description="LLM provider to use"
    )
    llm_api_key: str = Field(
        default="",
        description="API key for the LLM provider"
    )
    llm_model: str = Field(
        default="qwen/qwen3.8-27b",
        description="Model name to use with the LLM provider"
    )

    # Data Configuration
    data_path: str = Field(
        default="data/processed/restaurants.parquet",
        description="Path to the processed restaurant data file"
    )

    # Filter Configuration
    max_candidates: int = Field(
        default=30,
        ge=1,
        le=100,
        description="Maximum number of candidates to send to LLM"
    )

    # Budget Band Configuration (in INR)
    budget_low_max: int = Field(
        default=500,
        gt=0,
        description="Maximum cost for low budget band"
    )
    budget_medium_max: int = Field(
        default=1500,
        gt=0,
        description="Maximum cost for medium budget band"
    )

    # Application Configuration
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )

    @field_validator("llm_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that API key is not empty when using groq/openai/anthropic."""
        # Allow empty for local development with ollama
        return v

    @field_validator("budget_medium_max")
    @classmethod
    def validate_budget_thresholds(cls, v: int, info) -> int:
        """Ensure medium budget max is greater than low budget max."""
        if "budget_low_max" in info.data:
            if v <= info.data["budget_low_max"]:
                raise ValueError(
                    "budget_medium_max must be greater than budget_low_max"
                )
        return v


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the application settings.

    Returns:
        Settings: The application settings instance
    """
    return settings
