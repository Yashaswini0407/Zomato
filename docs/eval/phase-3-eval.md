# Phase 3 Evaluation Criteria: Filter Service & Business Logic

## Overview
This document defines the evaluation criteria for Phase 3: Filter Service & Business Logic.

## Success Criteria

### 1. Filter Service
- [ ] FilterService applies all filters correctly
- [ ] Filters applied in correct order
- [ ] Post-filter sorting by rating works
- [ ] Candidate capping at MAX_CANDIDATES works
- [ ] FilterResult includes metadata

**Evaluation Method**:
```python
from app.services.filter_service import FilterService
from app.models.preferences import UserPreferences
from app.data.repository import RestaurantRepository

repo = RestaurantRepository('data/processed/restaurants.parquet')
filter_service = FilterService()

preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)

result = filter_service.filter(preferences, repo)
assert len(result.candidates) <= 30  # MAX_CANDIDATES
assert result.total_before_cap >= len(result.candidates)
```

**Pass Criteria**: Filter service works correctly with capping

---

### 2. Filter Result Model
- [ ] FilterResult model defined correctly
- [ ] Contains candidates list
- [ ] Contains total_before_cap
- [ ] Contains applied_filters dict

**Evaluation Method**:
```python
from app.models.filter_result import FilterResult
result = FilterResult(
    candidates=[],
    total_before_cap=100,
    applied_filters={'location': 'Bangalore'}
)
assert result.total_before_cap == 100
```

**Pass Criteria**: Model structure correct

---

### 3. User Preferences Model
- [ ] UserPreferences model with all fields
- [ ] Validation: location not empty
- [ ] Validation: budget is valid enum
- [ ] Validation: cuisine not empty
- [ ] Validation: min_rating in [0, 5]
- [ ] Validation: top_k in [1, 20]

**Evaluation Method**:
```python
from app.models.preferences import UserPreferences
from pydantic import ValidationError

# Valid preferences
prefs = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
assert prefs.location == "Bangalore"

# Invalid rating
try:
    UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=10.0
    )
    assert False, "Should have raised ValidationError"
except ValidationError:
    pass
```

**Pass Criteria**: Validation works correctly

---

### 4. Input Validation
- [ ] InputValidator validates all fields
- [ ] String normalization works
- [ ] Validation errors are clear

**Evaluation Method**:
```python
from app.services.validator import InputValidator
validator = InputValidator()

# Test normalization
normalized = validator.normalize_location("bangalore")
assert normalized == "Bangalore"  # Title case
```

**Pass Criteria**: Validation and normalization work

---

### 5. Logging & Debugging
- [ ] Each filter stage logged
- [ ] Filter counts logged
- [ ] Applied filters logged
- [ ] Debug mode available

**Evaluation Method**: Check log output during filtering

**Pass Criteria**: Logging provides useful debugging info

---

## Functional Tests

### Test 1: Location Filter
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=3.0
)
result = filter_service.filter(preferences, repo)
assert all(r.location.lower() == "bangalore" for r in result.candidates)
```

**Expected**: Only Bangalore restaurants

**Pass/Fail**: Pass if location filter works

---

### Test 2: Budget Filter
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="low",
    cuisine="Italian",
    min_rating=3.0
)
result = filter_service.filter(preferences, repo)
assert all(r.budget_band == "low" for r in result.candidates)
```

**Expected**: Only low budget restaurants

**Pass/Fail**: Pass if budget filter works

---

### Test 3: Cuisine Filter
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=3.0
)
result = filter_service.filter(preferences, repo)
assert all(any("italian" in c.lower() for c in r.cuisines) for r in result.candidates)
```

**Expected**: Only Italian restaurants

**Pass/Fail**: Pass if cuisine filter works

---

### Test 4: Rating Filter
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.5
)
result = filter_service.filter(preferences, repo)
assert all(r.rating >= 4.5 for r in result.candidates)
```

**Expected**: Only restaurants with rating >= 4.5

**Pass/Fail**: Pass if rating filter works

---

