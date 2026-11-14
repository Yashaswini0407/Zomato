"""
Filter service for applying business rules to restaurant data.
"""

import logging
from typing import List, Optional
from src.app.models.preferences import UserPreferences
from src.app.models.filter_result import FilterResult
from src.app.models.filters import FilterCriteria
from src.app.data.repository import RestaurantRepository
from src.app.models.restaurant import Restaurant
from src.app.config import get_settings


logger = logging.getLogger(__name__)


class FilterService:
    """
    Service for applying deterministic filters to restaurant data.

    Handles filtering, sorting, and candidate capping.
    """

    def __init__(self, max_candidates: Optional[int] = None):
        """
        Initialize the filter service.

        Args:
            max_candidates: Maximum number of candidates to return
        """
        settings = get_settings()
        self.max_candidates = max_candidates or settings.max_candidates

    def filter(
        self,
        preferences: UserPreferences,
        repository: RestaurantRepository
    ) -> FilterResult:
        """
        Apply filters based on user preferences.

        Args:
            preferences: User preferences
            repository: Restaurant repository

        Returns:
            FilterResult with candidates and metadata
        """
        logger.info(f"Filtering restaurants with preferences: {preferences}")

        # Build filter criteria from preferences
        criteria = FilterCriteria(
            location=preferences.location,
            budget=preferences.budget,
            cuisine=preferences.cuisine,
            min_rating=preferences.min_rating,
            additional_preferences=preferences.additional_preferences,
        )

        # Apply filters through repository
        candidates = repository.filter(criteria)

        total_before_cap = len(candidates)
        logger.info(f"Total candidates before capping: {total_before_cap}")

        # Check if no candidates
        if not candidates:
            logger.warning("No candidates found after filtering")
            return FilterResult(
                candidates=[],
                total_before_cap=total_before_cap,
                applied_filters={
                    "location": preferences.location,
                    "budget": preferences.budget.value,
                    "cuisine": preferences.cuisine,
                    "min_rating": preferences.min_rating,
                }
            )

        # Sort by rating descending, then by any secondary criteria
        candidates = self._sort_candidates(candidates)

        # Cap candidates at max_candidates
        if len(candidates) > self.max_candidates:
            candidates = candidates[:self.max_candidates]
            logger.info(f"Capped candidates to {self.max_candidates}")

        logger.info(f"Final candidates: {len(candidates)}")

        return FilterResult(
            candidates=candidates,
            total_before_cap=total_before_cap,
            applied_filters={
                "location": preferences.location,
                "budget": preferences.budget.value,
                "cuisine": preferences.cuisine,
                "min_rating": preferences.min_rating,
                "capped_at": self.max_candidates if total_before_cap > self.max_candidates else None,
            }
        )

    def _sort_candidates(self, candidates: List[Restaurant]) -> List[Restaurant]:
        """
        Sort candidates by rating descending.

        Args:
            candidates: List of restaurants to sort

        Returns:
            Sorted list of restaurants
        """
        # Sort by rating descending
        sorted_candidates = sorted(
            candidates,
            key=lambda r: r.rating,
            reverse=True
        )
        return sorted_candidates
