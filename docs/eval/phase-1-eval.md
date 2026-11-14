# Phase 1 Evaluation Criteria: Data Ingestion Pipeline

## Overview
This document defines the evaluation criteria for Phase 1: Data Ingestion Pipeline.

## Success Criteria

### 1. Dataset Loading
- [ ] DatasetLoader successfully fetches from Hugging Face
- [ ] Handles authentication if required
- [ ] Implements retry logic for network failures
- [ ] Shows progress during download

**Evaluation Method**:
```python
from app.ingestion.loader import DatasetLoader
loader = DatasetLoader()
dataset = loader.load_dataset("ManikaSaini/zomato-restaurant-recommendation")
assert dataset is not None
assert len(dataset) > 0
```

**Pass Criteria**: Dataset loads successfully, retry logic works

---

### 2. Schema Normalization
- [ ] SchemaNormalizer maps raw columns to canonical fields
- [ ] Handles missing columns gracefully
- [ ] Logs warnings for unexpected columns
- [ ] Preserves metadata for extra columns

**Evaluation Method**:
```python
from app.ingestion.normalizer import SchemaNormalizer
normalizer = SchemaNormalizer()
normalized = normalizer.normalize(raw_data)
assert 'name' in normalized.columns
assert 'location' in normalized.columns
assert 'cuisines' in normalized.columns
```

**Pass Criteria**: All required fields present, mapping correct

---

### 3. Data Preprocessing
- [ ] Preprocessor cleans null values appropriately
- [ ] Normalizes location strings
- [ ] Parses cuisine lists correctly
- [ ] Maps budget bands based on cost thresholds
- [ ] Validates data ranges (rating 0-5, cost >= 0)

**Evaluation Method**:
```python
from app.ingestion.preprocessor import Preprocessor
preprocessor = Preprocessor()
processed = preprocessor.preprocess(normalized_data)
# Check no nulls in critical fields
assert processed['name'].notna().all()
assert processed['rating'].between(0, 5).all()
assert processed['budget_band'].isin(['low', 'medium', 'high']).all()
```

**Pass Criteria**: Data is clean, valid, and properly transformed

---

### 4. Persistence
- [ ] PersistenceWriter writes to Parquet format
- [ ] File is created in data/processed/
- [ ] File integrity verified after write
- [ ] Supports SQLite as fallback

**Evaluation Method**:
```python
from app.ingestion.writer import PersistenceWriter
writer = PersistenceWriter()
writer.write(processed_data, 'data/processed/restaurants.parquet')
# Verify file exists and is readable
import os
assert os.path.exists('data/processed/restaurants.parquet')
```

**Pass Criteria**: File created, readable, data intact

---

### 5. Ingestion Pipeline
- [ ] IngestionPipeline orchestrates all steps
- [ ] CLI script `scripts/ingest.py` works
- [ ] Progress indicators show during processing
- [ ] Logging captures all stages

**Evaluation Method**:
```bash
python scripts/ingest.py
# Should show progress and complete successfully
```

**Pass Criteria**: Pipeline runs end-to-end without errors

---

### 6. Domain Models
- [ ] Restaurant model defined with all fields
- [ ] BudgetBand enum defined (low, medium, high)
- [ ] Validation methods work correctly
- [ ] Pydantic validation works

**Evaluation Method**:
```python
from app.models.restaurant import Restaurant, BudgetBand
restaurant = Restaurant(
    id="test",
    name="Test Restaurant",
    location="Test City",
    cuisines=["Italian"],
    rating=4.5,
    estimated_cost=1000,
    budget_band=BudgetBand.MEDIUM
)
assert restaurant.budget_band == BudgetBand.MEDIUM
```

**Pass Criteria**: Models validate correctly, all fields present

---

## Functional Tests

### Test 1: Full Ingestion Pipeline
```bash
# Run complete ingestion
python scripts/ingest.py

# Verify output
python -c "
import pandas as pd
df = pd.read_parquet('data/processed/restaurants.parquet')
print(f'Total restaurants: {len(df)}')
print(f'Columns: {list(df.columns)}')
assert len(df) > 0
assert 'name' in df.columns
assert 'location' in df.columns
print('Ingestion successful')
"
```

**Expected Output**: Ingestion completes, file created with data

**Pass/Fail**: Pass if ingestion completes and data is valid

---

### Test 2: Null Value Handling
```python
# Test with data containing nulls
test_data = pd.DataFrame({
    'name': ['Rest1', None, 'Rest3'],
    'location': ['City1', 'City2', 'City3'],
    'rating': [4.0, 3.5, None]
})
processed = preprocessor.preprocess(test_data)
# Should skip rows with null critical fields
assert processed['name'].notna().all()
```

**Expected**: Rows with null critical fields removed

**Pass/Fail**: Pass if nulls handled correctly

---