### Test 5: Sorting by Rating
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=3.0
)
result = filter_service.filter(preferences, repo)
ratings = [r.rating for r in result.candidates]
assert ratings == sorted(ratings, reverse=True)
```

**Expected**: Results sorted by rating descending

**Pass/Fail**: Pass if sorting works

---

### Test 6: Candidate Capping
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=0.0  # Low threshold to get many results
)
result = filter_service.filter(preferences, repo)
assert len(result.candidates) <= 30  # MAX_CANDIDATES
```

**Expected**: No more than 30 candidates

**Pass/Fail**: Pass if capping works

---

### Test 7: No Matches
```python
preferences = UserPreferences(
    location="NonexistentCity",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
result = filter_service.filter(preferences, repo)
assert len(result.candidates) == 0
```

**Expected**: Empty result set

**Pass/Fail**: Pass if no matches handled

---

### Test 8: Input Validation
```python
from pydantic import ValidationError

# Empty location
try:
    UserPreferences(
        location="",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0
    )
    assert False
except ValidationError:
    pass

# Invalid budget
try:
    UserPreferences(
        location="Bangalore",
        budget="invalid",
        cuisine="Italian",
        min_rating=4.0
    )
    assert False
except ValidationError:
    pass
```

**Expected**: Validation errors raised

**Pass/Fail**: Pass if validation works

---

## Quality Checks

### Code Quality
- [ ] Code follows PEP 8
- [ ] Type hints used
- [ ] Comprehensive docstrings
- [ ] Error handling with clear messages

**Evaluation Method**: Code review and linting

**Pass Criteria**: Code passes linting, well-documented

---

## Edge Case Handling

### Edge Case 1: No Matches After Filters
**Scenario**: All filters eliminate all candidates

**Expected**: Empty FilterResult, logged

**Test**: Test with impossible criteria

**Expected**: Empty result, no error

**Pass/Fail**: Pass if handled gracefully

---

### Edge Case 2: Too Many Matches
**Scenario**: Thousands of restaurants match

**Expected**: Sorted and capped at MAX_CANDIDATES

**Test**: Test with low min_rating

**Expected**: Capped at 30, sorted

**Pass/Fail**: Pass if capping works

---

### Edge Case 3: Ambiguous Location
**Scenario**: Location name is misspelled

**Expected**: Fuzzy matching or empty result

**Test**: Test with "Bangalor" instead of "Bangalore"

**Expected**: Either fuzzy match or empty

**Pass/Fail**: Pass if handled gracefully

---

### Edge Case 4: Location Case Mismatch
**Scenario**: User types "delhi" but data has "Delhi"

**Expected**: Case-insensitive match

**Test**:
```python
preferences = UserPreferences(
    location="delhi",  # lowercase
    budget="medium",
    cuisine="Italian",
    min_rating=3.0
)
result = filter_service.filter(preferences, repo)
# Should match "Delhi"
```

**Pass/Fail**: Pass if case-insensitive

---

### Edge Case 5: Rating at Boundary
**Scenario**: min_rating exactly equals restaurant rating

**Expected**: Restaurant included (>= comparison)

**Test**:
```python
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
result = filter_service.filter(preferences, repo)
# Restaurant with rating 4.0 should be included
```

**Pass/Fail**: Pass if boundary handled correctly

---

## Performance Criteria

- [ ] Filter operation completes in < 100ms
- [ ] Sorting completes in < 50ms
- [ ] Validation completes in < 10ms

**Evaluation Method**: Timing tests

**Pass Criteria**: All operations within time limits

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] All filter types work correctly
- [ ] Sorting and capping work
- [ ] Input validation works
- [ ] Empty results handled
- [ ] Performance within targets

### Should Have (Non-blocking)
- [ ] Fuzzy location matching
- [ ] Comprehensive logging
- [ ] Clear error messages
- [ ] Debug mode

### Nice to Have (Optional)
- [ ] Filter suggestions
- [ ] Filter performance profiling
- [ ] Advanced filter combinations

---

## Sign-off

**Phase 3 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
