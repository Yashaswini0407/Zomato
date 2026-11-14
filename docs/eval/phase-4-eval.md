# Phase 4 Evaluation Criteria: LLM Integration & Prompt Engineering

## Overview
This document defines the evaluation criteria for Phase 4: LLM Integration & Prompt Engineering.

## Success Criteria

### 1. LLM Client
- [ ] GroqClient successfully calls Groq API
- [ ] Retry logic implemented (3 attempts)
- [ ] Timeout handling works
- [ ] Rate limit handling works
- [ ] Error messages are clear

**Evaluation Method**:
```python
from app.services.llm_client import GroqClient
client = GroqClient()
response = client.complete("Test prompt")
assert response is not None
assert len(response) > 0
```

**Pass Criteria**: LLM client makes successful API calls

---

### 2. Prompt Builder
- [ ] PromptBuilder generates valid prompts
- [ ] System message includes role and constraints
- [ ] User context serialized correctly
- [ ] Candidate block formatted as JSON
- [ ] Task instructions clear
- [ ] Output format specified

**Evaluation Method**:
```python
from app.services.prompt_builder import PromptBuilder
from app.models.preferences import UserPreferences

builder = PromptBuilder()
preferences = UserPreferences(
    location="Bangalore",
    budget="medium",
    cuisine="Italian",
    min_rating=4.0
)
prompt = builder.build(preferences, candidates)
assert "restaurant advisor" in prompt.lower()
assert "only recommend from provided list" in prompt.lower()
```

**Pass Criteria**: Prompt contains all required elements

---

### 3. Prompt Templates
- [ ] Versioned templates implemented
- [ ] Template variables work correctly
- [ ] Template validation works

**Evaluation Method**:
```python
from app.services.prompt_templates import PromptTemplates
templates = PromptTemplates()
prompt = templates.render("v1", {
    "user_preferences": "...",
    "candidates_json": "...",
    "top_k": 5
})
assert prompt is not None
```

**Pass Criteria**: Templates render correctly

---

### 4. Response Parser
- [ ] ResponseParser extracts JSON correctly
- [ ] Validates response schema
- [ ] Validates restaurant_ids
- [ ] Handles malformed JSON with regex fallback
- [ ] Returns structured recommendations

**Evaluation Method**:
```python
from app.services.response_parser import ResponseParser

parser = ResponseParser()
valid_json = '{"summary": "...", "recommendations": [...]}'
parsed = parser.parse(valid_json)
assert parsed is not None
assert 'recommendations' in parsed
```

**Pass Criteria**: Parser handles valid and invalid JSON

---

### 5. Recommendation Merger
- [ ] Merger joins LLM output with Restaurant entities
- [ ] Validates restaurant_ids
- [ ] Handles missing restaurant_ids
- [ ] Returns complete recommendations

**Evaluation Method**:
```python
from app.services.merger import RecommendationMerger

merger = RecommendationMerger()
llm_output = {"recommendations": [{"restaurant_id": "123", "rank": 1}]}
candidates = [Restaurant(id="123", ...)]
merged = merger.merge(llm_output, candidates)
assert len(merged) > 0
```

**Pass Criteria**: Merger joins data correctly

---

### 6. Prompt Engineering
- [ ] System prompt effective (no hallucinations)
- [ ] Candidate block format clear
- [ ] Output format specification works
- [ ] LLM follows instructions

**Evaluation Method**: Test with real LLM calls

**Pass Criteria**: LLM follows instructions, no hallucinations

---

## Functional Tests

### Test 1: LLM API Call
```python
from app.services.llm_client import GroqClient
client = GroqClient()
response = client.complete("What is 2+2?")
assert response is not None
print(f"Response: {response}")
```

**Expected**: Valid response from Groq

**Pass/Fail**: Pass if API call succeeds

---

### Test 2: Prompt Building
```python
from app.services.prompt_builder import PromptBuilder
builder = PromptBuilder()
prompt = builder.build(preferences, candidates)
print(f"Prompt length: {len(prompt)}")
assert len(prompt) > 0
assert "system" in prompt.lower() or "role" in prompt.lower()
```

**Expected**: Valid prompt generated

**Pass/Fail**: Pass if prompt is valid

---

