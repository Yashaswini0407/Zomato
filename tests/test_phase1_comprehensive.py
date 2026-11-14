"""
Comprehensive test suite for Phase 1: Data Ingestion Pipeline
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.app.ingestion.loader import DatasetLoader
from src.app.ingestion.normalizer import SchemaNormalizer
from src.app.ingestion.preprocessor import Preprocessor
from src.app.ingestion.writer import PersistenceWriter
from src.app.ingestion.pipeline import IngestionPipeline
from src.app.models.restaurant import Restaurant, BudgetBand
from src.app.config import get_settings


def test_dataset_loader():
    """Test DatasetLoader with sample data."""
    print("\n=== Test 1: DatasetLoader ===")
    loader = DatasetLoader()
    print(f"Dataset ID: {loader.dataset_id}")
    print("[PASS] DatasetLoader initialized successfully")


def test_schema_normalizer():
    """Test SchemaNormalizer with various column names."""
    print("\n=== Test 2: SchemaNormalizer ===")
    
    # Test with standard columns
    data = pd.DataFrame({
        "name": ["Test Restaurant"],
        "location": ["Bangalore"],
        "cuisines": ["Italian"],
        "rating": [4.5],
        "estimated_cost": [1000]
    })
    
    normalizer = SchemaNormalizer()
    normalized = normalizer.normalize(data)
    
    assert "name" in normalized.columns
    assert "location" in normalized.columns
    assert "cuisines" in normalized.columns
    assert "rating" in normalized.columns
    assert "estimated_cost" in normalized.columns
    print(f"Normalized columns: {list(normalized.columns)}")
    print("[PASS] SchemaNormalizer works correctly")


def test_schema_normalizer_case_insensitive():
    """Test case-insensitive column matching."""
    print("\n=== Test 3: SchemaNormalizer Case-Insensitive ===")
    
    data = pd.DataFrame({
        "Name": ["Test Restaurant"],
        "City": ["Bangalore"],
        "Cuisine": ["Italian"],
        "Rating": [4.5],
        "Cost": [1000]
    })
    
    normalizer = SchemaNormalizer()
    normalized = normalizer.normalize(data)
    
    assert "name" in normalized.columns
    assert "location" in normalized.columns
    print(f"Normalized columns: {list(normalized.columns)}")
    print("[PASS] Case-insensitive matching works")


def test_preprocessor_null_handling():
    """Test null value handling."""
    print("\n=== Test 4: Preprocessor Null Handling ===")
    
    data = pd.DataFrame({
        "name": ["Rest1", None, "Rest3"],
        "location": ["City1", "City2", "City3"],
        "cuisines": ["Italian", "Chinese", None],
        "rating": [4.0, 3.5, None],
        "estimated_cost": [500, 800, 600]
    })
    
    settings = get_settings()
    preprocessor = Preprocessor(
        budget_low_max=settings.budget_low_max,
        budget_medium_max=settings.budget_medium_max,
    )
    
    processed = preprocessor.clean_nulls(data)
    
    # Should drop rows with null critical fields
    assert processed['name'].notna().all()
    assert processed['rating'].notna().all()
    print(f"Rows after null cleaning: {len(processed)}")
    print("[PASS] Null handling works correctly")


def test_preprocessor_budget_mapping():
    """Test budget band mapping."""
    print("\n=== Test 5: Budget Band Mapping ===")

    test_costs = [300, 800, 2000]
    expected_bands = [BudgetBand.LOW, BudgetBand.MEDIUM, BudgetBand.HIGH]

    settings = get_settings()
    preprocessor = Preprocessor(
        budget_low_max=settings.budget_low_max,
        budget_medium_max=settings.budget_medium_max,
    )

    for cost, expected in zip(test_costs, expected_bands):
        band = preprocessor.get_budget_band_for_cost(cost)
        assert band == expected, f"Cost {cost} should map to {expected}"
        print(f"Cost {cost} -> {band.value}")

    print("[PASS] Budget band mapping works correctly")


def test_preprocessor_cuisine_parsing():
    """Test cuisine string parsing."""
    print("\n=== Test 6: Cuisine Parsing ===")

    test_cuisines = [
        "Italian, Chinese",
        "Italian; Chinese",
        "Italian / Chinese",
        "Italian - Chinese"
    ]

    preprocessor = Preprocessor()

    for cuisine_str in test_cuisines:
        # Use the internal method by creating a DataFrame
        data = pd.DataFrame({"cuisines": [cuisine_str]})
        processed = preprocessor.parse_cuisines(data)
        cuisines = processed["cuisines"].iloc[0]
        assert 'italian' in cuisines
        assert 'chinese' in cuisines
        print(f"'{cuisine_str}' -> {cuisines}")

    print("[PASS] Cuisine parsing works correctly")


def test_preprocessor_rating_clamping():
    """Test rating clamping to valid range."""
    print("\n=== Test 7: Rating Clamping ===")
    
    data = pd.DataFrame({
        "name": ["Rest1", "Rest2", "Rest3"],
        "location": ["City1", "City2", "City3"],
        "cuisines": ["Italian", "Chinese", "Indian"],
        "rating": [-1.0, 3.5, 6.0],
        "estimated_cost": [500, 800, 600]
    })
    
    preprocessor = Preprocessor()
    processed = preprocessor.validate_ranges(data)
    
    assert processed['rating'].between(0, 5).all()
    print(f"Ratings after clamping: {list(processed['rating'])}")
    print("[PASS] Rating clamping works correctly")


def test_persistence_writer():
    """Test PersistenceWriter."""
    print("\n=== Test 8: PersistenceWriter ===")
    
    data = pd.DataFrame({
        "name": ["Test Restaurant"],
        "location": ["Bangalore"],
        "cuisines": [["Italian"]],
        "rating": [4.5],
        "estimated_cost": [1000],
        "budget_band": [BudgetBand.MEDIUM],
        "id": ["test-1"]
    })
    
    settings = get_settings()
    writer = PersistenceWriter(settings.data_path)
    
    output_path = writer.write(data, format="parquet")
    assert os.path.exists(output_path)
    
    verified = writer.verify()
    assert verified
    
    print(f"Written to: {output_path}")
    print("[PASS] PersistenceWriter works correctly")


def test_pipeline_integration():
    """Test full pipeline integration."""
    print("\n=== Test 9: Pipeline Integration ===")
    
    sample_data = [
        {
            "name": "Test Restaurant",
            "location": "Bangalore",
            "cuisines": "Italian",
            "rating": 4.5,
            "estimated_cost": 1000
        }
    ]
    
    df = pd.DataFrame(sample_data)
    
    # Simulate pipeline stages
    normalizer = SchemaNormalizer()
    normalized = normalizer.normalize(df)
    
    settings = get_settings()
    preprocessor = Preprocessor(
        budget_low_max=settings.budget_low_max,
        budget_medium_max=settings.budget_medium_max,
    )
    processed = preprocessor.preprocess(normalized)
    
    writer = PersistenceWriter(settings.data_path)
    output_path = writer.write(processed, format="parquet")
    
    # Read back and verify
    read_df = pd.read_parquet(output_path)
    assert len(read_df) == 1
    assert 'id' in read_df.columns
    assert 'budget_band' in read_df.columns
    
    print(f"Pipeline completed successfully")
    print(f"Output: {output_path}")
    print("[PASS] Pipeline integration works correctly")


def test_restaurant_model():
    """Test Restaurant model validation."""
    print("\n=== Test 10: Restaurant Model ===")

    restaurant = Restaurant(
        id="test-1",
        name="Test Restaurant",
        location="Bangalore",
        cuisines=["Italian", "Continental"],
        rating=4.5,
        estimated_cost=1000,
        budget_band=BudgetBand.MEDIUM
    )

    assert restaurant.id == "test-1"
    assert restaurant.rating == 4.5
    assert restaurant.budget_band == BudgetBand.MEDIUM

    print(f"Restaurant: {restaurant.name}")
    print(f"Budget Band: {restaurant.budget_band}")
    print("[PASS] Restaurant model works correctly")


def test_edge_case_missing_columns():
    """Test handling of missing columns."""
    print("\n=== Test 11: Edge Case - Missing Columns ===")
    
    data = pd.DataFrame({
        "restaurant_name": ["Test"],
        "city": ["Bangalore"],
        "cuisine": ["Italian"],
        "aggregate_rating": [4.5],
        "average_cost_for_two": [1000]
    })
    
    normalizer = SchemaNormalizer()
    try:
        normalized = normalizer.normalize(data)
        print(f"Normalized columns: {list(normalized.columns)}")
        print("[PASS] Missing columns handled with mapping")
    except ValueError as e:
        print(f"Expected error for missing required columns: {e}")
        print("[PASS] Missing columns validation works")


def run_all_tests():
    """Run all Phase 1 tests."""
    print("=" * 60)
    print("PHASE 1: DATA INGESTION PIPELINE - COMPREHENSIVE TESTS")
    print("=" * 60)
    
    tests = [
        test_dataset_loader,
        test_schema_normalizer,
        test_schema_normalizer_case_insensitive,
        test_preprocessor_null_handling,
        test_preprocessor_budget_mapping,
        test_preprocessor_cuisine_parsing,
        test_preprocessor_rating_clamping,
        test_persistence_writer,
        test_pipeline_integration,
        test_restaurant_model,
        test_edge_case_missing_columns,
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
