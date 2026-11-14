# Phase 6 Evaluation Criteria: Streamlit UI Development

## Overview
This document defines the evaluation criteria for Phase 6: Streamlit UI Development.

## Success Criteria

### 1. Streamlit Setup
- [ ] Streamlit app runs without errors
- [ ] Page settings configured
- [ ] Title and description displayed
- [ ] Layout is clean and organized

**Evaluation Method**:
```bash
streamlit run src/app/main.py
```

**Pass Criteria**: App starts and displays correctly

---

### 2. Input Form
- [ ] Location input field present
- [ ] Budget dropdown (low, medium, high)
- [ ] Cuisine input field
- [ ] Rating slider (0-5, step 0.1)
- [ ] Additional preferences text area (optional)
- [ ] Number of recommendations slider (1-10)
- [ ] Submit button
- [ ] Form validation works

**Evaluation Method**: Manual inspection of UI

**Pass Criteria**: All fields present and functional

---

### 3. Metadata Endpoints
- [ ] Available locations loaded
- [ ] Available cuisines loaded
- [ ] Autocomplete works for location
- [ ] Autocomplete works for cuisine
- [ ] Metadata cached for performance

**Evaluation Method**: Test autocomplete functionality

**Pass Criteria**: Autocomplete works correctly

---

### 4. Results Display
- [ ] Recommendation cards displayed
- [ ] Restaurant name shown
- [ ] Location shown
- [ ] Cuisines shown
- [ ] Rating shown (with stars)
- [ ] Estimated cost shown
- [ ] Budget band shown
- [ ] AI explanation shown
- [ ] Rank shown
- [ ] Summary displayed (if present)

**Evaluation Method**: Submit form and inspect results

**Pass Criteria**: All information displayed correctly

---

### 5. Loading States
- [ ] Spinner shown during processing
- [ ] Progress indicators displayed
- [ ] Submit button disabled during processing
- [ ] Loading message clear

**Evaluation Method**: Submit form and observe loading state

**Pass Criteria**: Loading states work correctly

---

### 6. Error Handling
- [ ] Validation errors displayed
- [ ] LLM failure errors displayed
- [ ] No results message shown
- [ ] Retry button available
- [ ] Error messages user-friendly

**Evaluation Method**: Test various error scenarios

**Pass Criteria**: Errors handled gracefully

---

### 7. Styling
- [ ] Custom CSS applied
- [ ] Icons used (emoji or FontAwesome)
- [ ] Color scheme consistent
- [ ] Responsive design works

**Evaluation Method**: Visual inspection and testing on different screen sizes

**Pass Criteria**: UI is visually appealing and responsive

---

## Functional Tests

### Test 1: Form Submission
```bash
# Start app
streamlit run src/app/main.py

# Fill form:
# Location: Bangalore
# Budget: Medium
# Cuisine: Italian
# Rating: 4.0
# Additional preferences: (optional)
# Top-k: 5

# Click submit
```

**Expected**: Results displayed after processing

**Pass/Fail**: Pass if submission works

---

### Test 2: Form Validation
```bash
# Try submitting with empty location
# Try submitting with empty cuisine
# Try submitting with invalid rating
```

**Expected**: Validation errors shown

**Pass/Fail**: Pass if validation works

---

### Test 3: Autocomplete
```bash
# Type "Bang" in location field
# Should show "Bangalore" as suggestion
# Type "Ital" in cuisine field
# Should show "Italian" as suggestion
```

**Expected**: Autocomplete suggestions appear

**Pass/Fail**: Pass if autocomplete works

---

### Test 4: Results Display
```bash
# Submit valid form
# Check that all fields are displayed:
# - Restaurant name
# - Location
# - Cuisines
# - Rating with stars
# - Cost
# - Explanation
# - Rank
```

**Expected**: All fields displayed correctly

**Pass/Fail**: Pass if display is correct

---

### Test 5: Loading State
```bash
# Submit form
# Observe loading spinner
# Check submit button is disabled
```

**Expected**: Loading state shown

**Pass/Fail**: Pass if loading works

---

### Test 6: Error Handling
```bash
# Submit with invalid data
# Check error message displayed
# Submit with location that has no results
# Check "No results" message
```

**Expected**: Appropriate error messages shown

**Pass/Fail**: Pass if errors handled

---

### Test 7: Responsive Design
```bash
# Test on desktop (1920x1080)
# Test on tablet (768x1024)
# Test on mobile (375x667)
```

**Expected**: Layout adapts to screen size

**Pass/Fail**: Pass if responsive

---

## Quality Checks

### UI/UX Quality
- [ ] Form is intuitive
- [ ] Labels are clear
- [ ] Instructions are helpful
- [ ] Colors are accessible
- [ ] Typography is readable

**Evaluation Method**: Manual review and accessibility check

**Pass Criteria**: UI is user-friendly and accessible

---

### Code Quality
- [ ] Code follows PEP 8
- [ ] Streamlit best practices followed
- [ ] Components organized
- [ ] No hardcoded values

**Evaluation Method**: Code review

**Pass Criteria**: Code is clean and maintainable

---

## Edge Case Handling

### Edge Case 1: Empty Form Submission
**Scenario**: User submits without filling required fields

**Expected**: Validation error, prevent submission

**Test**: Submit empty form

**Expected**: Error shown, submission prevented

**Pass/Fail**: Pass if validation works

---

### Edge Case 2: Long Additional Preferences
**Scenario**: User enters 1000+ characters

**Expected**: Character count shown, truncated to 500

**Test**: Enter long text

**Expected**: Truncation with warning

**Pass/Fail**: Pass if handled

---

### Edge Case 3: No Results
**Scenario**: Query returns no restaurants

**Expected**: Friendly message, suggest relaxing criteria

**Test**: Submit impossible criteria

**Expected**: Appropriate message

**Pass/Fail**: Pass if message shown

---

### Edge Case 4: Slow Response
**Scenario**: LLM takes > 15 seconds

**Expected**: Loading spinner, progress indicator

**Test**: Mock slow response

**Expected**: Loading state maintained

**Pass/Fail**: Pass if loading shown

---

### Edge Case 5: Network Error
**Scenario**: Network disconnect during request

**Expected**: Error message, retry button

**Test**: Disconnect network during request

**Expected**: Error shown, retry available

**Pass/Fail**: Pass if handled

---

### Edge Case 6: Mobile View
**Scenario**: User on mobile device

**Expected**: Responsive layout, stacked components

**Test**: Test on mobile

**Expected**: Layout adapts

**Pass/Fail**: Pass if responsive

---

## Performance Criteria

- [ ] App starts in < 5 seconds
- [ ] Form renders in < 1 second
- [ ] Results render in < 1 second
- [ ] Loading states appear immediately

**Evaluation Method**: Timing tests

**Pass Criteria**: UI performance is acceptable

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Streamlit app runs without errors
- [ ] All form fields present
- [ ] Results display correctly
- [ ] Loading states work
- [ ] Error handling works
- [ ] Responsive design

### Should Have (Non-blocking)
- [ ] Autocomplete works
- [ ] Custom styling
- [ ] Icons used
- [ ] Accessible colors

### Nice to Have (Optional)
- [ ] Dark mode
- [ ] Save favorites
- [ ] Share functionality
- [ ] Advanced filters

---

## Sign-off

**Phase 6 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
