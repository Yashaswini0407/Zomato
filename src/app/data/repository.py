"""
Restaurant repository for data access.
"""

import logging
from typing import Optional, List
from abc import ABC, abstractmethod
import pandas as pd
from src.app.models.restaurant import Restaurant
from src.app.models.filters import FilterCriteria


logger = logging.getLogger(__name__)


class RestaurantRepository(ABC):
    """
    Abstract base class for restaurant repository.

    Defines the interface for restaurant data access.
    """

    @abstractmethod
    def get_all(self) -> List[Restaurant]:
        """
        Get all restaurants.

        Returns:
            List of all restaurants
        """
        pass

    @abstractmethod
    def filter(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        Filter restaurants based on criteria.

        Args:
            criteria: Filter criteria

        Returns:
            List of filtered restaurants
        """
        pass

    @abstractmethod
    def get_by_ids(self, ids: List[str]) -> List[Restaurant]:
        """
        Get restaurants by their IDs.

        Args:
            ids: List of restaurant IDs

        Returns:
            List of restaurants with matching IDs
        """
        pass

    @abstractmethod
    def get_locations(self) -> List[str]:
        """
        Get all unique locations.

        Returns:
            List of unique location names
        """
        pass

    @abstractmethod
    def get_cuisines(self) -> List[str]:
        """
        Get all unique cuisines.

        Returns:
            List of unique cuisine names
        """
        pass


class ParquetRepository(RestaurantRepository):
    """
    Parquet-based restaurant repository.

    Loads data from a Parquet file and provides filtering capabilities.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Parquet repository.

        Args:
            file_path: Path to the Parquet file
        """
        self.file_path = file_path
        self._data: Optional[pd.DataFrame] = None
        self._restaurants: Optional[List[Restaurant]] = None

    def _load_data(self) -> pd.DataFrame:
        """
        Load data from Parquet file.

        Returns:
            DataFrame with restaurant data
        """
        if self._data is None:
            logger.info(f"Loading data from {self.file_path}")
            self._data = pd.read_parquet(self.file_path)
            logger.info(f"Loaded {len(self._data)} restaurants")
        return self._data

    def _dataframe_to_restaurants(self, df: pd.DataFrame) -> List[Restaurant]:
        """
        Convert DataFrame to list of Restaurant objects.

        Args:
            df: DataFrame with restaurant data

        Returns:
            List of Restaurant objects
        """
        restaurants = []
        for _, row in df.iterrows():
            restaurant = Restaurant(
                id=row["id"],
                name=row["name"],
                location=row["location"],
                cuisines=row["cuisines"].tolist() if isinstance(row["cuisines"], list) else row["cuisines"],
                rating=float(row["rating"]),
                estimated_cost=float(row["estimated_cost"]),
                budget_band=row["budget_band"],
                metadata=row.get("metadata", None) if "metadata" in row else None
            )
            restaurants.append(restaurant)
        return restaurants

    def get_all(self) -> List[Restaurant]:
        """
        Get all restaurants.

        Returns:
            List of all restaurants
        """
        df = self._load_data()
        return self._dataframe_to_restaurants(df)

    def filter(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        Filter restaurants based on criteria.

        Args:
            criteria: Filter criteria

        Returns:
            List of filtered restaurants
        """
        df = self._load_data()
        logger.info(f"Filtering {len(df)} restaurants with criteria: {criteria}")

        # Apply location filter
        if criteria.location:
            df = df[df["location"].str.lower().str.contains(criteria.location.lower(), na=False)]
            logger.info(f"After location filter: {len(df)} restaurants")

        # Apply budget filter
        if criteria.budget:
            budget_value = criteria.budget.value if hasattr(criteria.budget, 'value') else str(criteria.budget)
            df = df[df["budget_band"].astype(str) == budget_value]
            logger.info(f"After budget filter: {len(df)} restaurants")

        # Apply cuisine filter
        if criteria.cuisine:
            def has_cuisine(cuisines):
                """Check if cuisine list contains the target cuisine."""
                if isinstance(cuisines, list):
                    return any(criteria.cuisine.lower() in str(c).lower() for c in cuisines)
                return criteria.cuisine.lower() in str(cuisines).lower()

            df = df[df["cuisines"].apply(has_cuisine)]
            logger.info(f"After cuisine filter: {len(df)} restaurants")

        # Apply rating filter
        if criteria.min_rating is not None:
            df = df[df["rating"] >= criteria.min_rating]
            logger.info(f"After rating filter: {len(df)} restaurants")

        return self._dataframe_to_restaurants(df)

    def get_by_ids(self, ids: List[str]) -> List[Restaurant]:
        """
        Get restaurants by their IDs.

        Args:
            ids: List of restaurant IDs

        Returns:
            List of restaurants with matching IDs
        """
        df = self._load_data()
        df = df[df["id"].isin(ids)]
        return self._dataframe_to_restaurants(df)

    def get_locations(self) -> List[str]:
        """
        Get all unique locations.

        Returns:
            List of unique location names
        """
        df = self._load_data()
        locations = df["location"].unique().tolist()
        return sorted(locations)

    def get_cuisines(self) -> List[str]:
        """
        Get all unique cuisines.

        Returns:
            List of unique cuisine names
        """
        df = self._load_data()
        all_cuisines = set()
        for cuisines in df["cuisines"]:
            if isinstance(cuisines, list):
                all_cuisines.update([c.lower() for c in cuisines])
            else:
                all_cuisines.add(str(cuisines).lower())
        return sorted(list(all_cuisines))


class InMemoryRepository(RestaurantRepository):
    """
    In-memory restaurant repository.

    Loads all data into memory for fast access.
    """

    def __init__(self, restaurants: List[Restaurant]):
        """
        Initialize the in-memory repository.

        Args:
            restaurants: List of Restaurant objects
        """
        self._restaurants = restaurants
        logger.info(f"InMemoryRepository initialized with {len(restaurants)} restaurants")

    def get_all(self) -> List[Restaurant]:
        """
        Get all restaurants.

        Returns:
            List of all restaurants
        """
        return self._restaurants

    def filter(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        Filter restaurants based on criteria.

        Args:
            criteria: Filter criteria

        Returns:
            List of filtered restaurants
        """
        filtered = self._restaurants

        # Apply location filter
        if criteria.location:
            filtered = [
                r for r in filtered
                if criteria.location.lower() in r.location.lower()
            ]

        # Apply budget filter
        if criteria.budget:
            filtered = [r for r in filtered if r.budget_band == criteria.budget]

        # Apply cuisine filter
        if criteria.cuisine:
            filtered = [
                r for r in filtered
                if any(criteria.cuisine.lower() in c.lower() for c in r.cuisines)
            ]

        # Apply rating filter
        if criteria.min_rating is not None:
            filtered = [r for r in filtered if r.rating >= criteria.min_rating]

        return filtered

    def get_by_ids(self, ids: List[str]) -> List[Restaurant]:
        """
        Get restaurants by their IDs.

        Args:
            ids: List of restaurant IDs

        Returns:
            List of restaurants with matching IDs
        """
        return [r for r in self._restaurants if r.id in ids]

    def get_locations(self) -> List[str]:
        """
        Get all unique locations.

        Returns:
            List of unique location names
        """
        locations = set(r.location for r in self._restaurants)
        return sorted(list(locations))

    def get_cuisines(self) -> List[str]:
        """
        Get all unique cuisines.

        Returns:
            List of unique cuisine names
        """
        cuisines = set()
        for r in self._restaurants:
            cuisines.update([c.lower() for c in r.cuisines])
        return sorted(list(cuisines))
