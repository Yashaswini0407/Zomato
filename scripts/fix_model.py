"""
Script to update .env with correct model name
"""

from pathlib import Path

env_path = Path(".env")
content = env_path.read_text()

# Replace the invalid model name with a valid one
updated_content = content.replace("llama-3.3-70b-versatile", "mixtral-8x7b-32768")

env_path.write_text(updated_content)
print("Updated .env file with correct model name: mixtral-8x7b-32768")
print("\nNew content:")
print(updated_content)
