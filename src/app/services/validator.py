"""
Input validator for user preferences.
"""

import logging
from typing import Optional
from src.app.models.preferences import UserPreferences


logger = logging.getLogger(__name__)


class InputValidator:
    """
    Validates and normalizes user input preferences.
    """

    def validate(self, preferences: dict) -> UserPreferences:
        """
        Validate and convert preferences dict to UserPreferences model.

        Args:
            preferences: Dictionary of user preferences

        Returns:
            Validated UserPreferences object

        Raises:
            ValueError: If validation fails
        """
        logger.info(f"Validating preferences: {preferences}")

        try:
            user_prefs = UserPreferences(**preferences)
            logger.info("Preferences validated successfully")
            return user_prefs
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise ValueError(f"Invalid preferences: {e}") from e

    def normalize_location(self, location: str) -> str:
        """
        Normalize location string.

        Args:
            location: Location string

        Returns:
            Normalized location (title case)
        """
        return location.strip().title()
