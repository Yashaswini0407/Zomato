"""
Data preprocessor for cleaning and transforming restaurant data.
"""

import logging
import re
from typing import Any
import pandas as pd
from src.app.models.restaurant import BudgetBand


logger = logging.getLogger(__name__)


class Preprocessor:
    """
    Preprocesses restaurant data by cleaning, normalizing, and transforming.

    Handles null values, string normalization, cuisine parsing, and budget band mapping.
    """

    def __init__(
        self,
        budget_low_max: int = 500,
        budget_medium_max: int = 1500,
    ):
        """
        Initialize the preprocessor.

        Args:
            budget_low_max: Maximum cost for low budget band
            budget_medium_max: Maximum cost for medium budget band
        """
        self.budget_low_max = budget_low_max
        self.budget_medium_max = budget_medium_max

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the restaurant data.

        Args:
            df: Input DataFrame with normalized schema

        Returns:
            Preprocessed DataFrame
        """
        logger.info("Starting data preprocessing")
        initial_count = len(df)

        # Add ID field
        df = self.add_id_field(df)

        # Clean null values
        df = self.clean_nulls(df)

        # Normalize strings
        df = self.normalize_strings(df)

        # Parse cuisines
        df = self.parse_cuisines(df)

        # Map budget bands
        df = self.map_budget_band(df)

        # Validate data ranges
        df = self.validate_ranges(df)

        final_count = len(df)
        logger.info(f"Preprocessing complete: {initial_count} -> {final_count} rows")

        return df

    def add_id_field(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a unique ID field to the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with id field
        """
        logger.info("Adding ID field")

        # Generate ID from name and location if not present
        if "id" not in df.columns:
            def generate_id(row):
                """Generate a unique ID from name and location."""
                if pd.isna(row.get("name")) or pd.isna(row.get("location")):
                    return f"unknown_{hash(str(row))}"
                # Create a simple ID from name and location
                name_clean = str(row["name"]).lower().replace(" ", "-")
                location_clean = str(row["location"]).lower().replace(" ", "-")
                return f"{location_clean}-{name_clean}"

            df["id"] = df.apply(generate_id, axis=1)

        return df

    def clean_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean null values in critical fields.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with nulls handled
        """
        logger.info("Cleaning null values")

        # Drop rows with null critical fields
        critical_fields = ["name", "location", "rating", "estimated_cost"]
        initial_count = len(df)

        df = df.copy()  # Avoid SettingWithCopyWarning
        df = df.dropna(subset=critical_fields)

        dropped = initial_count - len(df)
        if dropped > 0:
            logger.warning(f"Dropped {dropped} rows with null critical fields")

        # Fill null optional fields
        if "cuisines" in df.columns:
            df["cuisines"] = df["cuisines"].fillna("Other")

        return df

    def normalize_strings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize string fields.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with normalized strings
        """
        logger.info("Normalizing strings")

        # Normalize location (title case)
        if "location" in df.columns:
            df["location"] = df["location"].str.strip().str.title()

        # Normalize name (strip whitespace)
        if "name" in df.columns:
            df["name"] = df["name"].str.strip()

        return df

    def parse_cuisines(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse cuisine strings into lists.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with parsed cuisine lists
        """
        logger.info("Parsing cuisines")

        if "cuisines" not in df.columns:
            logger.warning("Cuisines column not found")
            return df

        def parse_cuisine_string(cuisine_str: Any) -> list:
            """Parse a cuisine string into a list."""
            if pd.isna(cuisine_str) or cuisine_str == "":
                return ["Other"]

            # Convert to string if not already
            cuisine_str = str(cuisine_str)

            # Split on common delimiters
            delimiters = [",", ";", "/", "-", "&"]
            for delimiter in delimiters:
                cuisine_str = cuisine_str.replace(delimiter, ",")

            # Split by comma and clean
            cuisines = [
                c.strip().lower() for c in cuisine_str.split(",") if c.strip()
            ]

            return cuisines if cuisines else ["Other"]

        df["cuisines"] = df["cuisines"].apply(parse_cuisine_string)

        return df

    def map_budget_band(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map estimated cost to budget band.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with budget_band column
        """
        logger.info("Mapping budget bands")

        def get_budget_band(cost: float) -> BudgetBand:
            """Get budget band from cost."""
            if cost <= self.budget_low_max:
                return BudgetBand.LOW
            elif cost <= self.budget_medium_max:
                return BudgetBand.MEDIUM
            else:
                return BudgetBand.HIGH

        df = df.copy()  # Avoid SettingWithCopyWarning
        df["budget_band"] = df["estimated_cost"].apply(get_budget_band)

        # Log distribution
        band_counts = df["budget_band"].value_counts()
        logger.info(f"Budget band distribution:\n{band_counts}")

        return df

    def get_budget_band_for_cost(self, cost: float) -> BudgetBand:
        """
        Get budget band for a single cost value.

        Args:
            cost: Cost value

        Returns:
            BudgetBand enum value
        """
        if cost <= self.budget_low_max:
            return BudgetBand.LOW
        elif cost <= self.budget_medium_max:
            return BudgetBand.MEDIUM
        else:
            return BudgetBand.HIGH

    def validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and clamp data ranges.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with validated ranges
        """
        logger.info("Validating data ranges")

        # Clamp rating to [0, 5]
        if "rating" in df.columns:
            initial_invalid = ((df["rating"] < 0) | (df["rating"] > 5)).sum()
            if initial_invalid > 0:
                logger.warning(f"Clamping {initial_invalid} invalid ratings")
            df["rating"] = df["rating"].clip(0, 5)

        # Ensure cost is non-negative
        if "estimated_cost" in df.columns:
            initial_invalid = (df["estimated_cost"] < 0).sum()
            if initial_invalid > 0:
                logger.warning(f"Setting {initial_invalid} negative costs to 0")
            df["estimated_cost"] = df["estimated_cost"].clip(lower=0)

        return df
