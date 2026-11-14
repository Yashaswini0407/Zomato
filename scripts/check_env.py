"""
Script to check and setup .env file
"""

from pathlib import Path

print("Checking .env file...")

env_path = Path(".env")
env_example_path = Path(".env.example")

if env_path.exists():
    content = env_path.read_text()
    if content.strip():
        print(f".env file exists and has content ({len(content)} characters)")
        print("First 200 characters:")
        print(content[:200])
    else:
        print(".env file exists but is EMPTY!")
        print("Please add your API key to the .env file")
        print("\nExpected format:")
        print("LLM_API_KEY=gsk_your_actual_api_key_here")
else:
    print(".env file does not exist")
    print("Creating from .env.example...")
    if env_example_path.exists():
        content = env_example_path.read_text()
        env_path.write_text(content)
        print(f".env file created from .env.example")
        print("Please edit .env and replace 'your-groq-api-key-here' with your actual API key")
