# Phase 5 Evaluation Criteria: Recommendation Orchestrator

## Overview
This document defines the evaluation criteria for Phase 5: Recommendation Orchestrator.

## Success Criteria

### 1. Orchestrator
- [ ] RecommendationOrchestrator coordinates all services
- [ ] execute() method works end-to-end
- [ ] Validation step works
- [ ] Filtering step works
- [ ] Prompt building step works
- [ ] LLM call step works
- [ ] Parsing step works
- [ ] Merging step works

**Evaluation Method**:
```python
from app.services.orchestrator import RecommendationOrchestrator
from app.models.preferences import UserPreferences

orchestrator = RecommendationOrchestrator()
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
response = orchestrator.execute(preferences)
assert response is not None
assert len(response.recommendations) > 0
```

**Pass Criteria**: Orchestrator completes full flow

---

### 2. Recommendation Response Model
- [ ] RecommendationResponse model defined
- [ ] Contains summary field
- [ ] Contains recommendations list
- [ ] Contains meta field

**Evaluation Method**:
```python
from app.models.response import RecommendationResponse
response = RecommendationResponse(
    summary="Test summary",
    recommendations=[],
    meta={"test": "value"}
)
assert response.summary == "Test summary"
```

**Pass Criteria**: Model structure correct

---

### 3. Error Handling
- [ ] Validation errors return 400
- [ ] No candidates returns empty response
- [ ] LLM failure triggers fallback
- [ ] Parse failure triggers fallback
- [ ] Errors logged with details

**Evaluation Method**: Test various error scenarios

**Pass Criteria**: All errors handled gracefully

---

### 4. Fallback Strategy
- [ ] Rating-based fallback implemented
- [ ] Fallback returns top-k by rating
- [ ] Fallback provides generic explanations
- [ ] Fallback logged

**Evaluation Method**:
```python
# Test fallback by mocking LLM failure
response = orchestrator.execute(preferences, force_fallback=True)
assert len(response.recommendations) > 0
```

**Pass Criteria**: Fallback works correctly

---

### 5. Caching Integration
- [ ] Cache checked before LLM call
- [ ] Cache stores successful responses
- [ ] Cache key based on preferences + candidate_ids
- [ ] Cache TTL configured (1 hour)
- [ ] Cache hit/miss logged

**Evaluation Method**:
```python
# First call - cache miss
response1 = orchestrator.execute(preferences)
# Second call - cache hit
response2 = orchestrator.execute(preferences)
# Should be faster
```

**Pass Criteria**: Caching improves performance

---

## Functional Tests

### Test 1: End-to-End Flow
```python
from app.services.orchestrator import RecommendationOrchestrator

orchestrator = RecommendationOrchestrator()
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0,
    top_k=5
)
response = orchestrator.execute(preferences)
print(f"Summary: {response.summary}")
print(f"Recommendations: {len(response.recommendations)}")
assert len(response.recommendations) == 5
assert all(r.explanation for r in response.recommendations)
```

**Expected**: Complete recommendation response

**Pass/Fail**: Pass if full flow works

---

### Test 2: Validation Error
```python
invalid_prefs = UserPreferences(
    location="",  # Empty
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
try:
    orchestrator.execute(invalid_prefs)
    assert False, "Should have raised error"
except ValidationError as e:
    print(f"Validation error: {e}")
```

**Expected**: Validation error raised

**Pass/Fail**: Pass if validation works

---

### Test 3: No Candidates
```python
no_match_prefs = UserPreferences(
    location="NonexistentCity",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
response = orchestrator.execute(no_match_prefs)
assert len(response.recommendations) == 0
```

**Expected**: Empty response, no LLM call

**Pass/Fail**: Pass if handled correctly

---

### Test 4: LLM Failure Fallback
```python
# Mock LLM failure
response = orchestrator.execute(preferences, mock_llm_failure=True)
assert len(response.recommendations) > 0
# Should use rating-based fallback
```

**Expected**: Fallback activated, results returned

**Pass/Fail**: Pass if fallback works

---

### Test 5: Parse Failure Fallback
```python
# Mock parse failure
response = orchestrator.execute(preferences, mock_parse_failure=True)
assert len(response.recommendations) > 0
```

**Expected**: Fallback activated

**Pass/Fail**: Pass if fallback works

---

### Test 6: Cache Hit
```python
# First call
response1 = orchestrator.execute(preferences)
# Second call should hit cache
response2 = orchestrator.execute(preferences)
assert response1.summary == response2.summary
```

**Expected**: Same response from cache

**Pass/Fail**: Pass if caching works

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

### Edge Case 1: Validation Fails
**Scenario**: Input validation returns errors

**Expected**: ValidationError with details

**Test**: Test with invalid input

**Expected**: Clear error message

**Pass/Fail**: Pass if error is clear

---

### Edge Case 2: No Candidates
**Scenario**: Filter returns empty candidate list

**Expected**: Empty response, skip LLM

**Test**: Test with impossible criteria

**Expected**: Empty response

**Pass/Fail**: Pass if handled correctly

---

### Edge Case 3: LLM Failure
**Scenario**: LLM call fails after retries

**Expected**: Rating-based fallback

**Test**: Mock LLM failure

**Expected**: Fallback activated

**Pass/Fail**: Pass if fallback works

---

### Edge Case 4: Parse Failure
**Scenario**: Response parser fails

**Expected**: Rating-based fallback

**Test**: Mock parse failure

**Expected**: Fallback activated

**Pass/Fail**: Pass if fallback works

---

### Edge Case 5: Merge Failure
**Scenario**: Merger fails to join data

**Expected**: Partial results with warning

**Test**: Mock merge failure

**Expected**: Partial results returned

**Pass/Fail**: Pass if partial results returned

---

### Edge Case 6: Timeout
**Scenario**: Operation takes too long

**Expected**: Partial results or timeout error

**Test**: Set very short timeout

**Expected**: Timeout handled gracefully

**Pass/Fail**: Pass if timeout handled

---

## Performance Criteria

- [ ] End-to-end flow completes in < 20 seconds
- [ ] Validation < 10ms
- [ ] Filtering < 100ms
- [ ] LLM call 2-15s
- [ ] Parsing < 50ms
- [ ] Merging < 50ms
- [ ] Cache hit < 100ms

**Evaluation Method**: Timing tests

**Pass Criteria**: All operations within time limits

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Orchestrator coordinates all services
- [ ] End-to-end flow works
- [ ] Error handling works
- [ ] Fallback mechanism works
- [ ] Caching improves performance
- [ ] Performance within targets

### Should Have (Non-blocking)
- [ ] Comprehensive logging
- [ ] Detailed error messages
- [ ] Cache statistics
- [ ] Fallback metrics

### Nice to Have (Optional)
- [ ] Request tracing
- [ ] Performance profiling
- [ ] Advanced caching strategies

---

## Sign-off

**Phase 5 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
