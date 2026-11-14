# Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

## Overview
You are tasked with building an AI-powered restaurant recommendation service inspired by Zomato. The system should intelligently suggest restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

## Problem Context
Restaurant discovery is challenging due to the overwhelming number of options available. Users often struggle to find restaurants that match their specific preferences across multiple dimensions: location, budget, cuisine type, quality ratings, and personal requirements (e.g., family-friendly, quick service). Traditional search interfaces rely on rigid filters that don't capture nuanced preferences or provide personalized explanations for recommendations.

## Objective
Design and implement an application that:
- Takes user preferences (such as location, budget, cuisine, and ratings)
- Uses a real-world dataset of restaurants
- Leverages an LLM to generate personalized, human-like recommendations
- Displays clear and useful results to the user

## Key Requirements

### 1. Data Source
- Use the Zomato dataset from Hugging Face: https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- Extract relevant fields: restaurant name, location, cuisine, cost, rating, etc.

### 2. User Input
Collect user preferences:
- **Location** (e.g., Delhi, Bangalore)
- **Budget** (low, medium, high)
- **Cuisine** (e.g., Italian, Chinese)
- **Minimum rating**
- **Additional preferences** (e.g., family-friendly, quick service) - optional free text

### 3. System Workflow

#### Data Ingestion
- Load and preprocess the Zomato dataset from Hugging Face
- Normalize and clean the data
- Store in a format optimized for querying

#### Integration Layer
- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

#### Recommendation Engine
- Use the LLM to:
  - Rank restaurants
  - Provide explanations (why each recommendation fits)
  - Optionally summarize choices

#### Output Display
- Present top recommendations in a user-friendly format:
  - Restaurant Name
  - Cuisine
  - Rating
  - Estimated Cost
  - AI-generated explanation

## Technical Constraints

### LLM Provider
- **Primary LLM**: Groq (for fast inference)
- **Alternative options**: Google AI Studio, OpenAI, etc.

### Deployment Strategy
- **Initial deployment**: Streamlit (simple, all-in-one deployment)
- **Advanced deployment**: Backend on Railway, Frontend on Vercel

### AI Tools
The project should be developed using modern AI-assisted development tools:
- Cursor
- Windsurf
- VS Code + Claude/GitHub Copilot
- Antigravity
- Qoder

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

## Related Documentation
- [Architecture](./architecture.md) - Detailed technical architecture
- [Implementation Plan](./implementation-plan.md) - Phase-wise implementation approach
- [Edge Cases](./edgecase.md) - Edge case handling strategies
- [Evaluation](./eval.md) - Testing and evaluation criteria
