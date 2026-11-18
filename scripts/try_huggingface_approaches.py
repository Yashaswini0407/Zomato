"""
Script to try multiple approaches to get restaurant data from Hugging Face
"""

import sys
from datasets import load_dataset
import pandas as pd

print("=" * 60)
print("Hugging Face Dataset - Multiple Approaches")
print("=" * 60)

# Approach 1: Try the original dataset with different parameters
print("\n=== Approach 1: Original dataset with force_download ===")
try:
    dataset = load_dataset(
        "ManikaSaini/zomato-restaurant-recommendation",
        split="train",
        force_download=True,
        trust_remote_code=True
    )
    print(f"SUCCESS! Length: {len(dataset)}")
    print(f"Columns: {dataset.column_names}")
    print(f"First row: {dataset[0]}")
except Exception as e:
    print(f"FAILED: {e}")

# Approach 2: Try loading directly without split
print("\n=== Approach 2: Load without split ===")
try:
    dataset = load_dataset(
        "ManikaSaini/zomato-restaurant-recommendation",
        trust_remote_code=True
    )
    print(f"Dataset type: {type(dataset)}")
    if hasattr(dataset, 'keys'):
        print(f"Keys: {list(dataset.keys())}")
        for key in dataset.keys():
            print(f"  {key}: {len(dataset[key])} rows")
            if len(dataset[key]) > 0:
                print(f"  Columns: {dataset[key].column_names}")
                print(f"  First row: {dataset[key][0]}")
except Exception as e:
    print(f"FAILED: {e}")

# Approach 3: Try other restaurant datasets
print("\n=== Approach 3: Try other restaurant datasets ===")

other_datasets = [
    "Amod/food_delivery",
    "food101",  # Food images dataset
    "recipe_nlg",  # Recipe dataset
]

for dataset_id in other_datasets:
    print(f"\nTrying: {dataset_id}")
    try:
        dataset = load_dataset(dataset_id, split="train")
        print(f"  SUCCESS! Length: {len(dataset)}")
        print(f"  Columns: {dataset.column_names}")
        # Check if it has restaurant-like data
        if len(dataset) > 0:
            print(f"  First row: {dataset[0]}")
    except Exception as e:
        print(f"  FAILED: {str(e)[:100]}")

# Approach 4: Try to clear cache and reload
print("\n=== Approach 4: Clear cache and reload ===")
try:
    import shutil
    from pathlib import Path
    cache_dir = Path.home() / ".cache" / "huggingface" / "datasets"
    if cache_dir.exists():
        print(f"Cache directory exists: {cache_dir}")
        # Don't actually delete, just check
        print(f"Cache size: {sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file()) / 1024 / 1024:.2f} MB")
    
    dataset = load_dataset(
        "ManikaSaini/zomato-restaurant-recommendation",
        split="train",
        cache_dir=None  # Use default cache
    )
    print(f"SUCCESS! Length: {len(dataset)}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n" + "=" * 60)
print("Conclusion: If all approaches failed, we need to use synthetic data")
print("=" * 60)
