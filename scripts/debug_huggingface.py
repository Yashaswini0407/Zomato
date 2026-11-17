"""
Script to debug Hugging Face dataset loading
"""

import sys
from datasets import load_dataset

print("=" * 60)
print("Hugging Face Dataset Debug")
print("=" * 60)

dataset_id = "ManikaSaini/zomato-restaurant-recommendation"

print(f"\nAttempting to load dataset: {dataset_id}")

try:
    # Try loading without specifying split
    print("\n1. Loading dataset (no split specified)...")
    dataset = load_dataset(dataset_id)
    print(f"Dataset type: {type(dataset)}")
    print(f"Dataset keys: {dataset.keys() if hasattr(dataset, 'keys') else 'N/A'}")
    
    if hasattr(dataset, 'keys'):
        for split in dataset.keys():
            print(f"\n2. Loading split: {split}")
            split_data = dataset[split]
            print(f"   Split type: {type(split_data)}")
            print(f"   Split length: {len(split_data)}")
            
            if len(split_data) > 0:
                print(f"   First item: {split_data[0]}")
                print(f"   Columns: {split_data.column_names}")
            else:
                print("   WARNING: Split is empty!")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Trying alternative datasets...")
print("=" * 60)

# Try some other Zomato datasets
alternative_datasets = [
    "ashishkumar10/Zomato-Restaurant-Dataset",
    "akshaypawar7/zomato-dataset",
]

for alt_id in alternative_datasets:
    print(f"\nTrying: {alt_id}")
    try:
        dataset = load_dataset(alt_id)
        print(f"  SUCCESS! Type: {type(dataset)}")
        if hasattr(dataset, 'keys'):
            print(f"  Splits: {list(dataset.keys())}")
            for split in dataset.keys():
                print(f"  {split}: {len(dataset[split])} rows")
    except Exception as e:
        print(f"  FAILED: {e}")
