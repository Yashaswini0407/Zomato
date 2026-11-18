"""
Test the orchestrator with real data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from src.app.services.orchestrator import RecommendationOrchestrator
from src.app.data.repository import ParquetRepository
from src.app.config import get_settings


def test_orchestrator():
    """Test the orchestrator with real data."""
    print("Testing Recommendation Orchestrator...")
    
    settings = get_settings()
    repository = ParquetRepository(settings.data_path)
    orchestrator = RecommendationOrchestrator(repository)
    
    preferences = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "South Indian",  # Changed to match available data
        "min_rating": 3.5,  # Lowered to get more results
        "additional_preferences": None,
        "top_k": 3
    }
    
    print(f"\nInput preferences: {preferences}")
    
    response = orchestrator.execute(preferences)
    
    print(f"\nSummary: {response.summary}")
    print(f"\nRecommendations: {len(response.recommendations)}")
    
    for rec in response.recommendations:
        print(f"\nRank {rec.rank}: {rec.restaurant.name}")
        print(f"  Location: {rec.restaurant.location}")
        print(f"  Rating: {rec.restaurant.rating}")
        print(f"  Cost: INR {rec.restaurant.estimated_cost}")
        print(f"  Explanation: {rec.explanation}")
    
    print(f"\nMeta: {response.meta}")
    print("\n[SUCCESS] Orchestrator test completed!")


if __name__ == "__main__":
    test_orchestrator()
