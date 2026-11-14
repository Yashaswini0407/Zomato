"""
Schema normalizer for mapping raw dataset columns to canonical schema.
"""

import logging
from typing import Any, Dict
import pandas as pd


logger = logging.getLogger(__name__)


class SchemaNormalizer:
    """
    Normalizes the schema of raw dataset to canonical Restaurant model.

    Maps raw column names to canonical field names and handles missing columns.
    """

    # Column mapping from raw dataset to canonical fields
    # This will be updated after inspecting the actual dataset
    COLUMN_MAPPING: Dict[str, str] = {
        # Common column names in Zomato datasets
        "name": "name",
        "restaurant_name": "name",
        "Name": "name",
        "location": "location",
        "city": "location",
        "City": "location",
        "cuisines": "cuisines",
        "cuisine": "cuisines",
        "Cuisines": "cuisines",
        "rating": "rating",
        "aggregate_rating": "rating",
        "Rating": "rating",
        "cost": "estimated_cost",
        "average_cost_for_two": "estimated_cost",
        "Cost": "estimated_cost",
        "votes": "votes",
        "Votes": "votes",
    }

    # Required columns that must be present
    REQUIRED_COLUMNS = ["name", "location", "cuisines", "rating", "estimated_cost"]

    def __init__(self):
        """Initialize the schema normalizer."""
        pass

    def normalize(self, raw_data: Any) -> pd.DataFrame:
        """
        Normalize the raw dataset to canonical schema.

        Args:
            raw_data: Raw dataset from Hugging Face (can be Dataset dict or DataFrame)

        Returns:
            Normalized pandas DataFrame with canonical column names

        Raises:
            ValueError: If required columns are missing
        """
        logger.info("Normalizing dataset schema")

        # Convert to DataFrame if needed
        if not isinstance(raw_data, pd.DataFrame):
            df = pd.DataFrame(raw_data)
        else:
            df = raw_data.copy()

        logger.info(f"Original columns: {list(df.columns)}")

        # Apply column mapping
        normalized_columns = {}
        for col in df.columns:
            # Try exact match first
            if col in self.COLUMN_MAPPING:
                normalized_columns[col] = self.COLUMN_MAPPING[col]
            else:
                # Try case-insensitive match
                for key, value in self.COLUMN_MAPPING.items():
                    if col.lower() == key.lower():
                        normalized_columns[col] = value
                        break
                else:
                    # Keep original column name if no mapping found
                    normalized_columns[col] = col

        # Rename columns
        df = df.rename(columns=normalized_columns)

        logger.info(f"Normalized columns: {list(df.columns)}")

        # Check for required columns
        missing_columns = [
            col for col in self.REQUIRED_COLUMNS if col not in df.columns
        ]

        if missing_columns:
            logger.warning(f"Missing required columns: {missing_columns}")
            # Try to find similar columns
            for missing in missing_columns:
                similar = self._find_similar_column(missing, df.columns)
                if similar:
                    logger.info(f"Using '{similar}' for missing '{missing}'")
                    df = df.rename(columns={similar: missing})
                    missing_columns.remove(missing)

        if missing_columns:
            raise ValueError(
                f"Cannot proceed without required columns: {missing_columns}. "
                f"Available columns: {list(df.columns)}"
            )

        logger.info("Schema normalization complete")
        return df

    def _find_similar_column(self, target: str, columns: list) -> str:
        """
        Find a column similar to the target name.

        Args:
            target: Target column name
            columns: Available column names

        Returns:
            Similar column name or None
        """
        target_lower = target.lower()
        for col in columns:
            col_lower = col.lower()
            if target_lower in col_lower or col_lower in target_lower:
                return col
        return None
