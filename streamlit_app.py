"""
Streamlit UI for restaurant recommendations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from pathlib import Path

# Load from .env for local development, Streamlit secrets for cloud
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

import streamlit as st
import pandas as pd
from src.app.services.orchestrator import RecommendationOrchestrator
from src.app.data.repository import ParquetRepository
from src.app.config import get_settings
from src.app.models.restaurant import BudgetBand


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Restaurant Recommendations",
        page_icon="🍽️",
        layout="wide"
    )

    st.title("🍽️ AI-Powered Restaurant Recommendations")
    st.markdown("Get personalized restaurant recommendations based on your preferences")

    # Check for API key
    api_key = os.environ.get("LLM_API_KEY") or st.secrets.get("LLM_API_KEY", "")
    if not api_key:
        st.error("⚠️ LLM API Key not configured. Please set LLM_API_KEY in Streamlit Cloud secrets or .env file.")
        st.stop()

    # Load data
    settings = get_settings()
    repository = ParquetRepository(settings.data_path)
    orchestrator = RecommendationOrchestrator(repository)

    # Sidebar for filters
    st.sidebar.header("Your Preferences")

    # Location
    locations = repository.get_locations()
    location = st.sidebar.selectbox(
        "Location",
        options=locations,
        index=0
    )

    # Budget
    budget = st.sidebar.selectbox(
        "Budget",
        options=[BudgetBand.LOW, BudgetBand.MEDIUM, BudgetBand.HIGH],
        format_func=lambda x: x.value.title(),
        index=1
    )

    # Cuisine
    cuisines = repository.get_cuisines()
    cuisine = st.sidebar.selectbox(
        "Cuisine",
        options=cuisines,
        index=0
    )

    # Minimum rating
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=3.5,
        step=0.1
    )

    # Additional preferences
    additional_prefs = st.sidebar.text_area(
        "Additional Preferences (optional)",
        placeholder="e.g., outdoor seating, romantic atmosphere, family-friendly...",
        max_chars=500
    )

    # Number of recommendations
    top_k = st.sidebar.slider(
        "Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    # Get recommendations button
    if st.sidebar.button("Get Recommendations", type="primary"):
        with st.spinner("Finding the best restaurants for you..."):
            try:
                preferences = {
                    "location": location,
                    "budget": budget,
                    "cuisine": cuisine,
                    "min_rating": min_rating,
                    "additional_preferences": additional_prefs if additional_prefs else None,
                    "top_k": top_k
                }

                response = orchestrator.execute(preferences)

                # Display summary
                if response.summary:
                    st.info(response.summary)

                # Display recommendations
                if response.recommendations:
                    st.subheader(f"Top {len(response.recommendations)} Recommendations")

                    for rec in response.recommendations:
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                st.metric("Rank", rec.rank)
                                st.metric("Rating", f"{rec.restaurant.rating:.1f}")
                                st.metric("Cost", f"INR {int(rec.restaurant.estimated_cost)}")
                            
                            with col2:
                                st.markdown(f"### {rec.restaurant.name}")
                                st.markdown(f"Location: {rec.restaurant.location}")
                                st.markdown(f"Cuisines: {', '.join(rec.restaurant.cuisines).title()}")
                                st.markdown(f"Budget: {rec.restaurant.budget_band.value.title()}")
                                st.markdown("---")
                                st.markdown(f"**Why this restaurant?**")
                                st.markdown(rec.explanation)
                            
                            st.divider()

                    # Display metadata
                    if response.meta:
                        with st.expander("Request Details"):
                            st.json(response.meta)
                else:
                    st.warning("No recommendations found. Try adjusting your criteria.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error("Please try again or adjust your preferences.")

    # Display info about the system
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("This system uses AI to provide personalized restaurant recommendations based on your preferences.")
    st.sidebar.markdown(f"**LLM Provider**: Groq")
    st.sidebar.markdown(f"**Model**: {settings.llm_model}")
    st.sidebar.markdown(f"**Total Restaurants**: {len(repository.get_all())}")


if __name__ == "__main__":
    main()
