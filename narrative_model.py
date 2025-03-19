from openai import OpenAI
from typing import List, Dict
import logging
from dotenv import load_dotenv
import os   

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

class MainNarrativeModel:
    def __init__(self, api_key: str, system_prompt: str):
        """Initialize the narrative model with API key and system prompt."""
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = system_prompt

    def generate_narrative(self, user_input: str, game_state: 'GameState', history: List[Dict]) -> str:
        """Generate a narrative based on user input, game state, and history."""
        # Limit history to the last 20 entries to manage token limits
        recent_history = history[-20:]
        messages = [{"role": "system", "content": self.system_prompt}] + recent_history

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to generate narrative: {e}")
            return "Something went wrong. Please try again."