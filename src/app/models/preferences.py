"""
User preferences models for restaurant recommendations.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
from src.app.models.restaurant import BudgetBand


class UserPreferences(BaseModel):
    """
    User preferences for restaurant recommendations.

    Attributes:
        location: Restaurant location (required)
        budget: Budget band (required)
        cuisine: Cuisine type (required)
        min_rating: Minimum rating (required)
        additional_preferences: Additional text preferences (optional)
        top_k: Number of recommendations to return (optional)
    """

    location: str = Field(..., min_length=1, description="Restaurant location")
    budget: BudgetBand = Field(..., description="Budget band")
    cuisine: str = Field(..., min_length=1, description="Cuisine type")
    min_rating: float = Field(..., ge=0.0, le=5.0, description="Minimum rating")
    additional_preferences: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Additional text preferences"
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of recommendations to return"
    )

    @field_validator("location", "cuisine")
    @classmethod
    def normalize_strings(cls, v: str) -> str:
        """Normalize string values."""
        return v.strip()

    @field_validator("location")
    @classmethod
    def title_case_location(cls, v: str) -> str:
        """Title case location for display."""
        return v.title()
