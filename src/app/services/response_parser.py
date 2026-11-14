"""
Response parser for parsing LLM responses.
"""

import logging
import json
import re
from typing import Optional, Dict, Any, List


logger = logging.getLogger(__name__)


class ResponseParser:
    """
    Parses LLM responses and extracts structured data.
    """

    def __init__(self):
        """Initialize the response parser."""
        pass

    def parse(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse the raw LLM response into structured data.

        Args:
            raw_response: Raw text response from LLM

        Returns:
            Parsed response as dictionary

        Raises:
            ValueError: If parsing fails completely
        """
        logger.info("Parsing LLM response")
        logger.debug(f"Raw response length: {len(raw_response)} characters")

        # Try to extract JSON from the response
        json_str = self._extract_json(raw_response)

        if not json_str:
            logger.warning("Could not extract JSON from response")
            raise ValueError("No JSON found in LLM response")

        # Parse JSON
        try:
            parsed = json.loads(json_str)
            logger.info("JSON parsed successfully")
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            raise ValueError(f"Invalid JSON in response: {e}") from e

    def _extract_json(self, text: str) -> Optional[str]:
        """
        Extract JSON block from text.

        Args:
            text: Text that may contain JSON

        Returns:
            JSON string or None
        """
        # Try to find JSON between ```json and ```
        json_pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(json_pattern, text)
        if match:
            return match.group(1)

        # Try to find JSON between { and }
        json_pattern = r"\{[\s\S]*\}"
        match = re.search(json_pattern, text)
        if match:
            return match.group(0)

        # Try to find JSON-like structure
        # Look for patterns like "summary": ... "recommendations": ...
        if '"summary"' in text and '"recommendations"' in text:
            # Try to extract the entire JSON object
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                return text[start:end + 1]

        return None

    def validate_schema(self, parsed: Dict[str, Any]) -> bool:
        """
        Validate the parsed response schema.

        Args:
            parsed: Parsed response dictionary

        Returns:
            True if schema is valid, False otherwise
        """
        # Check required fields
        if "recommendations" not in parsed:
            logger.warning("Missing 'recommendations' field in response")
            return False

        if not isinstance(parsed["recommendations"], list):
            logger.warning("'recommendations' should be a list")
            return False

        # Validate each recommendation
        for rec in parsed["recommendations"]:
            if "restaurant_id" not in rec:
                logger.warning("Missing 'restaurant_id' in recommendation")
                return False
            if "rank" not in rec:
                logger.warning("Missing 'rank' in recommendation")
                return False
            if "explanation" not in rec:
                logger.warning("Missing 'explanation' in recommendation")
                return False

        return True