### Test 3: JSON Parsing
```python
from app.services.response_parser import ResponseParser
parser = ResponseParser()

valid_json = '''
{
  "summary": "Test summary",
  "recommendations": [
    {"restaurant_id": "123", "rank": 1, "explanation": "Good choice"}
  ]
}
'''
parsed = parser.parse(valid_json)
assert parsed['summary'] == "Test summary"
assert len(parsed['recommendations']) == 1
```

**Expected**: JSON parsed correctly

**Pass/Fail**: Pass if parsing works

---

### Test 4: Malformed JSON Handling
```python
malformed = "Some text before ```json {...} ``` after"
parsed = parser.parse(malformed)
# Should extract JSON using regex
assert parsed is not None
```

**Expected**: JSON extracted from malformed response

**Pass/Fail**: Pass if regex fallback works

---

### Test 5: Restaurant ID Validation
```python
llm_output = {
    "recommendations": [
        {"restaurant_id": "invalid_id", "rank": 1}
    ]
}
merged = merger.merge(llm_output, candidates)
# Should drop invalid restaurant_id
assert all(r.restaurant.id in [c.id for c in candidates] for r in merged)
```

**Expected**: Invalid IDs dropped

**Pass/Fail**: Pass if validation works

---

### Test 6: Retry Logic
```python
# Mock API failure then success
# Test that retry works
```

**Expected**: Retry on failure

**Pass/Fail**: Pass if retry logic works

---

## Quality Checks

### Prompt Quality
- [ ] System message clear and concise
- [ ] Constraints explicitly stated
- [ ] Output format specified
- [ ] Examples provided (if needed)

**Evaluation Method**: Manual review of prompts

**Pass Criteria**: Prompts are well-designed

---

### Response Quality
- [ ] LLM returns valid JSON
- [ ] LLM doesn't hallucinate restaurants
- [ ] Explanations are relevant
- [ ] Rankings are reasonable

**Evaluation Method**: Test with real LLM calls

**Pass Criteria**: Responses are high quality

---

## Edge Case Handling

### Edge Case 1: LLM API Timeout
**Scenario**: Groq API doesn't respond

**Expected**: Retry with backoff, then fallback

**Test**: Mock timeout scenario

**Expected**: Retry attempted, fallback activated

**Pass/Fail**: Pass if retry and fallback work

---

### Edge Case 2: Invalid API Key
**Scenario**: API key is invalid

**Expected**: Clear error with setup instructions

**Test**: Test with invalid key

**Expected**: Clear error message

**Pass/Fail**: Pass if error is clear

---

### Edge Case 3: Rate Limit (429)
**Scenario**: Too many requests

**Expected**: Exponential backoff, max 3 retries

**Test**: Mock rate limit response

**Expected**: Backoff implemented

**Pass/Fail**: Pass if backoff works

---

### Edge Case 4: Malformed JSON
**Scenario**: LLM returns non-JSON

**Expected**: Regex extraction, then fallback

**Test**: Test with non-JSON response

**Expected**: Fallback activated

**Pass/Fail**: Pass if fallback works

---

### Edge Case 5: Hallucinated Restaurants
**Scenario**: LLM invents restaurants

**Expected**: Invalid IDs dropped, logged

**Test**: Test with hallucinated IDs

**Expected**: Invalid IDs dropped

**Pass/Fail**: Pass if validation works

---

## Performance Criteria

- [ ] LLM call completes in 2-15 seconds
- [ ] Prompt building < 50ms
- [ ] Response parsing < 50ms
- [ ] Merging < 50ms

**Evaluation Method**: Timing tests

**Pass Criteria**: All operations within time limits

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] LLM client works with Groq
- [ ] Prompt builder generates valid prompts
- [ ] Response parser handles various formats
- [ ] Merger joins data correctly
- [ ] Retry logic implemented
- [ ] Fallback mechanism works

### Should Have (Non-blocking)
- [ ] Prompt templates versioned
- [ ] Comprehensive error handling
- [ ] Logging for debugging
- [ ] Response quality monitoring

### Nice to Have (Optional)
- [ ] A/B testing for prompts
- [ ] Prompt optimization
- [ ] Multiple LLM provider support

---

## Sign-off

**Phase 4 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
