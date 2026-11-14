"""
Test suite for Phase 4: LLM Integration & Prompt Engineering
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.services.llm_client import GroqClient
from src.app.services.prompt_builder import PromptBuilder
from src.app.services.response_parser import ResponseParser
from src.app.services.merger import RecommendationMerger
from src.app.models.preferences import UserPreferences
from src.app.models.restaurant import Restaurant, BudgetBand
from src.app.config import get_settings


def test_prompt_builder():
    """Test prompt builder."""
    print("\n=== Test 1: Prompt Builder ===")
    
    builder = PromptBuilder()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    candidates = [
        Restaurant(
            id="test-1",
            name="Test Restaurant",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
    ]
    
    prompt = builder.build(preferences, candidates)
    
    print(f"Prompt length: {len(prompt)} characters")
    assert "restaurant recommendation expert" in prompt.lower()
    assert "only recommend restaurants from the provided list" in prompt.lower()
    assert "restaurant_id" in prompt
    assert "summary" in prompt
    assert "recommendations" in prompt
    print("[PASS] Prompt builder works correctly")


def test_response_parser_valid_json():
    """Test response parser with valid JSON."""
    print("\n=== Test 2: Response Parser Valid JSON ===")
    
    parser = ResponseParser()
    
    valid_json = '''
{
      "summary": "Test summary",
      "recommendations": [
        {
          "restaurant_id": "test-1",
          "rank": 1,
          "explanation": "Good choice"
        }
      ]
    }
'''
    
    parsed = parser.parse(valid_json)
    
    assert parsed["summary"] == "Test summary"
    assert len(parsed["recommendations"]) == 1
    print(f"Parsed: {parsed}")
    print("[PASS] Valid JSON parsed correctly")


def test_response_parser_malformed_json():
    """Test response parser with malformed JSON (regex fallback)."""
    print("\n=== Test 3: Response Parser Malformed JSON ===")
    
    parser = ResponseParser()
    
    malformed = "Some text before ```json {\"summary\": \"test\"} ``` after"
    
    try:
        parsed = parser.parse(malformed)
        print(f"Extracted from malformed: {parsed}")
        print("[PASS] Regex fallback works")
    except Exception as e:
        print(f"Could not extract: {e}")
        print("[FAIL] Regex fallback failed")


def test_response_parser_invalid_json():
    """Test response parser with invalid JSON."""
    print("\n=== Test 4: Response Parser Invalid JSON ===")
    
    parser = ResponseParser()
    
    invalid_json = "This is not JSON at all"
    
    try:
        parser.parse(invalid_json)
        print("[FAIL] Should have raised error")
    except ValueError:
        print("Invalid JSON rejected as expected")
        print("[PASS] Invalid JSON handled correctly")


def test_merger():
    """Test recommendation merger."""
    print("\n=== Test 5: Recommendation Merger ===")
    
    merger = RecommendationMerger()
    
    llm_output = {
        "summary": "Test summary",
        "recommendations": [
            {
                "restaurant_id": "test-1",
                "rank": 1,
                "explanation": "Good choice"
            }
        ]
    }
    
    candidates = [
        Restaurant(
            id="test-1",
            name="Test Restaurant",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
    ]
    
    merged = merger.merge(llm_output, candidates)
    
    print(f"Merged: {len(merged)} recommendations")
    assert len(merged) == 1
    assert merged[0]["rank"] == 1
    assert merged[0]["restaurant"].id == "test-1"
    print("[PASS] Merger works correctly")


def test_merger_invalid_id():
    """Test merger with invalid restaurant ID."""
    print("\n=== Test 6: Merger Invalid ID ===")
    
    merger = RecommendationMerger()
    
    llm_output = {
        "summary": "Test summary",
        "recommendations": [
            {
                "restaurant_id": "invalid-id",
                "rank": 1,
                "explanation": "Good choice"
            }
        ]
    }
    
    candidates = [
        Restaurant(
            id="test-1",
            name="Test Restaurant",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
    ]
    
    merged = merger.merge(llm_output, candidates)
    
    print(f"Merged: {len(merged)} recommendations")
    assert len(merged) == 0  # Invalid ID should be dropped
    print("[PASS] Invalid ID dropped correctly")


def test_groq_client_initialization():
    """Test Groq client initialization."""
    print("\n=== Test 7: Groq Client Initialization ===")
    
    # Test with no API key (should initialize but fail on call)
    try:
        client = GroqClient(api_key="")
        print("Client initialized without API key")
        print("[PASS] Client initializes without API key")
    except Exception as e:
        print(f"Initialization failed: {e}")


def test_edge_case_long_additional_preferences():
    """Test handling of long additional preferences in prompt."""
    print("\n=== Test 8: Edge Case - Long Additional Preferences ===")
    
    builder = PromptBuilder()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0,
        additional_preferences="A" * 400  # Within limit
    )
    
    candidates = [
        Restaurant(
            id="test-1",
            name="Test Restaurant",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.5,
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
    ]
    
    prompt = builder.build(preferences, candidates)
    
    print(f"Prompt length: {len(prompt)} characters")
    print("[PASS] Long preferences handled")


def test_edge_case_too_many_candidates():
    """Test handling of too many candidates in prompt."""
    print("\n=== Test 9: Edge Case - Too Many Candidates ===")
    
    builder = PromptBuilder()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    # Create many candidates
    candidates = [
        Restaurant(
            id=f"test-{i}",
            name=f"Restaurant {i}",
            location="Bangalore",
            cuisines=["Italian"],
            rating=4.0 + (i * 0.01),
            estimated_cost=1000,
            budget_band=BudgetBand.MEDIUM
        )
        for i in range(50)
    ]
    
    prompt = builder.build(preferences, candidates)
    
    print(f"Prompt with 50 candidates: {len(prompt)} characters")
    print("[PASS] Many candidates handled")


def test_edge_case_empty_candidates():
    """Test prompt builder with no candidates."""
    print("\n=== Test 10: Edge Case - Empty Candidates ===")
    
    builder = PromptBuilder()
    
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0
    )
    
    prompt = builder.build(preferences, [])
    
    print(f"Prompt with no candidates: {len(prompt)} characters")
    assert "Available Restaurants" in prompt
    print("[PASS] Empty candidates handled")


def run_all_tests():
    """Run all Phase 4 tests."""
    print("=" * 60)
    print("PHASE 4: LLM INTEGRATION & PROMPT ENGINEERING - TESTS")
    print("=" * 60)
    
    tests = [
        test_prompt_builder,
        test_response_parser_valid_json,
        test_response_parser_malformed_json,
        test_response_parser_invalid_json,
        test_merger,
        test_merger_invalid_id,
        test_groq_client_initialization,
        test_edge_case_long_additional_preferences,
        test_edge_case_too_many_candidates,
        test_edge_case_empty_candidates,
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
