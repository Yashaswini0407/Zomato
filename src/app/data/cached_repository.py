"""
Cached repository with LRU caching support.
"""

import logging
from functools import lru_cache
from typing import List, Optional
from src.app.data.repository import RestaurantRepository, ParquetRepository
from src.app.models.restaurant import Restaurant
from src.app.models.filters import FilterCriteria


logger = logging.getLogger(__name__)


class CachedRepository(RestaurantRepository):
    """
    Repository decorator that adds LRU caching to another repository.

    Caches results of expensive operations to improve performance.
    """

    def __init__(self, repository: RestaurantRepository, maxsize: int = 128):
        """
        Initialize the cached repository.

        Args:
            repository: The underlying repository to cache
            maxsize: Maximum size of the LRU cache
        """
        self._repository = repository
        self._maxsize = maxsize
        self._cache_hits = 0
        self._cache_misses = 0

    def get_all(self) -> List[Restaurant]:
        """
        Get all restaurants (cached).

        Returns:
            List of all restaurants
        """
        return self._repository.get_all()

    def filter(self, criteria: FilterCriteria) -> List[Restaurant]:
        """
        Filter restaurants (cached).

        Args:
            criteria: Filter criteria

        Returns:
            List of filtered restaurants
        """
        # Create a hashable key from criteria
        cache_key = self._make_cache_key(criteria)

        # Try to get from cache
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            self._cache_hits += 1
            logger.debug(f"Cache hit for filter: {cache_key}")
            return cached_result

        # Cache miss - get from repository
        self._cache_misses += 1
        logger.debug(f"Cache miss for filter: {cache_key}")
        result = self._repository.filter(criteria)

        # Store in cache
        self._store_in_cache(cache_key, result)

        return result

    def get_by_ids(self, ids: List[str]) -> List[Restaurant]:
        """
        Get restaurants by IDs (cached).

        Args:
            ids: List of restaurant IDs

        Returns:
            List of restaurants with matching IDs
        """
        # Sort IDs for consistent cache key
        sorted_ids = tuple(sorted(ids))
        cache_key = f"ids_{sorted_ids}"

        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            self._cache_hits += 1
            return cached_result

        self._cache_misses += 1
        result = self._repository.get_by_ids(ids)
        self._store_in_cache(cache_key, result)

        return result

    def get_locations(self) -> List[str]:
        """
        Get all unique locations (cached).

        Returns:
            List of unique location names
        """
        cache_key = "locations"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            self._cache_hits += 1
            return cached_result

        self._cache_misses += 1
        result = self._repository.get_locations()
        self._store_in_cache(cache_key, result)

        return result

    def get_cuisines(self) -> List[str]:
        """
        Get all unique cuisines (cached).

        Returns:
            List of unique cuisine names
        """
        cache_key = "cuisines"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            self._cache_hits += 1
            return cached_result

        self._cache_misses += 1
        result = self._repository.get_cuisines()
        self._store_in_cache(cache_key, result)

        return result

    def _make_cache_key(self, criteria: FilterCriteria) -> str:
        """
        Create a hashable cache key from filter criteria.

        Args:
            criteria: Filter criteria

        Returns:
            String cache key
        """
        parts = []
        if criteria.location:
            parts.append(f"loc_{criteria.location.lower()}")
        if criteria.budget:
            parts.append(f"bud_{criteria.budget.value}")
        if criteria.cuisine:
            parts.append(f"cui_{criteria.cuisine.lower()}")
        if criteria.min_rating is not None:
            parts.append(f"rat_{criteria.min_rating}")
        return "_".join(parts) if parts else "all"

    def _get_from_cache(self, key: str) -> Optional[List[Restaurant]]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        # Simple in-memory cache (in production, use Redis or similar)
        if not hasattr(self, "_cache"):
            self._cache = {}
        return self._cache.get(key)

    def _store_in_cache(self, key: str, value: List[Restaurant]) -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to store
        """
        if not hasattr(self, "_cache"):
            self._cache = {}

        # Simple LRU eviction based on size
        if len(self._cache) >= self._maxsize:
            # Remove oldest entry (first key)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"Evicted cache entry: {oldest_key}")

        self._cache[key] = value

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0

        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "total": total,
            "hit_rate": hit_rate,
            "size": len(getattr(self, "_cache", {})),
        }

    def clear_cache(self) -> None:
        """Clear the cache."""
        if hasattr(self, "_cache"):
            self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        logger.info("Cache cleared")
