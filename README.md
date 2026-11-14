# AI-Powered Restaurant Recommendation System (Zomato Use Case)

An intelligent restaurant recommendation service inspired by Zomato that combines structured data with Large Language Model (LLM) capabilities to provide personalized, human-like restaurant suggestions.

## Overview

This system intelligently suggests restaurants based on user preferences by:
- Taking user preferences (location, budget, cuisine, ratings)
- Using a real-world dataset of restaurants from Hugging Face
- Leveraging an LLM (Groq) to generate personalized recommendations
- Displaying clear and useful results with AI-generated explanations

## Features

- **Personalized Recommendations**: AI-powered suggestions based on location, budget, cuisine, and ratings
- **Explainable AI**: Each recommendation includes a clear explanation of why it fits your preferences
- **Grounded Results**: All recommendations come from the actual Zomato dataset (no hallucinations)
- **User-Friendly Interface**: Clean Streamlit web interface for easy interaction
- **Fast Performance**: Powered by Groq for fast LLM inference

## Tech Stack

- **Backend**: Python 3.11+
- **LLM Provider**: Groq (fast inference)
- **Data Source**: Hugging Face (ManikaSaini/zomato-restaurant-recommendation)
- **Frontend**: Streamlit (initial), React + Vite (advanced)
- **Deployment**: Streamlit Cloud (initial), Railway + Vercel (advanced)

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Groq API key (get one at https://console.groq.com/keys)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Zomato
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

5. Run data ingestion:
```bash
python scripts/ingest.py
```

6. Start the application:
```bash
streamlit run src/app/main.py
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file based on `.env.example`:

```env
LLM_PROVIDER=groq
LLM_API_KEY=your-groq-api-key-here
LLM_MODEL=mixtral-8x7b-32768
DATA_PATH=data/processed/restaurants.parquet
MAX_CANDIDATES=30
BUDGET_LOW_MAX=500
BUDGET_MEDIUM_MAX=1500
```

## Usage

1. Open the Streamlit application in your browser
2. Enter your preferences:
   - Location (e.g., Bangalore, Delhi)
   - Budget (low, medium, high)
   - Cuisine (e.g., Italian, Chinese)
   - Minimum rating (0-5)
   - Additional preferences (optional, e.g., "family-friendly")
3. Click "Get Recommendations"
4. View personalized recommendations with AI-generated explanations

## Project Structure

```
zomato-milestone/
├── docs/                      # Documentation
│   ├── ProblemStatement.md
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── edgecase.md
│   └── eval/                 # Evaluation criteria
├── data/                     # Data files
│   ├── raw/                  # Raw dataset cache
│   └── processed/            # Processed restaurant data
├── src/
│   └── app/
│       ├── config.py         # Configuration management
│       ├── models/           # Data models
│       ├── ingestion/        # Data ingestion pipeline
│       ├── data/             # Data access layer
│       ├── services/         # Business logic
│       └── api/              # API layer
├── tests/                    # Test suite
├── scripts/                  # Utility scripts
├── .env.example             # Environment variables template
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
flake8 src/app/
mypy src/app/
```

### Data Ingestion

To re-ingest the dataset from Hugging Face:

```bash
python scripts/ingest.py
```

## Deployment

### Streamlit Cloud (Initial)

1. Push code to GitHub
2. Create account on Streamlit Cloud (https://share.streamlit.io/)
3. Connect GitHub repository
4. Add environment variables in Streamlit settings
5. Deploy

### Railway + Vercel (Advanced)

See [implementation-plan.md](docs/implementation-plan.md) Phase 9 for detailed instructions.

## Documentation

- [Problem Statement](docs/ProblemStatement.md) - Project overview and requirements
- [Architecture](docs/architecture.md) - Technical architecture
- [Implementation Plan](docs/implementation-plan.md) - Phase-wise implementation plan
- [Edge Cases](docs/edgecase.md) - Edge case handling strategies
- [Evaluation](docs/eval/README.md) - Testing and evaluation criteria

## Success Criteria

1. **Accuracy**: Recommendations must come from the actual dataset (no hallucinations)
2. **Personalization**: Results should reflect user's specific preferences
3. **Explainability**: Each recommendation includes a clear, human-readable explanation
4. **Performance**: Reasonable response time for end-to-end recommendation flow
5. **Usability**: Intuitive interface for input and clear presentation of results

## Out of Scope (Initial Milestone)

- User accounts, saved favorites, or order placement
- Real-time restaurant availability or live Zomato API integration
- Fine-tuned custom models (use hosted LLM APIs)
- Geographic routing or map visualization
- Multi-user authentication
- Payment processing or reservations

## License

This project is for educational purposes.

## Acknowledgments

- Dataset: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) on Hugging Face
- LLM Provider: [Groq](https://groq.com/)
- Inspired by: [Zomato](https://www.zomato.com/)
