"""
LLM client for interacting with Groq API.
"""

import logging
from typing import Optional
from groq import Groq
from src.app.config import get_settings


logger = logging.getLogger(__name__)


class GroqClient:
    """
    Client for interacting with Groq LLM API.
    """

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the Groq client.

        Args:
            model: Model name to use
            api_key: API key for Groq
        """
        settings = get_settings()
        
        self.model = model or settings.llm_model
        self.api_key = api_key or settings.llm_api_key
        
        if not self.api_key:
            logger.warning("No API key provided. LLM calls will fail.")
        
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def complete(self, prompt: str, temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """
        Complete a prompt using the LLM.

        Args:
            prompt: The prompt to complete
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response

        Returns:
            LLM response text

        Raises:
            Exception: If API call fails
        """
        if not self.client:
            raise Exception("Groq client not initialized. Please provide API key.")
        
        logger.info(f"Sending request to Groq (model: {self.model})")
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides restaurant recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            result = response.choices[0].message.content
            logger.info(f"Received response from Groq ({len(result)} characters)")
            return result
            
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            raise Exception(f"LLM API call failed: {e}") from e
