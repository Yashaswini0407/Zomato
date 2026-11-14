# Phase 9 Evaluation Criteria: Advanced Deployment (Railway + Vercel)

## Overview
This document defines the evaluation criteria for Phase 9: Advanced Deployment (Railway + Vercel).

## Success Criteria

### 1. Backend Refactoring
- [ ] Streamlit converted to FastAPI
- [ ] REST API endpoints implemented:
  - POST /api/v1/recommendations
  - GET /api/v1/health
  - GET /api/v1/metadata/locations
  - GET /api/v1/metadata/cuisines
- [ ] CORS support added
- [ ] API documentation (Swagger) added
- [ ] requirements.txt for backend created

**Evaluation Method**: Test FastAPI endpoints

**Pass Criteria**: All endpoints work correctly

---

### 2. Frontend Development
- [ ] React + Vite frontend created
- [ ] User input form implemented
- [ ] Results display implemented
- [ ] API client for backend communication
- [ ] Loading states and error handling
- [ ] Responsive design

**Evaluation Method**: Test React frontend

**Pass Criteria**: Frontend works correctly

---

### 3. Railway Deployment
- [ ] Railway account created
- [ ] Railway project created
- [ ] GitHub repository connected
- [ ] Build settings configured
- [ ] Environment variables added:
  - LLM_API_KEY
  - LLM_MODEL
  - DATA_PATH
  - etc.
- [ ] Backend deployed
- [ ] Backend endpoints tested

**Evaluation Method**: Check Railway dashboard and test endpoints

**Pass Criteria**: Backend deployed and working

---

### 4. Vercel Deployment
- [ ] Vercel account created
- [ ] Vercel project created from GitHub
- [ ] Build settings configured
- [ ] Environment variable added: VITE_API_URL
- [ ] Frontend deployed
- [ ] Frontend-backend communication tested

**Evaluation Method**: Check Vercel dashboard and test frontend

**Pass Criteria**: Frontend deployed and working

---

### 5. Data Deployment
- [ ] Data file stored in Railway volume or external storage
- [ ] Data loading configured in backend
- [ ] Data access tested in deployed environment

**Evaluation Method**: Test data loading in deployed backend

**Pass Criteria**: Data loads successfully

---

### 6. Integration Testing
- [ ] Full flow from frontend to backend tested
- [ ] Error handling tested
- [ ] Performance tested
- [ ] Logs monitored

**Evaluation Method**: End-to-end testing

**Pass Criteria**: Full flow works

---

## Functional Tests

### Test 1: Backend Endpoints
```bash
# Test health endpoint
curl https://backend-url.railway.app/api/v1/health

# Test locations endpoint
curl https://backend-url.railway.app/api/v1/metadata/locations

# Test cuisines endpoint
curl https://backend-url.railway.app/api/v1/metadata/cuisines

# Test recommendations endpoint
curl -X POST https://backend-url.railway.app/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"location":"Bangalore","budget":"medium","cuisine":"Italian","min_rating":4.0}'
```

**Expected**: All endpoints return valid responses

**Pass/Fail**: Pass if all endpoints work

---

### Test 2: Frontend Loading
```bash
# Visit frontend URL
# Check that app loads
# Check that no console errors
```

**Expected**: Frontend loads without errors

**Pass/Fail**: Pass if frontend loads

---

### Test 3: Frontend-Backend Communication
```bash
# Fill form in frontend
# Submit
# Check that backend is called
# Check that results displayed
```

**Expected**: Frontend communicates with backend

**Pass/Fail**: Pass if communication works

---

### Test 4: CORS Configuration
```bash
# Test CORS by making request from frontend
# Check that request succeeds
# Check that CORS headers present
```

**Expected**: CORS configured correctly

**Pass/Fail**: Pass if CORS works

---

### Test 5: Error Handling
```bash
# Submit invalid data from frontend
# Check error message displayed
# Test backend error scenarios
# Check errors propagated correctly
```

**Expected**: Errors handled end-to-end

**Pass/Fail**: Pass if errors handled

---

## Quality Checks

### Backend Quality
- [ ] API follows REST principles
- [ ] Endpoints documented
- [ ] Error responses consistent
- [ ] CORS configured properly

**Evaluation Method**: API review and testing

**Pass Criteria**: Backend is high quality

---

### Frontend Quality
- [ ] UI is responsive
- [ ] Error handling works
- [ ] Loading states work
- [ ] User experience is good

**Evaluation Method**: UI review and testing

**Pass Criteria**: Frontend is high quality

---

## Edge Case Handling

### Edge Case 1: CORS Errors
**Scenario**: Frontend cannot access backend

**Expected**: CORS configured properly

**Test**: Test from frontend

**Expected**: Request succeeds

**Pass/Fail**: Pass if CORS works

---

### Edge Case 2: API URL Mismatch
**Scenario**: Frontend has wrong backend URL

**Expected**: Use environment variable

**Test**: Check VITE_API_URL

**Expected**: URL correct

**Pass/Fail**: Pass if URL correct

---

### Edge Case 3: Backend Down
**Scenario**: Backend is unavailable

**Expected**: Show error, offer retry

**Test**: Stop backend, test frontend

**Expected**: Error shown

**Pass/Fail**: Pass if error handled

---

### Edge Case 4: Rate Limiting
**Scenario**: Too many requests to backend

**Expected**: Implement rate limiting

**Test**: Send many requests

**Expected**: Rate limiting works

**Pass/Fail**: Pass if rate limiting works

---

### Edge Case 5: Data File Access
**Scenario**: Cannot access data file on Railway

**Expected**: Use Railway volumes or S3

**Test**: Test data loading

**Expected**: Data loads

**Pass/Fail**: Pass if data loads

---

### Edge Case 6: Cold Start
**Scenario**: Backend takes long to start

**Expected**: Implement health checks, loading message

**Test**: Test cold start

**Expected**: Acceptable startup

**Pass/Fail**: Pass if startup acceptable

---

## Performance Criteria

- [ ] Backend starts in < 10 seconds
- [ ] API response time < 2 seconds (excluding LLM)
- [ ] Frontend loads in < 3 seconds
- [ ] End-to-end request < 20 seconds

**Evaluation Method**: Performance monitoring

**Pass Criteria**: Performance is acceptable

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Backend deploys to Railway
- [ ] Frontend deploys to Vercel
- [ ] Frontend communicates with backend
- [ ] Full user flow works
- [ ] Performance acceptable

### Should Have (Non-blocking)
- [ ] API documentation
- [ ] Error monitoring
- [ ] Performance monitoring
- [ ] Logging configured

### Nice to Have (Optional)
- [ ] Custom domains
- [ ] SSL certificates
- [ ] CDN for frontend
- [ ] Load balancing

---

## Sign-off

**Phase 9 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
