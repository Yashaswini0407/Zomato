"""
Restaurant domain models.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class BudgetBand(str, Enum):
    """Budget band classification for restaurants."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Restaurant(BaseModel):
    """
    Restaurant entity.

    Attributes:
        id: Unique identifier for the restaurant
        name: Name of the restaurant
        location: City or locality where the restaurant is located
        cuisines: List of cuisines served
        rating: Aggregate rating (0-5)
        estimated_cost: Estimated cost for two people (INR)
        budget_band: Budget classification (low, medium, high)
        metadata: Optional additional metadata
    """

    id: str = Field(..., description="Unique identifier for the restaurant")
    name: str = Field(..., description="Name of the restaurant")
    location: str = Field(..., description="City or locality")
    cuisines: list[str] = Field(
        default_factory=list,
        description="List of cuisines served"
    )
    rating: float = Field(
        ...,
        ge=0.0,
        le=5.0,
        description="Aggregate rating (0-5)"
    )
    estimated_cost: float = Field(
        ...,
        ge=0.0,
        description="Estimated cost for two people (INR)"
    )
    budget_band: BudgetBand = Field(
        ...,
        description="Budget classification"
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Optional additional metadata"
    )

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        json_encoders = {
            BudgetBand: lambda v: v.value,
        }
