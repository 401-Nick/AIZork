import json
from openai import OpenAI
from typing import Dict, Tuple, Optional
import logging
from dotenv import load_dotenv
import os   

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

logger = logging.getLogger(__name__)



class StateUpdateModel:
    def __init__(self, api_key: str, system_prompt: str):
        """Initialize the state update model with API key and system prompt."""
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = system_prompt

    def analyze_narrative(self, user_input: str, narrative: str) -> Tuple[Dict, Optional[str]]:
        """Analyze user input and narrative to extract state updates."""
        prompt = f"{self.system_prompt}\n\nPlayer Input: {user_input}\nNarrative: {narrative}"
        print("THE MODEL IS BEING FED THE FOLLOWING PROMPT:")
        print(prompt)
        print("----------------")

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.2,
                max_tokens=300
            )
            response_text = response.choices[0].message.content
            print("THE MODEL'S RESPONSE IS:")
            print(response_text)
            print("----------------")
        except Exception as e:
            logger.error(f"Failed to get response from OpenAI API: {e}")
            return {}, "Failed to get response from API."

        try:
            updates = json.loads(response_text)
            if not isinstance(updates, dict):
                logger.warning("State updates are not a dictionary.")
                return {}, "Invalid response format from API."
            return updates, None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse state updates as JSON: {response_text}")
            return {}, "Failed to parse response."