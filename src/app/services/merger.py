"""
Recommendation merger for joining LLM output with restaurant data.
"""

import logging
from typing import List, Dict, Any
from src.app.models.restaurant import Restaurant


logger = logging.getLogger(__name__)


class RecommendationMerger:
    """
    Merges LLM output with restaurant entities.
    """

    def __init__(self):
        """Initialize the merger."""
        pass

    def merge(self, llm_output: Dict[str, Any], candidates: List[Restaurant]) -> List[Dict[str, Any]]:
        """
        Merge LLM output with restaurant data.

        Args:
            llm_output: Parsed LLM response
            candidates: List of candidate restaurants

        Returns:
            Merged recommendations with full restaurant details
        """
        logger.info(f"Merging {len(candidates)} candidates with LLM output")

        recommendations = llm_output.get("recommendations", [])
        merged = []

        # Create a lookup map for candidates
        candidate_map = {r.id: r for r in candidates}

        for rec in recommendations:
            restaurant_id = rec.get("restaurant_id")
            if restaurant_id in candidate_map:
                restaurant = candidate_map[restaurant_id]
                merged.append({
                    "rank": rec.get("rank"),
                    "explanation": rec.get("explanation"),
                    "restaurant": restaurant
                })
            else:
                logger.warning(f"Restaurant ID {restaurant_id} not found in candidates, dropping")

        logger.info(f"Merged {len(merged)} recommendations")
        return merged
