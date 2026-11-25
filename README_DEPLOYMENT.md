# Streamlit Deployment README

## Quick Start

This application is ready for deployment to Streamlit Cloud.

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

### Deployment to Streamlit Cloud

1. **Push code to GitHub** (if not already done):
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy to Streamlit Cloud**:
   - Go to https://cloud.streamlit.io
   - Click "New app"
   - Select your repository
   - Main file: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Secrets**:
   - In Streamlit Cloud, go to app settings → Secrets
   - Add: `LLM_API_KEY` = your Groq API key
   - Save

4. **Redeploy** (after adding secrets):
   - Streamlit will automatically redeploy

### Configuration Files

- `.streamlit/config.toml` - Theme and client settings
- `.streamlit/secrets.toml.example` - Secrets template (for local dev)
- Streamlit Cloud Secrets - Production secrets (configured in cloud)

### Data File

The application uses `data/processed/restaurants.parquet` which is included in the repository.

### Troubleshooting

**App fails to start**: Check that `restaurants.parquet` exists in `data/processed/`

**LLM API errors**: Verify `LLM_API_KEY` is set in Streamlit Cloud secrets

**Data loading errors**: Ensure pyarrow==14.0.1 is installed