### Test 3: Budget Band Mapping
```python
# Test budget band assignment
test_costs = [300, 800, 2000]
expected_bands = ['low', 'medium', 'high']
for cost, expected in zip(test_costs, expected_bands):
    band = preprocessor.map_budget_band(cost)
    assert band == expected, f"Cost {cost} should map to {expected}"
```

**Expected**: Correct budget band assignment

**Pass/Fail**: Pass if all mappings correct

---

### Test 4: Cuisine Parsing
```python
# Test cuisine string parsing
test_cuisines = [
    "Italian, Chinese",
    "Italian; Chinese",
    "Italian / Chinese"
]
for cuisine_str in test_cuisines:
    cuisines = preprocessor.parse_cuisines(cuisine_str)
    assert 'italian' in cuisines
    assert 'chinese' in cuisines
```

**Expected**: Cuisines parsed correctly from various formats

**Pass/Fail**: Pass if parsing handles all formats

---

## Quality Checks

### Data Quality
- [ ] No duplicate restaurants (same name + location)
- [ ] All ratings in valid range [0, 5]
- [ ] All costs are non-negative
- [ ] All budget bands are valid
- [ ] No null values in critical fields (name, location, rating)

**Evaluation Method**:
```python
df = pd.read_parquet('data/processed/restaurants.parquet')
# Check for duplicates
duplicates = df.duplicated(subset=['name', 'location'])
assert not duplicates.any(), "Duplicates found"
# Check ranges
assert df['rating'].between(0, 5).all(), "Invalid ratings"
assert (df['estimated_cost'] >= 0).all(), "Negative costs"
```

**Pass Criteria**: All data quality checks pass

---

### Code Quality
- [ ] Code follows PEP 8
- [ ] Type hints used
- [ ] Comprehensive docstrings
- [ ] Error handling with clear messages

**Evaluation Method**: Code review and linting

**Pass Criteria**: Code passes linting, well-documented

---

## Edge Case Handling

### Edge Case 1: Dataset Not Found
**Scenario**: Invalid dataset ID

**Expected**: Clear error with dataset URL and instructions

**Test**:
```python
loader = DatasetLoader()
try:
    loader.load_dataset("invalid/dataset-id")
except Exception as e:
    assert "dataset" in str(e).lower()
    print("Correct error raised")
```

**Pass/Fail**: Pass if error message is clear and helpful

---

### Edge Case 2: Missing Columns
**Scenario**: Dataset missing expected columns

**Expected**: Log warning, use defaults or fail gracefully

**Test**: Test with dataset missing 'rating' column

**Expected**: Warning logged, appropriate handling

**Pass/Fail**: Pass if handled gracefully with logging

---

### Edge Case 3: Invalid Rating Values
**Scenario**: Rating values outside [0, 5]

**Expected**: Clamp to valid range, log warnings

**Test**:
```python
test_data = pd.DataFrame({'rating': [-1, 3.5, 6.0]})
processed = preprocessor.preprocess(test_data)
assert processed['rating'].between(0, 5).all()
```

**Pass/Fail**: Pass if values clamped correctly

---

### Edge Case 4: Network Timeout
**Scenario**: Network timeout during download

**Expected**: Retry with backoff, show progress

**Test**: Simulate network timeout (mock)

**Expected**: Retry logic activated, progress shown

**Pass/Fail**: Pass if retry works and progress shown

---

### Edge Case 5: Empty Dataset
**Scenario**: Dataset contains no rows

**Expected**: Raise error, prevent creating empty file

**Test**: Test with empty dataset

**Expected**: Error raised, no file created

**Pass/Fail**: Pass if error raised and no file created

---

## Performance Criteria

- [ ] Dataset download completes in < 3 minutes
- [ ] Data processing completes in < 2 minutes
- [ ] File write completes in < 30 seconds
- [ ] Total ingestion time < 5 minutes

**Evaluation Method**: Time the ingestion process

**Pass Criteria**: All operations complete within time limits

---

## Data Validation

### Schema Validation
- [ ] All required fields present: name, location, cuisines, rating, estimated_cost, budget_band
- [ ] Data types correct: strings, floats, lists
- [ ] No unexpected data types

**Evaluation Method**: Inspect schema of processed file

**Pass Criteria**: Schema matches specification

---

### Content Validation
- [ ] At least 100 restaurants in dataset
- [ ] Multiple locations represented
- [ ] Multiple cuisines represented
- [ ] Range of ratings present
- [ ] Range of costs present

**Evaluation Method**: Analyze processed data

**Pass Criteria**: Dataset is diverse and comprehensive

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Dataset loads from Hugging Face
- [ ] Data normalized and cleaned
- [ ] Processed file created in correct format
- [ ] All data quality checks pass
- [ ] CLI script works

### Should Have (Non-blocking)
- [ ] Progress indicators shown
- [ ] Comprehensive logging
- [ ] Retry logic implemented
- [ ] Error messages clear

### Nice to Have (Optional)
- [ ] Data validation report generated
- [ ] Statistics about dataset printed
- [ ] Support for incremental updates

---

## Sign-off

**Phase 1 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
