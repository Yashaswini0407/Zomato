"""
Test suite for Phase 2: Data Layer & Repository
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.app.data.repository import ParquetRepository, InMemoryRepository
from src.app.data.cached_repository import CachedRepository
from src.app.models.restaurant import Restaurant, BudgetBand
from src.app.models.filters import FilterCriteria
from src.app.config import get_settings


def test_parquet_repository_load():
    """Test loading data from Parquet file."""
    print("\n=== Test 1: ParquetRepository Load ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    restaurants = repo.get_all()
    print(f"Loaded {len(restaurants)} restaurants")
    assert len(restaurants) > 0
    print("[PASS] ParquetRepository loads data successfully")


def test_parquet_repository_filter_location():
    """Test filtering by location."""
    print("\n=== Test 2: ParquetRepository Filter by Location ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(location="Bangalore")
    results = repo.filter(criteria)
    
    print(f"Restaurants in Bangalore: {len(results)}")
    assert all("bangalore" in r.location.lower() for r in results)
    print("[PASS] Location filter works correctly")


def test_parquet_repository_filter_budget():
    """Test filtering by budget."""
    print("\n=== Test 3: ParquetRepository Filter by Budget ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(budget=BudgetBand.MEDIUM)
    results = repo.filter(criteria)
    
    print(f"Medium budget restaurants: {len(results)}")
    assert all(r.budget_band == BudgetBand.MEDIUM for r in results)
    print("[PASS] Budget filter works correctly")


def test_parquet_repository_filter_cuisine():
    """Test filtering by cuisine."""
    print("\n=== Test 4: ParquetRepository Filter by Cuisine ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(cuisine="italian")
    results = repo.filter(criteria)
    
    print(f"Italian restaurants: {len(results)}")
    assert all(any("italian" in c.lower() for c in r.cuisines) for r in results)
    print("[PASS] Cuisine filter works correctly")


def test_parquet_repository_filter_rating():
    """Test filtering by rating."""
    print("\n=== Test 5: ParquetRepository Filter by Rating ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(min_rating=4.0)
    results = repo.filter(criteria)
    
    print(f"Restaurants with rating >= 4.0: {len(results)}")
    assert all(r.rating >= 4.0 for r in results)
    print("[PASS] Rating filter works correctly")


def test_parquet_repository_combined_filters():
    """Test combined filters."""
    print("\n=== Test 6: ParquetRepository Combined Filters ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="italian",
        min_rating=4.0
    )
    results = repo.filter(criteria)
    
    print(f"Combined filter results: {len(results)}")
    assert all(
        "bangalore" in r.location.lower() and
        r.budget_band == BudgetBand.MEDIUM and
        any("italian" in c.lower() for c in r.cuisines) and
        r.rating >= 4.0
        for r in results
    )
    print("[PASS] Combined filters work correctly")


def test_parquet_repository_get_by_ids():
    """Test getting restaurants by IDs."""
    print("\n=== Test 7: ParquetRepository Get by IDs ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    all_restaurants = repo.get_all()
    test_ids = [r.id for r in all_restaurants[:3]]
    
    results = repo.get_by_ids(test_ids)
    
    print(f"Requested {len(test_ids)} IDs, got {len(results)} restaurants")
    assert len(results) == len(test_ids)
    assert all(r.id in test_ids for r in results)
    print("[PASS] Get by IDs works correctly")


def test_parquet_repository_get_locations():
    """Test getting unique locations."""
    print("\n=== Test 8: ParquetRepository Get Locations ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    locations = repo.get_locations()
    
    print(f"Unique locations: {len(locations)}")
    print(f"Locations: {locations}")
    assert isinstance(locations, list)
    assert len(locations) > 0
    print("[PASS] Get locations works correctly")


def test_parquet_repository_get_cuisines():
    """Test getting unique cuisines."""
    print("\n=== Test 9: ParquetRepository Get Cuisines ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    cuisines = repo.get_cuisines()
    
    print(f"Unique cuisines: {len(cuisines)}")
    print(f"Cuisines: {cuisines}")
    assert isinstance(cuisines, list)
    assert len(cuisines) > 0
    print("[PASS] Get cuisines works correctly")


def test_in_memory_repository():
    """Test in-memory repository."""
    print("\n=== Test 10: InMemoryRepository ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Test Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-2",
            name="Test Restaurant 2",
            location="Delhi",
            cuisines=["Chinese"],
            rating=4.0,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    
    # Test get_all
    all_restaurants = repo.get_all()
    assert len(all_restaurants) == 2
    
    # Test filter
    criteria = FilterCriteria(location="Bangalore")
    results = repo.filter(criteria)
    assert len(results) == 1
    assert results[0].location == "Bangalore"
    
    print("[PASS] InMemoryRepository works correctly")


def test_cached_repository():
    """Test cached repository."""
    print("\n=== Test 11: CachedRepository ===")
    
    settings = get_settings()
    base_repo = ParquetRepository(settings.data_path)
    cached_repo = CachedRepository(base_repo, maxsize=10)
    
    # First call - cache miss
    criteria = FilterCriteria(location="Bangalore")
    results1 = cached_repo.filter(criteria)
    
    # Second call - cache hit
    results2 = cached_repo.filter(criteria)
    
    stats = cached_repo.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    assert stats["hits"] >= 1
    assert stats["misses"] >= 1
    assert len(results1) == len(results2)
    
    print("[PASS] CachedRepository works correctly")


def test_filter_criteria_validation():
    """Test FilterCriteria validation."""
    print("\n=== Test 12: FilterCriteria Validation ===")
    
    # Valid criteria
    criteria = FilterCriteria(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    assert criteria.location == "Bangalore"
    assert criteria.budget == BudgetBand.MEDIUM
    
    # Invalid rating
    try:
        FilterCriteria(min_rating=10.0)
        assert False, "Should have raised validation error"
    except Exception:
        print("Invalid rating rejected as expected")
    
    print("[PASS] FilterCriteria validation works correctly")


def test_edge_case_empty_result():
    """Test handling of empty result set."""
    print("\n=== Test 13: Edge Case - Empty Result ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    criteria = FilterCriteria(location="NonexistentCity")
    results = repo.filter(criteria)
    
    print(f"Results for nonexistent location: {len(results)}")
    assert results == []
    print("[PASS] Empty result handled correctly")


def test_edge_case_invalid_rating():
    """Test handling of invalid rating in filter."""
    print("\n=== Test 14: Edge Case - Invalid Rating ===")
    
    settings = get_settings()
    repo = ParquetRepository(settings.data_path)
    
    # Rating should be clamped to [0, 5] by validation
    criteria = FilterCriteria(min_rating=4.5)
    results = repo.filter(criteria)
    
    print(f"Results with min_rating=4.5: {len(results)}")
    assert all(r.rating >= 4.5 for r in results)
    print("[PASS] Invalid rating handled correctly")


def run_all_tests():
    """Run all Phase 2 tests."""
    print("=" * 60)
    print("PHASE 2: DATA LAYER & REPOSITORY - TESTS")
    print("=" * 60)
    
    tests = [
        test_parquet_repository_load,
        test_parquet_repository_filter_location,
        test_parquet_repository_filter_budget,
        test_parquet_repository_filter_cuisine,
        test_parquet_repository_filter_rating,
        test_parquet_repository_combined_filters,
        test_parquet_repository_get_by_ids,
        test_parquet_repository_get_locations,
        test_parquet_repository_get_cuisines,
        test_in_memory_repository,
        test_cached_repository,
        test_filter_criteria_validation,
        test_edge_case_empty_result,
        test_edge_case_invalid_rating,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[FAILED] {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
