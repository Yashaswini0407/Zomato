"""
Integration test for Phase 4: Real LLM API calls
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file explicitly
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from src.app.services.llm_client import GroqClient
from src.app.services.prompt_builder import PromptBuilder
from src.app.services.response_parser import ResponseParser
from src.app.services.merger import RecommendationMerger
from src.app.models.preferences import UserPreferences
from src.app.models.restaurant import Restaurant, BudgetBand
from src.app.config import get_settings


def test_real_llm_api_call():
    """Test actual API call to Groq."""
    print("\n=== Test 1: Real LLM API Call ===")
    
    settings = get_settings()
    print(f"LLM Provider: {settings.llm_provider}")
    print(f"LLM Model: {settings.llm_model}")
    print(f"API Key: {'Present' if settings.llm_api_key else 'Missing'}")
    print(f"API Key Length: {len(settings.llm_api_key) if settings.llm_api_key else 0}")
    print(f"API Key Prefix: {settings.llm_api_key[:10] if settings.llm_api_key else 'N/A'}...")
    
    if not settings.llm_api_key:
        print("[SKIP] No API key found in .env file")
        return
    
    client = GroqClient()
    
    # Simple test prompt
    test_prompt = "What is 2+2? Answer with just the number."
    
    try:
        response = client.complete(test_prompt)
        print(f"Response: {response}")
        assert "4" in response or "four" in response.lower()
        print("[PASS] Real API call successful")
    except Exception as e:
        print(f"[FAILED] API call failed: {e}")
        raise


def test_full_recommendation_flow():
    """Test the full recommendation flow with real LLM."""
    print("\n=== Test 2: Full Recommendation Flow ===")
    
    settings = get_settings()
    if not settings.llm_api_key:
        print("[SKIP] No API key found in .env file")
        return
    
    # Create sample restaurants
    candidates = [
        Restaurant(
            id="bangalore-pizza-hut",
            name="Pizza Hut",
            location="Bangalore",
            cuisines=["italian", "fast food"],
            rating=4.2,
            estimated_cost=600,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="bangalore-truffles",
            name="Truffles",
            location="Bangalore",
            cuisines=["italian", "continental"],
            rating=4.6,
            estimated_cost=800,
            budget_band=BudgetBand.MEDIUM
        ),
        Restaurant(
            id="bangalore-italiano",
            name="Italiano",
            location="Bangalore",
            cuisines=["italian"],
            rating=4.0,
            estimated_cost=700,
            budget_band=BudgetBand.MEDIUM
        ),
    ]
    
    # User preferences
    preferences = UserPreferences(
        location="Bangalore",
        budget=BudgetBand.MEDIUM,
        cuisine="Italian",
        min_rating=4.0,
        top_k=2
    )
    
    # Build prompt
    builder = PromptBuilder()
    prompt = builder.build(preferences, candidates)
    print(f"Prompt built: {len(prompt)} characters")
    
    # Call LLM
    client = GroqClient()
    try:
        llm_response = client.complete(prompt, temperature=0.3, max_tokens=1024)
        print(f"LLM Response: {llm_response[:200]}...")
        
        # Parse response
        parser = ResponseParser()
        parsed = parser.parse(llm_response)
        print(f"Parsed: {parsed}")
        
        # Validate schema
        is_valid = parser.validate_schema(parsed)
        print(f"Schema valid: {is_valid}")
        
        if is_valid:
            # Merge with restaurant data
            merger = RecommendationMerger()
            merged = merger.merge(parsed, candidates)
            print(f"Merged recommendations: {len(merged)}")
            
            for rec in merged:
                print(f"\nRank {rec['rank']}: {rec['restaurant'].name}")
                print(f"Explanation: {rec['explanation']}")
            
            print("[PASS] Full recommendation flow successful")
        else:
            print("[FAILED] Schema validation failed")
            
    except Exception as e:
        print(f"[FAILED] Full flow failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_groq_client_with_real_api():
    """Test GroqClient with real API key."""
    print("\n=== Test 3: GroqClient with Real API ===")
    
    settings = get_settings()
    if not settings.llm_api_key:
        print("[SKIP] No API key found in .env file")
        return
    
    client = GroqClient()
    
    # Test with a more complex prompt
    prompt = "Recommend a good Italian restaurant in Bangalore. Keep it brief."
    
    try:
        response = client.complete(prompt, temperature=0.5, max_tokens=200)
        print(f"Response: {response}")
        assert len(response) > 0
        print("[PASS] GroqClient works with real API")
    except Exception as e:
        print(f"[FAILED] GroqClient failed: {e}")
        raise


def test_error_handling_invalid_key():
    """Test error handling with invalid API key."""
    print("\n=== Test 4: Error Handling ===")
    
    # Test with empty API key
    try:
        client = GroqClient(api_key="")
        client.complete("Test")
        print("[FAILED] Should have raised error for empty API key")
    except Exception as e:
        print(f"Expected error: {e}")
        print("[PASS] Error handling works correctly")


def run_all_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("PHASE 4: LLM INTEGRATION - REAL API TESTS")
    print("=" * 60)
    
    tests = [
        test_real_llm_api_call,
        test_full_recommendation_flow,
        test_groq_client_with_real_api,
        test_error_handling_invalid_key,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[FAILED] {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
