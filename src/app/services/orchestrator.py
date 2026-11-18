"""
Recommendation orchestrator - coordinates all services.
"""

import logging
from typing import Optional
from src.app.services.validator import InputValidator
from src.app.services.filter_service import FilterService
from src.app.services.llm_client import GroqClient
from src.app.services.prompt_builder import PromptBuilder
from src.app.services.response_parser import ResponseParser
from src.app.services.merger import RecommendationMerger
from src.app.data.repository import RestaurantRepository
from src.app.models.preferences import UserPreferences
from src.app.models.response import RecommendationResponse, Recommendation
from src.app.models.restaurant import Restaurant
from src.app.config import get_settings


logger = logging.getLogger(__name__)


class RecommendationOrchestrator:
    """
    Orchestrates the complete recommendation flow.

    Coordinates: validate → filter → prompt → LLM → parse → merge
    """

    def __init__(self, repository: RestaurantRepository):
        """
        Initialize the orchestrator.

        Args:
            repository: Restaurant repository
        """
        self.repository = repository
        self.validator = InputValidator()
        self.filter_service = FilterService()
        self.llm_client = GroqClient()
        self.prompt_builder = PromptBuilder()
        self.response_parser = ResponseParser()
        self.merger = RecommendationMerger()

    def execute(self, preferences: dict) -> RecommendationResponse:
        """
        Execute the complete recommendation flow.

        Args:
            preferences: User preferences as dictionary

        Returns:
            RecommendationResponse with recommendations
        """
        logger.info("=" * 60)
        logger.info("Starting recommendation flow")
        logger.info("=" * 60)

        try:
            # Stage 1: Validate input
            logger.info("Stage 1: Validating input")
            user_prefs = self.validator.validate(preferences)
            logger.info(f"Validated preferences: {user_prefs.location}, {user_prefs.budget.value}, {user_prefs.cuisine}")

            # Stage 2: Filter candidates
            logger.info("Stage 2: Filtering candidates")
            filter_result = self.filter_service.filter(user_prefs, self.repository)
            candidates = filter_result.candidates
            logger.info(f"Filtered candidates: {len(candidates)}")

            # Stage 3: Check if no candidates
            if not candidates:
                logger.warning("No candidates found after filtering")
                return RecommendationResponse(
                    summary=f"No restaurants found matching your criteria in {user_prefs.location}",
                    recommendations=[],
                    meta={
                        "total_candidates": 0,
                        "used_fallback": False,
                        "error": "No candidates"
                    }
                )

            # Stage 4: Build prompt
            logger.info("Stage 4: Building prompt")
            prompt = self.prompt_builder.build(user_prefs, candidates)
            logger.info(f"Prompt built: {len(prompt)} characters")

            # Stage 5: Call LLM
            logger.info("Stage 5: Calling LLM")
            try:
                llm_response = self.llm_client.complete(prompt, temperature=0.3, max_tokens=1024)
                logger.info(f"LLM response received: {len(llm_response)} characters")
                used_fallback = False
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                logger.info("Using fallback: rating-based ranking")
                return self._fallback_ranking(candidates, user_prefs, "LLM API failure")

            # Stage 6: Parse response
            logger.info("Stage 6: Parsing LLM response")
            try:
                parsed = self.response_parser.parse(llm_response)
                is_valid = self.response_parser.validate_schema(parsed)
                if not is_valid:
                    logger.warning("Schema validation failed")
                    return self._fallback_ranking(candidates, user_prefs, "Invalid LLM response")
            except Exception as e:
                logger.error(f"Parse failed: {e}")
                return self._fallback_ranking(candidates, user_prefs, "Parse failure")

            # Stage 7: Merge with restaurant data
            logger.info("Stage 7: Merging recommendations")
            try:
                merged = self.merger.merge(parsed, candidates)
                logger.info(f"Merged recommendations: {len(merged)}")
            except Exception as e:
                logger.error(f"Merge failed: {e}")
                return self._fallback_ranking(candidates, user_prefs, "Merge failure")

            # Stage 8: Build response
            logger.info("Stage 8: Building response")
            recommendations = [
                Recommendation(
                    restaurant=item["restaurant"],
                    rank=item["rank"],
                    explanation=item["explanation"]
                )
                for item in merged
            ]

            response = RecommendationResponse(
                summary=parsed.get("summary"),
                recommendations=recommendations,
                meta={
                    "total_candidates": len(candidates),
                    "returned": len(recommendations),
                    "used_fallback": False,
                    "llm_model": get_settings().llm_model
                }
            )

            logger.info("=" * 60)
            logger.info("Recommendation flow completed successfully")
            logger.info("=" * 60)

            return response

        except Exception as e:
            logger.error(f"Orchestrator failed: {e}")
            raise

    def _fallback_ranking(
        self,
        candidates: list[Restaurant],
        preferences: UserPreferences,
        reason: str
    ) -> RecommendationResponse:
        """
        Fallback to rating-based ranking when LLM fails.

        Args:
            candidates: List of candidate restaurants
            preferences: User preferences
            reason: Reason for fallback

        Returns:
            RecommendationResponse with fallback recommendations
        """
        logger.info(f"Using fallback ranking: {reason}")

        # Sort by rating descending
        sorted_candidates = sorted(candidates, key=lambda r: r.rating, reverse=True)
        top_k = min(len(sorted_candidates), preferences.top_k)

        recommendations = []
        for i, restaurant in enumerate(sorted_candidates[:top_k], 1):
            explanation = (
                f"{restaurant.name} is a great choice in {restaurant.location} "
                f"with a rating of {restaurant.rating}. "
                f"It serves {', '.join(restaurant.cuisines)} and fits your {preferences.budget.value} budget."
            )
            recommendations.append(
                Recommendation(
                    restaurant=restaurant,
                    rank=i,
                    explanation=explanation
                )
            )

        return RecommendationResponse(
            summary=f"Showing top {len(recommendations)} restaurants sorted by rating (LLM unavailable: {reason})",
            recommendations=recommendations,
            meta={
                "total_candidates": len(candidates),
                "returned": len(recommendations),
                "used_fallback": True,
                "fallback_reason": reason
            }
        )
