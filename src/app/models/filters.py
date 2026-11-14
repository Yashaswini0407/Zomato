"""
Filter criteria models for restaurant queries.
"""

from typing import Optional
from pydantic import BaseModel, Field
from src.app.models.restaurant import BudgetBand


class FilterCriteria(BaseModel):
    """
    Criteria for filtering restaurants.

    Attributes:
        location: Location filter (substring or exact match)
        budget: Budget band filter
        cuisine: Cuisine filter (any-match in cuisines list)
        min_rating: Minimum rating filter
        additional_preferences: Additional text preferences (not used structurally)
    """

    location: Optional[str] = Field(
        default=None,
        description="Location filter (substring or exact match)"
    )
    budget: Optional[BudgetBand] = Field(
        default=None,
        description="Budget band filter"
    )
    cuisine: Optional[str] = Field(
        default=None,
        description="Cuisine filter (any-match in cuisines list)"
    )
    min_rating: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=5.0,
        description="Minimum rating filter"
    )
    additional_preferences: Optional[str] = Field(
        default=None,
        description="Additional text preferences (not used structurally)"
    )

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
