# Implementation Plan: AI-Powered Restaurant Recommendation System

**LLM Provider**: Groq (qwen/qwen3.8-27b)
**Current Status**: Phases 0-4 Complete (4/11 phases, 36%)
**Data Source**: Synthetic data (95 restaurants) - Hugging Face dataset was broken

This document provides a phase-wise implementation plan for the Zomato-inspired restaurant recommendation system, derived from [ProblemStatement.md](./ProblemStatement.md) and [architecture.md](./architecture.md).

## Table of Contents
- [Phase Overview](#phase-overview)
- [Phase 0: Project Setup & Configuration](#phase-0-project-setup--configuration)
- [Phase 1: Data Ingestion Pipeline](#phase-1-data-ingestion-pipeline)
- [Phase 2: Data Layer & Repository](#phase-2-data-layer--repository)
- [Phase 3: Filter Service & Business Logic](#phase-3-filter-service--business-logic)
- [Phase 4: LLM Integration & Prompt Engineering](#phase-4-llm-integration--prompt-engineering)
- [Phase 5: Recommendation Orchestrator](#phase-5-recommendation-orchestrator)
- [Phase 6: Streamlit UI Development](#phase-6-streamlit-ui-development)
- [Phase 7: Testing & Quality Assurance](#phase-7-testing--quality-assurance)
- [Phase 8: Streamlit Deployment](#phase-8-streamlit-deployment)
- [Phase 9: Advanced Deployment (Railway + Vercel)](#phase-9-advanced-deployment-railway--vercel)
- [Phase 10: Frontend Enhancement](#phase-10-frontend-enhancement)

---

## Phase Overview

| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| Phase 0 | Project setup, environment configuration | 0.5 day | None |
| Phase 1 | Data ingestion from Hugging Face | 1 day | Phase 0 |
| Phase 2 | Data layer, repository implementation | 1 day | Phase 1 |
| Phase 3 | Filter service and business logic | 1 day | Phase 2 |
| Phase 4 | LLM integration with Groq | 1.5 days | Phase 3 |
| Phase 5 | Orchestrator and end-to-end flow | 1 day | Phase 4 |
| Phase 6 | Streamlit UI development | 1.5 days | Phase 5 |
| Phase 7 | Testing and quality assurance | 1 day | Phase 6 |
| Phase 8 | Streamlit deployment | 0.5 day | Phase 7 |
| Phase 9 | Railway + Vercel deployment | 1 day | Phase 7 |
| Phase 10 | Frontend enhancement | 2 days | Phase 9 |

**Total Estimated Time**: ~11.5 days for complete implementation

---

## Phase 0: Project Setup & Configuration

### Objectives
- Initialize project structure
- Set up development environment
- Configure dependencies and tools
- Set up version control

### Tasks

#### 0.1 Repository Initialization
- [ ] Create project directory structure
- [ ] Initialize Git repository
- [ ] Create `.gitignore` file
- [ ] Set up README.md with project overview

#### 0.2 Environment Setup
- [ ] Create Python virtual environment (Python 3.11+)
- [ ] Create `requirements.txt` with dependencies:
  ```
  streamlit
  pandas
  datasets
  pyarrow
  pydantic
  pydantic-settings
  python-dotenv
  groq
  httpx
  pytest
  pytest-asyncio
  ```
- [ ] Install dependencies
- [ ] Create `.env.example` file

#### 0.3 Configuration Management
- [ ] Create `src/app/config.py` with configuration classes
- [ ] Define environment variables:
  - `LLM_PROVIDER=groq`
  - `LLM_API_KEY=<your-groq-api-key>`
  - `LLM_MODEL=qwen/qwen3.8-27b` (Groq model - mixtral decommissioned)
  - `DATA_PATH=data/processed/restaurants.parquet`
  - `MAX_CANDIDATES=30`
  - `BUDGET_LOW_MAX=500`
  - `BUDGET_MEDIUM_MAX=1500`
- [ ] Implement configuration loading with pydantic-settings

#### 0.4 Project Structure
- [ ] Create directory structure as per architecture:
  ```
  zomato-milestone/
  ├── docs/
  ├── data/
  │   ├── raw/
  │   └── processed/
  ├── src/
  │   └── app/
  │       ├── __init__.py
  │       ├── config.py
  │       ├── models/
  │       ├── ingestion/
  │       ├── data/
  │       ├── services/
  │       └── api/
  ├── tests/
  ├── scripts/
  ├── .env.example
  ├── requirements.txt
  └── README.md
  ```

### Edge Cases & Considerations
- **Python version compatibility**: Ensure Python 3.11+ for modern type hints
- **Dependency conflicts**: Use pip-tools or poetry for dependency management
- **Environment variable security**: Never commit `.env` file; use `.env.example`
- **Cross-platform compatibility**: Handle Windows/Unix path differences

### Deliverables
- Initialized Git repository
- Working Python environment with all dependencies
- Configuration system with environment variables
- Complete directory structure

### Success Criteria
- `python -c "import streamlit; import pandas; import groq"` runs without errors
- Configuration loads correctly from environment variables
- All directories are created and accessible

---

## Phase 1: Data Ingestion Pipeline

### Objectives
- Fetch Zomato dataset from Hugging Face
- Normalize and clean the data
- Map raw columns to canonical schema
- Persist processed data for fast querying

### Tasks

#### 1.1 Dataset Loading
- [ ] Create `src/app/ingestion/loader.py`
- [ ] Implement `DatasetLoader` class with `load_dataset()` method
- [ ] Use `datasets` library to fetch from Hugging Face
- [ ] Handle authentication if required
- [ ] Add error handling for network failures

#### 1.2 Schema Normalization
- [ ] Create `src/app/ingestion/normalizer.py`
- [ ] Implement `SchemaNormalizer` class
- [ ] Inspect actual column names from dataset
- [ ] Create mapping from raw columns to canonical fields:
  - Restaurant name → `name`
  - City/locality → `location`
  - Cuisines → `cuisines` (list)
  - Cost/price → `estimated_cost`
  - Rating → `rating`
- [ ] Handle missing or inconsistent columns

#### 1.3 Data Preprocessing
- [ ] Create `src/app/ingestion/preprocessor.py`
- [ ] Implement `Preprocessor` class with methods:
  - `clean_nulls()`: Remove or fill null values
  - `normalize_location()`: Standardize location strings
  - `parse_cuisines()`: Split comma-separated cuisines
  - `map_budget_band()`: Assign low/medium/high based on cost
- [ ] Add data validation rules

#### 1.4 Persistence
- [ ] Create `src/app/ingestion/writer.py`
- [ ] Implement `PersistenceWriter` class
- [ ] Support multiple formats: Parquet (primary), SQLite (fallback)
- [ ] Write processed data to `data/processed/`
- [ ] Add data integrity checks

#### 1.5 Ingestion Pipeline
- [ ] Create `src/app/ingestion/pipeline.py`
- [ ] Implement `IngestionPipeline` orchestrating all steps
- [ ] Add logging for each stage
- [ ] Create CLI script `scripts/ingest.py`
- [ ] Add progress indicators

#### 1.6 Domain Models
- [ ] Create `src/app/models/restaurant.py`
- [ ] Define `Restaurant` dataclass/pydantic model
- [ ] Define `BudgetBand` enum (low, medium, high)
- [ ] Add validation methods

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Dataset not found** | Raise clear error with dataset URL and instructions |
| **Missing columns** | Log warning, use default values or skip affected rows |
| **Null values in critical fields** | Skip rows with null name/location/rating |
| **Invalid rating values** | Clamp to [0, 5] range, log warnings |
| **Malformed cuisine strings** | Split on common delimiters (, ; /), clean whitespace |
| **Cost as string** | Parse numeric value, handle currency symbols |
| **Duplicate restaurants** | Deduplicate based on name + location |
| **Empty dataset** | Raise error, prevent creating empty processed file |
| **Network timeout** | Implement retry with exponential backoff (3 attempts) |
| **Large dataset** | Process in chunks, show progress bar |
| **Encoding issues** | Use UTF-8 encoding, handle special characters |

### Testing Strategy
- [ ] Unit test for `DatasetLoader` with mock Hugging Face response
- [ ] Unit test for `SchemaNormalizer` with sample raw data
- [ ] Unit test for `Preprocessor` with edge case data
- [ ] Integration test for full pipeline with real dataset
- [ ] Test with null values, missing columns, invalid data

### Deliverables
- Complete data ingestion pipeline
- Processed restaurant dataset in Parquet format
- Domain models for Restaurant
- CLI script for data ingestion
- Comprehensive test coverage

### Success Criteria
- `python scripts/ingest.py` runs successfully
- Processed data file created in `data/processed/`
- Data contains all required fields with valid values
- No data loss during processing
- Processing time < 5 minutes for full dataset

---

## Phase 2: Data Layer & Repository

### Objectives
- Implement RestaurantRepository for data access
- Support filtering operations
- Add in-memory caching for performance
- Implement data validation

### Tasks

#### 2.1 Repository Interface
- [ ] Create `src/app/data/repository.py`
- [ ] Define `RestaurantRepository` interface
- [ ] Implement methods:
  - `get_all() -> list[Restaurant]`
  - `filter(criteria: FilterCriteria) -> list[Restaurant]`
  - `get_by_ids(ids: list[str]) -> list[Restaurant]`
  - `get_locations() -> list[str]`
  - `get_cuisines() -> list[str]`

#### 2.2 Filter Criteria Model
- [ ] Create `src/app/models/filters.py`
- [ ] Define `FilterCriteria` pydantic model:
  ```python
  class FilterCriteria(BaseModel):
      location: str | None = None
      budget: BudgetBand | None = None
      cuisine: str | None = None
      min_rating: float | None = None
  ```

#### 2.3 Repository Implementation
- [ ] Implement `ParquetRepository` for Parquet backend
- [ ] Implement `InMemoryRepository` for in-memory backend
- [ ] Add lazy loading for large datasets
- [ ] Implement indexing for frequently queried fields

#### 2.4 Caching Layer
- [ ] Add optional caching using `functools.lru_cache`
- [ ] Implement cache invalidation strategy
- [ ] Add cache statistics logging

#### 2.5 Data Validation
- [ ] Add validation in repository methods
- [ ] Validate query parameters
- [ ] Handle empty results gracefully

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Processed data file not found** | Raise FileNotFoundError with clear message |
| **Corrupted data file** | Attempt recovery, else re-run ingestion |
| **Empty result set** | Return empty list, log info message |
| **Invalid filter criteria** | Validate and raise ValueError with details |
| **Location not found** | Return empty list, suggest available locations |
| **Cuisine not found** | Return empty list, suggest available cuisines |
| **Rating out of range** | Clamp to [0, 5], log warning |
| **Memory constraints** | Load data in chunks, use generators |
| **Concurrent access** | Use thread-safe operations or locks |
| **Cache staleness** | Implement TTL or manual cache clear |

### Testing Strategy
- [ ] Unit test for repository with mock data
- [ ] Test filter combinations (location + budget + cuisine + rating)
- [ ] Test edge cases (no results, all results, single result)
- [ ] Test caching behavior
- [ ] Performance test for large datasets

### Deliverables
- RestaurantRepository implementation
- FilterCriteria model
- Caching layer
- Comprehensive test suite
- Performance benchmarks

### Success Criteria
- Repository loads processed data successfully
- Filter operations return correct results
- Cache improves performance on repeated queries
- All filter combinations work correctly
- Query time < 100ms for in-memory operations

---

## Phase 3: Filter Service & Business Logic

### Objectives
- Implement FilterService for applying business rules
- Add post-filter ranking logic
- Implement candidate capping
- Add logging and debugging support

### Tasks

#### 3.1 Filter Service
- [ ] Create `src/app/services/filter_service.py`
- [ ] Implement `FilterService` class
- [ ] Implement `filter()` method with signature:
  ```python
  def filter(preferences: UserPreferences, repository: RestaurantRepository) -> FilterResult
  ```
- [ ] Apply filters in order: location → budget → cuisine → rating
- [ ] Add post-filter sorting by rating (descending)
- [ ] Implement candidate capping at MAX_CANDIDATES

#### 3.2 Filter Result Model
- [ ] Create `src/app/models/filter_result.py`
- [ ] Define `FilterResult` model:
  ```python
  class FilterResult(BaseModel):
      candidates: list[Restaurant]
      total_before_cap: int
      applied_filters: dict[str, Any]
  ```

#### 3.3 User Preferences Model
- [ ] Create `src/app/models/preferences.py`
- [ ] Define `UserPreferences` model:
  ```python
  class UserPreferences(BaseModel):
      location: str
      budget: BudgetBand
      cuisine: str
      min_rating: float
      additional_preferences: str | None = None
      top_k: int = 5
  ```
- [ ] Add validation:
  - location not empty
  - budget is valid enum
  - cuisine not empty
  - min_rating in [0, 5]
  - top_k in [1, 20]

#### 3.4 Input Validation
- [ ] Create `src/app/services/validator.py`
- [ ] Implement `InputValidator` class
- [ ] Add string normalization (trim, title-case)
- [ ] Add validation error messages

#### 3.5 Logging & Debugging
- [ ] Add logging for each filter stage
- [ ] Log filter counts and applied filters
- [ ] Add debug mode for detailed logging

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **No matches after filters** | Return empty FilterResult, skip LLM call |
| **Too many matches** | Sort by rating, cap at MAX_CANDIDATES |
| **Ambiguous location** | Implement fuzzy matching (fuzzywuzzy) |
| **Location case mismatch** | Case-insensitive comparison |
| **Cuisine partial match** | Substring match in cuisines list |
| **Rating at boundary** | Include rating >= min_rating (inclusive) |
| **Invalid budget enum** | Raise ValidationError with valid options |
| **Negative top_k** | Clamp to minimum of 1 |
| **top_k > MAX_CANDIDATES** | Use min(top_k, MAX_CANDIDATES) |
| **additional_preferences too long** | Truncate to 500 chars, log warning |

### Testing Strategy
- [ ] Unit test for each filter type
- [ ] Test filter combinations
- [ ] Test edge cases (no results, single result, many results)
- [ ] Test input validation
- [ ] Test candidate capping logic
- [ ] Test fuzzy location matching

### Deliverables
- FilterService implementation
- UserPreferences model
- FilterResult model
- InputValidator
- Comprehensive test suite
- Logging configuration

### Success Criteria
- FilterService correctly applies all filters
- Results are sorted by rating
- Candidate capping works correctly
- Input validation catches invalid inputs
- Filter operations complete in < 100ms

---

## Phase 4: LLM Integration & Prompt Engineering

### Objectives
- Integrate Groq LLM API
- Implement prompt builder with templates
- Add response parser for structured output
- Implement retry logic and error handling

### Tasks

#### 4.1 LLM Client
- [ ] Create `src/app/services/llm_client.py`
- [ ] Implement `GroqClient` class
- [ ] Use `groq` Python SDK
- [ ] Implement `complete()` method with retry logic
- [ ] Add timeout handling
- [ ] Add rate limit handling

#### 4.2 Prompt Builder
- [ ] Create `src/app/services/prompt_builder.py`
- [ ] Implement `PromptBuilder` class
- [ ] Design system message with role and constraints
- [ ] Design user context serialization
- [ ] Design candidate block formatting (JSON)
- [ ] Design task instructions
- [ ] Design output format specification

#### 4.3 Prompt Templates
- [ ] Create `src/app/services/prompt_templates.py`
- [ ] Define versioned prompt templates
- [ ] Implement template variables:
  - `{user_preferences}`
  - `{candidates_json}`
  - `{top_k}`
- [ ] Add template validation

#### 4.4 Response Parser
- [ ] Create `src/app/services/response_parser.py`
- [ ] Implement `ResponseParser` class
- [ ] Parse JSON from LLM response
- [ ] Validate response schema
- [ ] Validate restaurant_ids against candidates
- [ ] Handle malformed JSON with regex fallback

#### 4.5 Recommendation Merger
- [ ] Create `src/app/services/merger.py`
- [ ] Implement `RecommendationMerger` class
- [ ] Join LLM output with Restaurant entities
- [ ] Add rank validation
- [ ] Handle missing restaurant_ids

#### 4.6 Prompt Engineering
- [ ] Design effective system prompt:
  ```
  You are a restaurant recommendation expert. Your task is to recommend restaurants
  from the provided list based on user preferences. You must ONLY recommend restaurants
  from the provided list. Do not invent or hallucinate restaurants.

  For each recommendation, provide:
  1. A rank (1 = best match)
  2. A clear explanation of why it fits the user's preferences
  ```
- [ ] Design candidate block format (JSON)
- [ ] Design output format specification
- [ ] Test and iterate on prompt effectiveness

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **LLM API timeout** | Retry once with 2x timeout, then fallback |
| **Invalid API key** | Raise clear error with setup instructions |
| **Rate limit (429)** | Implement exponential backoff, max 3 retries |
| **Malformed JSON response** | Use regex to extract JSON, else fallback |
| **Missing restaurant_id** | Drop recommendation, log warning |
| **Invalid rank values** | Re-rank based on order in list |
| **Duplicate ranks** | Preserve order, log warning |
| **Empty recommendations** | Return empty list, log error |
| **Hallucinated restaurants** | Validate IDs against candidates, drop invalid |
| **Response too long** | Truncate explanation field |
| **Temperature too high** | Clamp to 0.2-0.5 for consistency |
| **Token limit exceeded** | Reduce candidate count, retry |

### Testing Strategy
- [ ] Unit test for LLM client with mock responses
- [ ] Test prompt builder with various inputs
- [ ] Test response parser with valid/invalid JSON
- [ ] Test merger with various LLM outputs
- [ ] Integration test with real Groq API (use test key)
- [ ] Test retry logic with simulated failures

### Deliverables
- Groq LLM client implementation
- Prompt builder with templates
- Response parser with fallback
- Recommendation merger
- Comprehensive test suite
- Prompt documentation

### Success Criteria
- LLM client successfully calls Groq API
- Prompt builder generates valid prompts
- Response parser handles various response formats
- Merger correctly joins LLM output with data
- End-to-end LLM call completes in 2-15 seconds
- Fallback mechanisms work correctly

---

## Phase 5: Recommendation Orchestrator

### Objectives
- Implement orchestrator as single entry point
- Coordinate all services
- Implement complete recommendation flow
- Add error handling and fallbacks

### Tasks

#### 5.1 Orchestrator
- [ ] Create `src/app/services/orchestrator.py`
- [ ] Implement `RecommendationOrchestrator` class
- [ ] Implement `execute()` method:
  ```python
  def execute(preferences: UserPreferences) -> RecommendationResponse
  ```
- [ ] Coordinate: validate → filter → prompt → LLM → parse → merge
- [ ] Add error handling at each stage

#### 5.2 Recommendation Response Model
- [ ] Create `src/app/models/response.py`
- [ ] Define `RecommendationResponse` model:
  ```python
  class RecommendationResponse(BaseModel):
      summary: str | None = None
      recommendations: list[Recommendation]
      meta: dict[str, Any] | None = None
  ```
- [ ] Define `Recommendation` model:
  ```python
  class Recommendation(BaseModel):
      restaurant: Restaurant
      rank: int
      explanation: str
  ```

#### 5.3 Error Handling
- [ ] Implement graceful degradation:
  - Validation error → return 400
  - No candidates → return empty response
  - LLM failure → fallback to rating-based ranking
  - Parse failure → fallback to rating-based ranking
- [ ] Add detailed error logging
- [ ] Add user-friendly error messages

#### 5.4 Fallback Strategy
- [ ] Implement rating-based fallback:
  - Sort candidates by rating descending
  - Return top-k with generic explanations
- [ ] Add fallback logging
- [ ] Add fallback metrics

#### 5.5 Caching Integration
- [ ] Add optional caching in orchestrator
- [ ] Cache key: hash of (preferences, candidate_ids)
- [ ] Cache TTL: 1 hour
- [ ] Add cache hit/miss logging

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Validation fails** | Return ValidationError with details |
| **No candidates** | Return empty response, skip LLM |
| **LLM API down** | Use rating-based fallback |
| **LLM returns invalid data** | Use rating-based fallback |
| **Parse fails** | Use rating-based fallback |
| **Merge fails** | Return partial results with warning |
| **Cache corruption** | Clear cache, recompute |
| **Timeout** | Return partial results or fallback |
| **Concurrent requests** | Use thread-safe operations |
| **Memory pressure** | Limit concurrent requests |

### Testing Strategy
- [ ] Integration test for full orchestrator flow
- [ ] Test with mocked LLM responses
- [ ] Test error scenarios (LLM failure, parse failure)
- [ ] Test fallback mechanism
- [ ] Test caching behavior
- [ ] Performance test for end-to-end flow

### Deliverables
- RecommendationOrchestrator implementation
- RecommendationResponse model
- Comprehensive error handling
- Fallback mechanism
- Caching integration
- Integration test suite

### Success Criteria
- Orchestrator successfully coordinates all services
- Error handling works correctly
- Fallback mechanism activates when needed
- End-to-end flow completes in < 20 seconds
- Caching improves performance on repeated requests

---

## Phase 6: Streamlit UI Development

### Objectives
- Create Streamlit web interface
- Implement user input form
- Display recommendation results
- Add loading states and error handling

### Tasks

#### 6.1 Streamlit Setup
- [ ] Create `src/app/main.py` as Streamlit entry point
- [ ] Configure Streamlit page settings
- [ ] Add title and description
- [ ] Set up page layout

#### 6.2 Input Form
- [ ] Create input form with fields:
  - Location (text input with autocomplete)
  - Budget (select: low, medium, high)
  - Cuisine (text input with autocomplete)
  - Minimum rating (slider: 0-5, step 0.1)
  - Additional preferences (text area, optional)
  - Number of recommendations (slider: 1-10)
- [ ] Add form validation
- [ ] Add submit button

#### 6.3 Metadata Endpoints
- [ ] Add function to get available locations
- [ ] Add function to get available cuisines
- [ ] Implement autocomplete for location and cuisine
- [ ] Cache metadata for performance

#### 6.4 Results Display
- [ ] Create recommendation card component
- [ ] Display:
  - Restaurant name
  - Location
  - Cuisines
  - Rating (with stars)
  - Estimated cost
  - Budget band
  - AI explanation
  - Rank
- [ ] Add summary display (if present)
- [ ] Add expand/collapse for details

#### 6.5 Loading States
- [ ] Add spinner during processing
- [ ] Add progress indicators
- [ ] Disable submit button during processing

#### 6.6 Error Handling
- [ ] Add error display for validation errors
- [ ] Add error display for LLM failures
- [ ] Add error display for no results
- [ ] Add retry button

#### 6.7 Styling
- [ ] Apply custom CSS for better UI
- [ ] Add icons (using emoji or FontAwesome)
- [ ] Improve color scheme
- [ ] Add responsive design

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Empty form submission** | Show validation error, prevent submission |
| **Invalid rating value** | Clamp to valid range, show warning |
| **No autocomplete data** | Allow free text input |
| **Long additional preferences** | Show character count, limit to 500 |
| **No results** | Show friendly message, suggest relaxing criteria |
| **LLM timeout** | Show timeout message, offer retry |
| **Network error** | Show error message, offer retry |
| **Malformed response** | Show error, log details |
| **Slow response** | Show loading spinner with progress |
| **Mobile view** | Use responsive layout, stack components |

### Testing Strategy
- [ ] Manual testing of form inputs
- [ ] Test validation errors
- [ ] Test with various user inputs
- [ ] Test loading states
- [ ] Test error scenarios
- [ ] Test on different screen sizes
- [ ] Test with slow network

### Deliverables
- Streamlit web application
- User input form
- Results display
- Loading states
- Error handling
- Custom styling

### Success Criteria
- Streamlit app runs without errors
- Form accepts all required inputs
- Results display correctly
- Loading states show during processing
- Errors are handled gracefully
- UI is responsive and user-friendly

---

## Phase 7: Testing & Quality Assurance

### Objectives
- Comprehensive testing of all components
- End-to-end testing
- Performance testing
- Manual testing checklist

### Tasks

#### 7.1 Unit Tests
- [ ] Test data ingestion components
- [ ] Test repository operations
- [ ] Test filter service
- [ ] Test LLM client (mocked)
- [ ] Test prompt builder
- [ ] Test response parser
- [ ] Test orchestrator
- [ ] Achieve > 80% code coverage

#### 7.2 Integration Tests
- [ ] Test full data ingestion pipeline
- [ ] Test full recommendation flow
- [ ] Test with real LLM API (test key)
- [ ] Test error scenarios end-to-end

#### 7.3 End-to-End Tests
- [ ] Test complete user journey
- [ ] Test with various user preferences
- [ ] Test edge cases
- [ ] Test performance under load

#### 7.4 Performance Testing
- [ ] Measure data ingestion time
- [ ] Measure filter operation time
- [ ] Measure LLM call time
- [ ] Measure end-to-end response time
- [ ] Identify bottlenecks

#### 7.5 Manual Testing Checklist
- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test with edge cases (no results, single result)
- [ ] Test with slow network
- [ ] Test with LLM failures
- [ ] Test UI on different browsers
- [ ] Test UI on mobile devices

#### 7.6 Bug Fixes
- [ ] Document all found bugs
- [ ] Prioritize and fix critical bugs
- [ ] Fix high-priority bugs
- [ ] Document known issues

### Edge Cases & Testing

| Test Case | Expected Behavior |
|-----------|-------------------|
| **Empty location** | Validation error |
| **Invalid budget** | Validation error |
| **No matching restaurants** | Empty result with message |
| **Single match** | Return single recommendation |
| **Many matches** | Return top-k, cap at MAX_CANDIDATES |
| **LLM timeout** | Fallback to rating-based |
| **Invalid JSON** | Fallback to rating-based |
| **Network error** | Show error, offer retry |
| **Concurrent requests** | Handle without errors |
| **Large dataset** | Performance acceptable |

### Deliverables
- Comprehensive test suite
- Test coverage report
- Performance benchmarks
- Manual testing report
- Bug fix documentation

### Success Criteria
- > 80% code coverage
- All critical bugs fixed
- Performance within targets
- Manual testing passed
- Ready for deployment

---

## Phase 8: Streamlit Deployment

### Objectives
- Deploy application to Streamlit Cloud
- Configure environment variables
- Test deployed application
- Document deployment process

### Tasks

#### 8.1 Preparation
- [ ] Ensure all code is committed to Git
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create `.streamlit/config.toml` for Streamlit settings
- [ ] Update README with deployment instructions

#### 8.2 Streamlit Cloud Setup
- [ ] Create account on Streamlit Cloud (https://share.streamlit.io/)
- [ ] Connect GitHub account
- [ ] Create new app from repository
- [ ] Select main branch and file path

#### 8.3 Environment Configuration
- [ ] Add environment variables in Streamlit settings:
  - `LLM_PROVIDER=groq`
  - `LLM_API_KEY=<your-groq-api-key>`
  - `LLM_MODEL=qwen/qwen3.8-27b` (Groq model - mixtral decommissioned)
  - `MAX_CANDIDATES=30`
  - `BUDGET_LOW_MAX=500`
  - `BUDGET_MEDIUM_MAX=1500`
- [ ] Ensure data file is included in deployment
- [ ] Test environment variable loading

#### 8.4 Data Deployment
- [ ] Ensure processed data file is in repository
- [ ] Or implement data loading on startup
- [ ] Verify data file is accessible
- [ ] Test data loading in deployed environment

#### 8.5 Testing
- [ ] Test deployed application
- [ ] Test all user flows
- [ ] Test error handling
- [ ] Monitor logs for issues

#### 8.6 Documentation
- [ ] Document deployment process
- [ ] Update README with deployed URL
- [ ] Document environment variables
- [ ] Create troubleshooting guide

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Data file too large for GitHub** | Use external storage (S3) or load on startup |
| **Environment variables not loading** | Verify Streamlit settings, check syntax |
| **LLM API key exposed** | Use secrets management, rotate key |
| **App fails to start** | Check logs, verify dependencies |
| **Memory limit exceeded** | Optimize data loading, use streaming |
| **Cold start slow** | Show loading message, optimize startup |
| **Deployment fails** | Check logs, verify file paths |

### Deliverables
- Deployed Streamlit application
- Environment configuration
- Deployment documentation
- Troubleshooting guide

### Success Criteria
- Application deploys successfully
- All features work in deployed environment
- Environment variables load correctly
- Data loads successfully
- Application is accessible via URL

---

## Phase 9: Advanced Deployment (Railway + Vercel)

### Objectives
- Split backend and frontend
- Deploy backend to Railway
- Deploy frontend to Vercel
- Configure cross-origin communication

### Tasks

#### 9.1 Backend Refactoring
- [ ] Convert Streamlit to FastAPI backend
- [ ] Create REST API endpoints:
  - `POST /api/v1/recommendations`
  - `GET /api/v1/health`
  - `GET /api/v1/metadata/locations`
  - `GET /api/v1/metadata/cuisines`
- [ ] Add CORS support
- [ ] Add API documentation (Swagger)
- [ ] Create `requirements.txt` for backend

#### 9.2 Frontend Development
- [ ] Create React + Vite frontend
- [ ] Implement user input form
- [ ] Implement results display
- [ ] Add API client for backend communication
- [ ] Add loading states and error handling
- [ ] Add responsive design

#### 9.3 Railway Deployment
- [ ] Create Railway account
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Configure build settings
- [ ] Add environment variables:
  - `LLM_API_KEY`
  - `LLM_MODEL=qwen/qwen3.8-27b` (Groq model - mixtral decommissioned)
  - `DATA_PATH`
  - etc.
- [ ] Deploy backend
- [ ] Test backend endpoints

#### 9.4 Vercel Deployment
- [ ] Create Vercel account
- [ ] Create new project from GitHub
- [ ] Configure build settings
- [ ] Add environment variable: `VITE_API_URL`
- [ ] Deploy frontend
- [ ] Test frontend-backend communication

#### 9.5 Data Deployment
- [ ] Store data file in Railway volume or external storage
- [ ] Configure data loading in backend
- [ ] Test data access in deployed environment

#### 9.6 Integration Testing
- [ ] Test full flow from frontend to backend
- [ ] Test error handling
- [ ] Test performance
- [ ] Monitor logs

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **CORS errors** | Configure CORS properly in FastAPI |
| **API URL mismatch** | Use environment variable for API URL |
| **Backend down** | Show error in frontend, offer retry |
| **Rate limiting** | Implement rate limiting in backend |
| **Authentication needed** | Add API key authentication (future) |
| **Data file access** | Use Railway volumes or S3 |
| **Cold start** | Implement health checks, show loading |

### Deliverables
- FastAPI backend
- React frontend
- Railway-deployed backend
- Vercel-deployed frontend
- Integration documentation

### Success Criteria
- Backend deploys to Railway successfully
- Frontend deploys to Vercel successfully
- Frontend communicates with backend
- Full user flow works end-to-end
- Performance is acceptable

---

## Phase 10: Frontend Enhancement

### Objectives
- Improve UI/UX with better design
- Add advanced features
- Optimize performance
- Enhance accessibility

### Tasks

#### 10.1 UI Enhancement
- [ ] Use Google Stitch or similar for design
- [ ] Implement modern design system
- [ ] Add animations and transitions
- [ ] Improve color scheme and typography
- [ ] Add icons and visual elements

#### 10.2 Advanced Features
- [ ] Add restaurant images (if available)
- [ ] Add map integration (optional)
- [ ] Add filters sidebar
- [ ] Add save favorites (local storage)
- [ ] Add share functionality
- [ ] Add dark mode

#### 10.3 Performance Optimization
- [ ] Implement lazy loading
- [ ] Add image optimization
- [ ] Implement request debouncing
- [ ] Add response caching in frontend
- [ ] Optimize bundle size

#### 10.4 Accessibility
- [ ] Add ARIA labels
- [ ] Improve keyboard navigation
- [ ] Add screen reader support
- [ ] Improve color contrast
- [ ] Add focus indicators

#### 10.5 Testing
- [ ] Test new features
- [ ] Test performance improvements
- [ ] Test accessibility
- [ ] User testing

### Edge Cases & Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| **Images not available** | Use placeholder images |
| **Map API quota exceeded** | Fallback to text display |
| **Local storage full** | Show warning, clear old data |
| **Slow network** | Show loading states, optimize |
| **Browser compatibility** | Test on multiple browsers |
| **Mobile limitations** | Responsive design, touch-friendly |

### Deliverables
- Enhanced frontend design
- Advanced features
- Performance optimizations
- Accessibility improvements
- Updated documentation

### Success Criteria
- UI is visually appealing
- Features work as expected
- Performance is improved
- Accessibility score is high
- User feedback is positive

---

## Summary

This implementation plan provides a structured approach to building the AI-powered restaurant recommendation system. Each phase builds upon the previous one, with clear objectives, tasks, edge cases, and success criteria.

### Key Principles
- **Incremental development**: Each phase delivers working functionality
- **Test-driven approach**: Comprehensive testing at each phase
- **Error handling**: Robust edge case handling throughout
- **Performance**: Continuous performance monitoring
- **Documentation**: Clear documentation for each phase

### Risk Mitigation
- **LLM reliability**: Fallback mechanisms for LLM failures
- **Data quality**: Robust data validation and cleaning
- **Performance**: Caching and optimization strategies
- **Deployment**: Multiple deployment options for flexibility

### Next Steps
1. Begin with Phase 0 (Project Setup)
2. Follow phases sequentially
3. Adapt plan based on learnings
4. Document deviations and decisions
5. Continuously test and iterate
