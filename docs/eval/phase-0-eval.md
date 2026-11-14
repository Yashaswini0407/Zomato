# Phase 0 Evaluation Criteria: Project Setup & Configuration

## Overview
This document defines the evaluation criteria for Phase 0: Project Setup & Configuration.

## Success Criteria

### 1. Repository Initialization
- [ ] Git repository initialized successfully
- [ ] `.gitignore` file created with appropriate patterns
- [ ] README.md created with project overview
- [ ] Directory structure matches architecture specification

**Evaluation Method**: Manual inspection of repository structure and files

**Pass Criteria**: All items checked and files exist with correct content

---

### 2. Environment Setup
- [ ] Python virtual environment created (Python 3.11+)
- [ ] `requirements.txt` contains all required dependencies
- [ ] All dependencies install without errors
- [ ] `.env.example` file created with all required variables

**Evaluation Method**:
```bash
python --version  # Should be 3.11+
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -c "import streamlit; import pandas; import groq; print('All imports successful')"
```

**Pass Criteria**: All commands execute successfully, no import errors

---

### 3. Configuration Management
- [ ] `src/app/config.py` created with configuration classes
- [ ] Configuration loads from environment variables
- [ ] All required environment variables defined:
  - `LLM_PROVIDER`
  - `LLM_API_KEY`
  - `LLM_MODEL`
  - `DATA_PATH`
  - `MAX_CANDIDATES`
  - `BUDGET_LOW_MAX`
  - `BUDGET_MEDIUM_MAX`
- [ ] Configuration validation works (raises error on missing required vars)
- [ ] Default values provided for optional variables

**Evaluation Method**:
```python
# Test configuration loading
from app.config import Settings
settings = Settings()
assert settings.llm_provider == "groq"
assert settings.max_candidates == 30
assert settings.budget_low_max == 500
```

**Pass Criteria**: Configuration loads correctly, validation works, all variables accessible

---

### 4. Project Structure
- [ ] All directories created as per architecture:
  - `docs/`
  - `data/raw/`
  - `data/processed/`
  - `src/app/models/`
  - `src/app/ingestion/`
  - `src/app/data/`
  - `src/app/services/`
  - `src/app/api/`
  - `tests/`
  - `scripts/`
- [ ] `__init__.py` files in all Python packages
- [ ] File structure is clean and organized

**Evaluation Method**: Manual inspection of directory tree

**Pass Criteria**: All directories exist, structure matches specification

---

## Functional Tests

### Test 1: Environment Import Test
```bash
python -c "
import sys
print(f'Python version: {sys.version}')
import streamlit
import pandas
import datasets
import pydantic
import groq
print('All core dependencies imported successfully')
"
```

**Expected Output**: All imports successful, no errors

**Pass/Fail**: Pass if no import errors

---

### Test 2: Configuration Loading Test
```python
# test_config.py
import os
from dotenv import load_dotenv
from app.config import Settings

# Test with .env.example
load_dotenv('.env.example')
try:
    settings = Settings()
    print('Configuration loaded successfully')
    print(f'LLM Provider: {settings.llm_provider}')
    print(f'Max Candidates: {settings.max_candidates}')
except Exception as e:
    print(f'Configuration loading failed: {e}')
    sys.exit(1)
```

**Expected Output**: Configuration loads without errors, values are correct

**Pass/Fail**: Pass if configuration loads and values are accessible

---

### Test 3: Directory Structure Test
```bash
# Check all required directories exist
required_dirs=(
    "docs"
    "data/raw"
    "data/processed"
    "src/app/models"
    "src/app/ingestion"
    "src/app/data"
    "src/app/services"
    "src/app/api"
    "tests"
    "scripts"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "✗ $dir missing"
        exit 1
    fi
done
echo "All directories present"
```

**Expected Output**: All directories exist

**Pass/Fail**: Pass if all directories are present

---

## Quality Checks

### Code Quality
- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints used where appropriate
- [ ] Docstrings present for all functions and classes
- [ ] No hardcoded values (use configuration)

**Evaluation Method**: Code review and linting with flake8/black

**Pass Criteria**: Code passes linting, style guidelines followed

---

### Documentation
- [ ] README.md contains:
  - Project description
  - Installation instructions
  - Usage instructions
  - Configuration guide
- [ ] .env.example has comments explaining each variable
- [ ] config.py has docstrings for configuration fields

**Evaluation Method**: Manual review of documentation

**Pass Criteria**: Documentation is complete and clear

---

## Edge Case Handling

### Edge Case 1: Missing .env File
**Scenario**: .env file not present

**Expected Behavior**: Configuration should load with defaults or raise clear error

**Test**:
```bash
rm .env  # Remove .env if exists
python -c "from app.config import Settings; Settings()"
```

**Expected**: Either loads with defaults or raises clear error message

**Pass/Fail**: Pass if behavior is graceful and error message is clear

---

### Edge Case 2: Invalid Environment Variable
**Scenario**: Invalid value for environment variable (e.g., MAX_CANDIDATES = "abc")

**Expected Behavior**: Configuration validation should catch and raise clear error

**Test**:
```bash
export MAX_CANDIDATES="abc"
python -c "from app.config import Settings; Settings()"
```

**Expected**: ValidationError with clear message about invalid value

**Pass/Fail**: Pass if validation catches error with clear message

---

### Edge Case 3: Python Version Mismatch
**Scenario**: Python version < 3.11

**Expected Behavior**: Should warn or fail with clear message

**Test**: Check with Python 3.10 or lower

**Expected**: Clear error about Python version requirement

**Pass/Fail**: Pass if version check exists and message is clear

---

## Performance Criteria

- [ ] Configuration loading completes in < 100ms
- [ ] Dependency installation completes in < 2 minutes
- [ ] Directory creation completes instantly

**Evaluation Method**: Timing tests

**Pass Criteria**: All operations complete within time limits

---

## Security Checklist

- [ ] .env is in .gitignore
- [ ] .env.example does not contain real secrets
- [ ] No hardcoded API keys or secrets in code
- [ ] README does not contain sensitive information

**Evaluation Method**: Manual review and grep for secrets

**Pass Criteria**: No secrets in repository, proper .gitignore

---

## Final Acceptance Criteria

### Must Have (Blocking)
- [ ] Git repository initialized
- [ ] Python 3.11+ environment working
- [ ] All dependencies installable
- [ ] Configuration system functional
- [ ] Directory structure complete
- [ ] No secrets in repository

### Should Have (Non-blocking but recommended)
- [ ] Code follows style guidelines
- [ ] Documentation complete
- [ ] Type hints present
- [ ] Configuration validation robust

### Nice to Have (Optional)
- [ ] Pre-commit hooks configured
- [ ] CI/CD pipeline set up
- [ ] Automated tests for configuration

---

## Sign-off

**Phase 0 Status**: [ ] Pass / [ ] Fail

**Evaluator**: _______________

**Date**: _______________

**Notes**: _________________________________
