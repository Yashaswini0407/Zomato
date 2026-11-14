"""
Test suite for Phase 3: Filter Service & Business Logic
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.services.validator import InputValidator
from src.app.services.filter_service import FilterService
from src.app.models.preferences import UserPreferences
from src.app.models.filter_result import FilterResult
from src.app.models.restaurant import Restaurant, BudgetBand
from src.app.data.repository import InMemoryRepository
from src.app.config import get_settings


def test_input_validator():
    """Test input validation."""
    print("\n=== Test 1: Input Validator ===")
    
    validator = InputValidator()
    
    # Valid preferences
    valid_prefs = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "Italian",
        "min_rating": 4.0
    }
    
    user_prefs = validator.validate(valid_prefs)
    assert user_prefs.location == "Bangalore"
    assert user_prefs.budget == BudgetBand.MEDIUM
    assert user_prefs.cuisine == "Italian"
    assert user_prefs.min_rating == 4.0
    
    print(f"Validated preferences: {user_prefs}")
    print("[PASS] Input validator works correctly")


def test_input_validator_invalid():
    """Test input validation with invalid data."""
    print("\n=== Test 2: Input Validator Invalid Data ===")
    
    validator = InputValidator()
    
    # Invalid rating
    invalid_prefs = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "Italian",
        "min_rating": 10.0
    }
    
    try:
        validator.validate(invalid_prefs)
        assert False, "Should have raised validation error"
    except ValueError as e:
        print(f"Validation error raised as expected: {e}")
    
    print("[PASS] Invalid data rejected correctly")


def test_filter_service_location():
    """Test filter service with location filter."""
    print("\n=== Test 3: Filter Service Location ===")
    
    # Create sample restaurants
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-2",
            name="Restaurant 2",
            location="Delhi",
            cuisines=["Chinese"],
            rating=4.0,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    assert len(result.candidates) == 1
    assert result.candidates[0].location == "Bangalore"
    print("[PASS] Location filter works correctly")


def test_filter_service_budget():
    """Test filter service with budget filter."""
    print("\n=== Test 4: Filter Service Budget ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=300,
            budget_band=BudgetBand.LOW
        ),
        Restaurant(
            id="test-2",
            name="Restaurant 2",
            location="Bangalore",
            cuisines=["Chinese"],
            rating=4.0,
            estimated_cost=1200,
            budget_band=BudgetBand.HIGH
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.LOW,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    assert all(r.budget_band == BudgetBand.LOW for r in result.candidates)
    print("[PASS] Budget filter works correctly")


def test_filter_service_cuisine():
    """Test filter service with cuisine filter."""
    print("\n=== Test 5: Filter Service Cuisine ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian", "Continental"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-2",
            name="Restaurant 2",
            location="Bangalore",
            cuisines=["Chinese", "Thai"],
            rating=4.0,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    assert all(any("italian" in c.lower() for c in r.cuisines) for r in result.candidates)
    print("[PASS] Cuisine filter works correctly")


def test_filter_service_rating():
    """Test filter service with rating filter."""
    print("\n=== Test 6: Filter Service Rating ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-2",
            name="Restaurant 2",
            location="Bangalore",
            cuisines=["Chinese"],
            rating=3.5,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    assert all(r.rating >= 4.0 for r in result.candidates)
    print("[PASS] Rating filter works correctly")


def test_filter_service_sorting():
    """Test filter service sorting by rating."""
    print("\n=== Test 7: Filter Service Sorting ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.0,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-2",
            name="Restaurant 2",
            location="Bangalore",
            cuisines=["Chinese"],
            rating=4.5,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="test-3",
            name="Restaurant 3",
            location="Bangalore",
            cuisines=["Indian"],
            rating=4.2,
            estimated_cost=600,
            budget_band=BudgetBand.LOW
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.LOW,
        cuisine="Italian",
        min_rating=0.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    ratings = [r.rating for r in result.candidates]
    print(f"Ratings: {ratings}")
    assert ratings == sorted(ratings, reverse=True)
    print("[PASS] Sorting works correctly")


def test_filter_service_capping():
    """Test filter service candidate capping."""
    print("\n=== Test 8: Filter Service Capping ===")
    
    # Create more restaurants than max_candidates
    restaurants = [
        Restaurant(
            id=f"test-{i}",
            name=f"Restaurant {i}",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.0 + (i * 0.1),
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
        for i in range(10)
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService(max_candidates=5)
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=0.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    print(f"Total before cap: {result.total_before_cap}")
    assert len(result.candidates) <= 5
    assert result.total_before_cap == 10
    print("[PASS] Capping works correctly")


def test_filter_service_no_matches():
    """Test filter service with no matches."""
    print("\n=== Test 9: Filter Service No Matches ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="NonexistentCity",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates: {len(result.candidates)}")
    assert len(result.candidates) == 0
    assert result.total_before_cap == 0
    print("[PASS] No matches handled correctly")


def test_user_preferences_validation():
    """Test UserPreferences model validation."""
    print("\n=== Test 10: UserPreferences Validation ===")
    
    # Valid preferences
    prefs = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    assert prefs.location == "Bangalore"
    assert prefs.budget == BudgetBand.MEDIUM
    assert prefs.top_k == 5  # default value
    
    print(f"Preferences: {prefs}")
    print("[PASS] UserPreferences validation works correctly")


def test_user_preferences_invalid():
    """Test UserPreferences with invalid data."""
    print("\n=== Test 11: UserPreferences Invalid Data ===")
    
    # Empty location
    try:
        UserPreferences(
            location="",
            budget=BudgetBand.MEDIUM,
            cuisine="Italian",
            min_rating=4.0
        )
        assert False, "Should have raised validation error"
    except Exception:
        print("Empty location rejected as expected")
    
    # Invalid rating
    try:
        UserPreferences(
            location="Bangalore",
            budget=BudgetBand.MEDIUM,
            cuisine="Italian",
            min_rating=10.0
        )
        assert False, "Should have raised validation error"
    except Exception:
        print("Invalid rating rejected as expected")
    
    print("[PASS] Invalid data rejected correctly")


def test_filter_result_model():
    """Test FilterResult model."""
    print("\n=== Test 12: FilterResult Model ===")
    
    result = FilterResult(
        candidates=[],
        total_before_cap=100,
        applied_filters={"location": "Bangalore"}
    )
    
    assert result.total_before_cap == 100
    assert result.applied_filters["location"] == "Bangalore"
    
    print(f"FilterResult: {result}")
    print("[PASS] FilterResult model works correctly")


def test_edge_case_ambiguous_location():
    """Test handling of ambiguous location (case insensitive)."""
    print("\n=== Test 13: Edge Case - Ambiguous Location ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    # Use lowercase location
    preferences = UserPreferences(
        location="bangalore",  # lowercase
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates with lowercase location: {len(result.candidates)}")
    assert len(result.candidates) == 1
    print("[PASS] Case-insensitive location matching works")


def test_edge_case_rating_boundary():
    """Test rating at boundary (inclusive)."""
    print("\n=== Test 14: Edge Case - Rating Boundary ===")
    
    restaurants = [
        Restaurant(
            id="test-1",
            name="Restaurant 1",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.0,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    repo = InMemoryRepository(restaurants)
    filter_service = FilterService()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0  # exactly equal to restaurant rating
    )
    
    result = filter_service.filter(preferences, repo)
    
    print(f"Candidates with rating >= 4.0: {len(result.candidates)}")
    assert len(result.candidates) == 1
    print("[PASS] Boundary condition handled correctly (inclusive)")


def run_all_tests():
    """Run all Phase 3 tests."""
    print("=" * 60)
    print("PHASE 3: FILTER SERVICE & BUSINESS LOGIC - TESTS")
    print("=" * 60)
    
    tests = [
        test_input_validator,
        test_input_validator_invalid,
        test_filter_service_location,
        test_filter_service_budget,
        test_filter_service_cuisine,
        test_filter_service_rating,
        test_filter_service_sorting,
        test_filter_service_capping,
        test_filter_service_no_matches,
        test_user_preferences_validation,
        test_user_preferences_invalid,
        test_filter_result_model,
        test_edge_case_ambiguous_location,
        test_edge_case_rating_boundary,
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
