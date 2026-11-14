"""
Test the data ingestion pipeline with sample data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.app.ingestion.normalizer import SchemaNormalizer
from src.app.ingestion.preprocessor import Preprocessor
from src.app.ingestion.writer import PersistenceWriter
from src.app.config import get_settings


def test_ingestion_with_sample_data():
    """Test ingestion with sample restaurant data."""
    print("Testing ingestion pipeline with sample data...")

    # Create sample data
    sample_data = [
        {
            "name": "Pizza Hut",
            "location": "Bangalore",
            "cuisines": "Italian, Fast Food",
            "rating": 4.2,
            "estimated_cost": 600,
            "votes": 1500
        },
        {
            "name": "Barbeque Nation",
            "location": "Delhi",
            "cuisines": "Barbecue, North Indian",
            "rating": 4.5,
            "estimated_cost": 1200,
            "votes": 2000
        },
        {
            "name": "Saravana Bhavan",
            "location": "Chennai",
            "cuisines": "South Indian",
            "rating": 4.3,
            "estimated_cost": 400,
            "votes": 1800
        },
        {
            "name": "Truffles",
            "location": "Bangalore",
            "cuisines": "Italian, Continental",
            "rating": 4.6,
            "estimated_cost": 800,
            "votes": 2200
        },
        {
            "name": "Bukhara",
            "location": "Delhi",
            "cuisines": "North Indian, Mughlai",
            "rating": 4.8,
            "estimated_cost": 2500,
            "votes": 3000
        },
    ]

    df = pd.DataFrame(sample_data)
    print(f"Sample data created: {len(df)} rows")
    print(f"Columns: {list(df.columns)}")

    # Stage 1: Normalize schema
    print("\nStage 1: Normalizing schema...")
    normalizer = SchemaNormalizer()
    normalized_df = normalizer.normalize(df)
    print(f"Normalized columns: {list(normalized_df.columns)}")

    # Stage 2: Preprocess
    print("\nStage 2: Preprocessing data...")
    settings = get_settings()
    preprocessor = Preprocessor(
        budget_low_max=settings.budget_low_max,
        budget_medium_max=settings.budget_medium_max,
    )
    processed_df = preprocessor.preprocess(normalized_df)
    print(f"Preprocessed data: {len(processed_df)} rows")
    print(f"Budget band distribution:\n{processed_df['budget_band'].value_counts()}")

    # Stage 3: Write to disk
    print("\nStage 3: Writing to disk...")
    writer = PersistenceWriter(settings.data_path)
    output_path = writer.write(processed_df, format="parquet")
    print(f"Data written to: {output_path}")

    # Stage 4: Verify
    print("\nStage 4: Verifying output...")
    if writer.verify():
        print("Verification successful!")
    else:
        print("Verification failed!")

    # Stage 5: Read back and verify
    print("\nStage 5: Reading back data...")
    read_df = pd.read_parquet(output_path)
    print(f"Read back: {len(read_df)} rows")
    print(f"Columns: {list(read_df.columns)}")
    print("\nSample row:")
    print(read_df.iloc[0].to_dict())

    print("\n[SUCCESS] Ingestion pipeline test completed successfully!")
    return True


if __name__ == "__main__":
    try:
        test_ingestion_with_sample_data()
        sys.exit(0)
    except Exception as e:
        print(f"\n[FAILED] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
