# Phase 2 Evaluation Criteria: Data Layer & Repository

## Overview
This document defines the evaluation criteria for Phase 2: Data Layer & Repository.

## Success Criteria

### 1. Repository Interface
- [ ] RestaurantRepository interface defined
- [ ] get_all() method returns all restaurants
- [ ] filter() method accepts FilterCriteria
- [ ] get_by_ids() method retrieves by IDs
- [ ] get_locations() returns unique locations
- [ ] get_cuisines() returns unique cuisines

**Evaluation Method**:
```python
from app.data.repository import RestaurantRepository
repo = RestaurantRepository('data/processed/restaurants.parquet')
all_restaurants = repo.get_all()
assert len(all_restaurants) > 0
```

**Pass Criteria**: All methods implemented and functional

---

### 2. Filter Criteria Model
- [ ] FilterCriteria model defined with all fields
- [ ] Pydantic validation works
- [ ] Optional fields handled correctly
- [ ] Type validation works

**Evaluation Method**:
```python
from app.models.filters import FilterCriteria
criteria = FilterCriteria(location="Bangalore", budget="medium")
assert criteria.location == "Bangalore"
assert criteria.budget == "medium"
```

**Pass Criteria**: Model validates correctly

---

### 3. Repository Implementation
- [ ] ParquetRepository loads Parquet files
- [ ] InMemoryRepository loads data into memory
- [ ] Lazy loading implemented for large datasets
- [ ] Indexing for frequently queried fields

**Evaluation Method**:
```python
from app.data.repository import ParquetRepository
repo = ParquetRepository('data/processed/restaurants.parquet')
restaurants = repo.get_all()
assert isinstance(restaurants, list)
```

**Pass Criteria**: Repository loads and returns data correctly

---

### 4. Caching Layer
- [ ] LRU cache implemented
- [ ] Cache invalidation strategy defined
- [ ] Cache statistics logged
- [ ] Cache improves performance

**Evaluation Method**:
```python
# Test cache performance
import time
start = time.time()
repo.get_all()
first_call = time.time() - start

start = time.time()
repo.get_all()
second_call = time.time() - start

assert second_call < first_call, "Cache should improve performance"
```

**Pass Criteria**: Cache improves performance on repeated calls

---

### 5. Data Validation
- [ ] Repository validates query parameters
- [ ] Handles empty results gracefully
- [ ] Invalid parameters raise clear errors

**Evaluation Method**:
```python
# Test invalid parameters
try:
    repo.filter(FilterCriteria(min_rating=10.0))  # Invalid rating
except ValueError as e:
    assert "rating" in str(e).lower()
```

**Pass Criteria**: Validation works with clear error messages

---

## Functional Tests

### Test 1: Load All Restaurants
```python
from app.data.repository import RestaurantRepository
repo = RestaurantRepository('data/processed/restaurants.parquet')
restaurants = repo.get_all()
print(f"Total restaurants: {len(restaurants)}")
assert len(restaurants) > 0
assert all(hasattr(r, 'name') for r in restaurants)
```

**Expected Output**: All restaurants loaded with required fields

**Pass/Fail**: Pass if data loads correctly

---

### Test 2: Filter by Location
```python
criteria = FilterCriteria(location="Bangalore")
results = repo.filter(criteria)
print(f"Restaurants in Bangalore: {len(results)}")
assert all(r.location.lower() == "bangalore" for r in results)
```

**Expected**: Only restaurants matching location

**Pass/Fail**: Pass if filter works correctly

---

### Test 3: Filter by Budget
```python
criteria = FilterCriteria(budget="medium")
results = repo.filter(criteria)
print(f"Medium budget restaurants: {len(results)}")
assert all(r.budget_band == "medium" for r in results)
```

**Expected**: Only restaurants matching budget band

**Pass/Fail**: Pass if filter works correctly

---

### Test 4: Filter by Cuisine
```python
criteria = FilterCriteria(cuisine="Italian")
results = repo.filter(criteria)
print(f"Italian restaurants: {len(results)}")
assert all(any("italian" in c.lower() for c in r.cuisines) for r in results)
```

**Expected**: Only restaurants with matching cuisine

**Pass/Fail**: Pass if filter works correctly

---

### Test 5: Filter by Rating
```python
criteria = FilterCriteria(min_rating=4.0)
results = repo.filter(criteria)
print(f"Restaurants with rating >= 4.0: {len(results)}")
assert all(r.rating >= 4.0 for r in results)
```

