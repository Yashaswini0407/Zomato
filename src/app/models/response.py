"""
Response models for the recommendation system.
"""

from typing import Optional, Any, List
from pydantic import BaseModel, Field
from src.app.models.restaurant import Restaurant


class Recommendation(BaseModel):
    """
    Single recommendation with restaurant details and explanation.

    Attributes:
        restaurant: Restaurant entity
        rank: Rank in the recommendation list
        explanation: LLM-generated explanation
    """

    restaurant: Restaurant = Field(..., description="Restaurant entity")
    rank: int = Field(..., ge=1, description="Rank in recommendations")
    explanation: str = Field(..., description="Explanation for recommendation")


class RecommendationResponse(BaseModel):
    """
    Complete recommendation response.

    Attributes:
        summary: Summary of recommendations
        recommendations: List of recommendations
        meta: Metadata about the request
    """

    summary: Optional[str] = Field(default=None, description="Summary of recommendations")
    recommendations: List[Recommendation] = Field(
        default_factory=list,
        description="List of recommendations"
    )
    meta: Optional[dict[str, Any]] = Field(
        default=None,
        description="Metadata about the request"
    )

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
