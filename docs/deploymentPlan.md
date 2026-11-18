# Streamlit Deployment Plan

## Overview

This document outlines the deployment strategy for the AI-Powered Restaurant Recommendation System on Streamlit Cloud.

**Target Deployment**: Streamlit Cloud
**Current Status**: Application ready for deployment (Phases 0-6 complete)
**Deployment Method**: Streamlit Cloud (cloud.streamlit.io)

---

## Prerequisites

### Required Accounts
- [ ] Streamlit Cloud account (free tier available)
- [ ] GitHub account (for code hosting)
- [ ] Groq API key (already configured in .env)

### Required Files
- [ ] `streamlit_app.py` - Main application file
- [ ] `requirements.txt` - Python dependencies
- [ ] `.streamlit/config.toml` - Streamlit configuration (optional)
- [ ] `.env` - Environment variables (secrets)

---

## Deployment Steps

### Step 1: Prepare for Deployment

#### 1.1 Create Streamlit Configuration
Create `.streamlit/config.toml` file:

```toml
[theme]
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

[client]
showErrorDetails = false
toolbarMode = "minimal"
maxUploadSize = 200

[logger]
level = "info"
```

#### 1.2 Update requirements.txt
Ensure all dependencies are pinned to specific versions

#### 1.3 Create .streamlit/secrets.toml
Create `.streamlit/secrets.toml` for secrets management:

```toml
# Secrets will be configured in Streamlit Cloud UI
# DO NOT commit actual secrets to this file
LLM_API_KEY = "Enter your Groq API key in Streamlit Cloud"
```

#### 1.4 Update .gitignore
Ensure `.env` and `.streamlit/secrets.toml` are in .gitignore

---

### Step 2: Push Code to GitHub

#### 2.1 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `zomato-milestone`
3. Make it Public or Private
4. Click "Create repository"

#### 2.2 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/zomato-milestone.git
git branch -M main
git push -u origin main
```

---

### Step 3: Deploy to Streamlit Cloud

#### 3.1 Sign Up/Login to Streamlit Cloud
1. Go to https://cloud.streamlit.io
2. Sign up or login with GitHub account
3. Authorize Streamlit Cloud to access your GitHub repositories

#### 3.2 Create New App
1. Click "New app" button
2. Select your repository: `zomato-milestone`
3. Select branch: `main`
4. Main file path: `streamlit_app.py`

#### 3.3 Configure Secrets
1. In the app settings, go to "Secrets"
2. Add secret:
   - Name: `LLM_API_KEY`
   - Value: Your Groq API key (gsk_...)
3. Click "Save"

#### 3.4 Deploy
1. Click "Deploy" button
2. Wait for deployment to complete (usually 1-2 minutes)
3. Streamlit will provide a URL like: `https://your-app-name.streamlit.app`

---

## Configuration Details

### Environment Variables

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `LLM_PROVIDER` | `groq` | Yes | LLM provider |
| `LLM_API_KEY` | `gsk_...` | Yes | Groq API key (secret) |
| `LLM_MODEL` | `qwen/qwen3.8-27b` | Yes | Groq model name |
| `MAX_CANDIDATES` | `30` | No | Max candidates for LLM |
| `BUDGET_LOW_MAX` | `500` | No | Low budget threshold |
| `BUDGET_MEDIUM_MAX` | `1500` | No | Medium budget threshold |

---

## Secrets Management

### Groq API Key

**Where to Store**: Streamlit Cloud Secrets

**How to Configure**:
1. Go to your app in Streamlit Cloud
2. Navigate to Settings → Secrets
3. Add secret:
   - Name: `LLM_API_KEY`
   - Value: Your Groq API key
4. Save

---

## Cost Analysis

### Streamlit Cloud Pricing (as of 2024)

| Plan | Price | Features |
|------|-------|----------|
| Free | $0/month | 1 app, 200 hours/month, community support |
| Basic | $20/month | 3 apps, 1000 hours/month, email support |
| Standard | $50/month | 10 apps, 5000 hours/month, priority support |

### Groq API Pricing

- **Free tier**: Available
- **Pay-per-use**: Very low cost (~$0.01-0.10 per 1K tokens)
- **Estimated cost**: <$1/month for typical usage

### Total Estimated Cost

**Free Tier**: $0/month (Streamlit) + Minimal (Groq API)
**Basic Tier**: $20/month (Streamlit) + Minimal (Groq API)

---

## Troubleshooting

### Common Issues

#### Issue 1: App fails to start
**Solutions**:
- Check requirements.txt for correct versions
- Verify pyarrow version compatibility
- Check Streamlit Cloud logs for errors

#### Issue 2: LLM API errors
**Solutions**:
- Verify LLM_API_KEY secret is set correctly
- Check Groq API status
- Verify model name is correct

---

## Post-Deployment Checklist

- [ ] App loads successfully in browser
- [ ] All UI elements render correctly
- [ ] Location dropdown shows all locations
- [ ] Budget dropdown works correctly
- [ ] Cuisine dropdown works correctly
- [ ] Rating slider works correctly
- [ ] "Get Recommendations" button works
- [ ] Recommendations display correctly
- [ ] LLM explanations are shown
- [ ] Restaurant details are accurate
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable (< 20s)
- [ ] Secrets are not exposed
- [ ] Logs are accessible
