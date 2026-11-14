"""
Prompt builder for constructing LLM prompts.
"""

import logging
import json
from typing import List
from src.app.models.preferences import UserPreferences
from src.app.models.restaurant import Restaurant


logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Builds prompts for the LLM to generate restaurant recommendations.
    """

    def __init__(self):
        """Initialize the prompt builder."""
        pass

    def build(self, preferences: UserPreferences, candidates: List[Restaurant]) -> str:
        """
        Build a complete prompt for the LLM.

        Args:
            preferences: User preferences
            candidates: List of candidate restaurants

        Returns:
            Complete prompt string
        """
        logger.info(f"Building prompt for {len(candidates)} candidates")

        # System message
        system_message = self._build_system_message()

        # User context
        user_context = self._build_user_context(preferences)

        # Candidate block
        candidate_block = self._build_candidate_block(candidates)

        # Task instructions
        task_instructions = self._build_task_instructions(preferences.top_k)

        # Combine all parts
        prompt = f"{system_message}\n\n{user_context}\n\n{candidate_block}\n\n{task_instructions}"

        logger.info(f"Prompt built: {len(prompt)} characters")
        return prompt

    def _build_system_message(self) -> str:
        """
        Build the system message for the LLM.

        Returns:
            System message string
        """
        return """You are a restaurant recommendation expert. Your task is to recommend restaurants from the provided list based on user preferences.

IMPORTANT CONSTRAINTS:
- You MUST ONLY recommend restaurants from the provided list
- Do not invent or hallucinate restaurants that are not in the list
- Use the restaurant_id field to identify each restaurant
- Provide clear explanations for why each recommendation fits the user's preferences"""

    def _build_user_context(self, preferences: UserPreferences) -> str:
        """
        Build the user context section of the prompt.

        Args:
            preferences: User preferences

        Returns:
            User context string
        """
        context_parts = [
            f"User Preferences:",
            f"- Location: {preferences.location}",
            f"- Budget: {preferences.budget.value}",
            f"- Cuisine: {preferences.cuisine}",
            f"- Minimum Rating: {preferences.min_rating}",
        ]

        if preferences.additional_preferences:
            context_parts.append(f"- Additional Preferences: {preferences.additional_preferences}")

        return "\n".join(context_parts)

    def _build_candidate_block(self, candidates: List[Restaurant]) -> str:
        """
        Build the candidate restaurants block.

        Args:
            candidates: List of candidate restaurants

        Returns:
            Candidate block as JSON string
        """
        candidates_data = []
        for r in candidates:
            candidates_data.append({
                "restaurant_id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisines": r.cuisines,
                "rating": r.rating,
                "estimated_cost": r.estimated_cost,
                "budget_band": r.budget_band.value if hasattr(r.budget_band, 'value') else str(r.budget_band),
            })

        return f"Available Restaurants:\n```json\n{json.dumps(candidates_data, indent=2)}\n```"

    def _build_task_instructions(self, top_k: int) -> str:
        """
        Build the task instructions for the LLM.

        Args:
            top_k: Number of recommendations to return

        Returns:
            Task instructions string
        """
        return f"""Task:
1. Review the user's preferences and the available restaurants
2. Select the top {top_k} restaurants that best match the user's preferences
3. Rank them from 1 (best match) to {top_k}
4. For each restaurant, provide a clear explanation of why it fits the user's preferences
5. Optionally provide a brief summary of your selection

Output Format:
Return your response as a JSON object with the following structure:
{{
  "summary": "Brief overview of your selection for this user (1-2 sentences)",
  "recommendations": [
    {{
      "restaurant_id": "restaurant_id from the list",
      "rank": 1,
      "explanation": "Why this restaurant fits the user's location, budget, cuisine, and any additional preferences"
    }}
  ]
}}

IMPORTANT: Ensure all restaurant_id values match exactly the IDs in the provided list."""
