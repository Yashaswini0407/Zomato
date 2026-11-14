"""
Filter result model for tracking filter operations.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from src.app.models.restaurant import Restaurant


class FilterResult(BaseModel):
    """
    Result of a filter operation.

    Attributes:
        candidates: List of filtered restaurants
        total_before_cap: Total number of restaurants before capping
        applied_filters: Dictionary of applied filters and their values
    """

    candidates: List[Restaurant] = Field(default_factory=list, description="Filtered restaurants")
    total_before_cap: int = Field(default=0, description="Total before capping")
    applied_filters: Dict[str, Any] = Field(
        default_factory=dict, description="Applied filters"
    )