**Expected**: Only restaurants with rating >= min_rating

**Pass/Fail**: Pass if filter works correctly

---

### Test 6: Combined Filters
```python
criteria = FilterCriteria(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
results = repo.filter(criteria)
print(f"Combined filter results: {len(results)}")
assert all(
    r.location.lower() == "bangalore" and
    r.budget_band == "medium" and
    any("italian" in c.lower() for c in r.cuisines) and
    r.rating >= 4.0
    for r in results
)
```

**Expected**: Restaurants matching all criteria

**Pass/Fail**: Pass if combined filters work

---

### Test 7: Get by IDs
```python
test_ids = [r.id for r in repo.get_all()[:5]]
results = repo.get_by_ids(test_ids)
assert len(results) == 5
assert all(r.id in test_ids for r in results)
```

**Expected**: Correct restaurants returned for given IDs

**Pass/Fail**: Pass if ID lookup works

---

### Test 8: Get Locations
```python
locations = repo.get_locations()
print(f"Unique locations: {len(locations)}")
assert isinstance(locations, list)
assert len(locations) > 0
```

**Expected**: List of unique locations

**Pass/Fail**: Pass if locations returned

---

### Test 9: Get Cuisines
```python
cuisines = repo.get_cuisines()
print(f"Unique cuisines: {len(cuisines)}")
assert isinstance(cuisines, list)
assert len(cuisines) > 0
```

**Expected**: List of unique cuisines

**Pass/Fail**: Pass if cuisines returned

---

## Quality Checks

### Performance
- [ ] get_all() completes in < 1 second
- [ ] filter() completes in < 100ms
- [ ] get_by_ids() completes in < 50ms
- [ ] Cache improves performance by > 50%

**Evaluation Method**: Performance timing tests

**Pass Criteria**: All operations within time limits

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

### Edge Case 1: File Not Found
**Scenario**: Processed data file missing

**Expected**: FileNotFoundError with clear message

**Test**:
```python
try:
    repo = RestaurantRepository('nonexistent.parquet')
except FileNotFoundError as e:
    assert "file" in str(e).lower() or "not found" in str(e).lower()
```

**Pass/Fail**: Pass if error message is clear

---

### Edge Case 2: Empty Result Set
**Scenario**: Filter returns no results

**Expected**: Empty list returned, no error

**Test**:
```python
criteria = FilterCriteria(location="NonexistentCity")
results = repo.filter(criteria)
assert results == []
```

**Pass/Fail**: Pass if empty list returned

---

### Edge Case 3: Invalid Filter Criteria
**Scenario**: Invalid rating value

**Expected**: ValueError with clear message

**Test**:
```python
try:
    repo.filter(FilterCriteria(min_rating=10.0))
except ValueError as e:
    assert "rating" in str(e).lower()
```

**Pass/Fail**: Pass if validation error raised

---

### Edge Case 4: Location Not Found
**Scenario**: Location doesn't exist in dataset

**Expected**: Empty list returned

**Test**:
```python
results = repo.filter(FilterCriteria(location="Nonexistent"))
assert results == []
```

**Pass/Fail**: Pass if empty list returned

---

### Edge Case 5: Memory Constraints
**Scenario**: Dataset too large for memory

**Expected**: Lazy loading or chunked loading

**Test**: Test with large dataset

**Expected**: Memory usage controlled

**Pass/Fail**: Pass if memory efficient

---

## Performance Criteria

- [ ] Repository initialization < 500ms
- [ ] get_all() < 1s (in-memory)
- [ ] filter() < 100ms
- [ ] get_by_ids() < 50ms
- [ ] Cache hit < 10ms

**Evaluation Method**: Timing tests with various operations

**Pass Criteria**: All operations within time limits

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Repository loads processed data
- [ ] All filter operations work correctly
- [ ] Empty results handled gracefully
- [ ] Performance within targets
- [ ] Cache improves performance

### Should Have (Non-blocking)
- [ ] Comprehensive validation
- [ ] Clear error messages
- [ ] Logging for debugging
- [ ] Indexing implemented

### Nice to Have (Optional)
- [ ] Multiple backend support
- [ ] Query optimization
- [ ] Advanced caching strategies

---

## Sign-off

**Phase 2 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
