import logging
from game_engine import GameEngine
from monitor_models import InventoryMonitor, MapMonitor, HealthMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)

# System prompts
SYSTEM_PROMPT_NARRATIVE = """
You are the narrator of a text-based adventure game. Based on the player's input and the conversation history, generate a narrative response that advances the story. Keep it immersive and concise.
"""

SYSTEM_PROMPT_UPDATES = """
You are an assistant that analyzes both the player's input and the narrative text from a text-based adventure game to extract state updates. Based on the player's input and the narrative, provide a JSON object with updates for the game state. The possible updates include:

- "inventory": an object with "add" (list of items to add) and "remove" (list of items to remove). | ONLY RESPOND WITH: {"inventory": {"add": [string], "remove": [string]}}
- "location": the new location if the player has moved. | ONLY RESPOND WITH: {"location": string}
- "health": the new health value if the player's health has changed. | ONLY RESPOND WITH: {"health": integer (0-100)}
- "map": the new map if the player has moved to a new location. | ONLY RESPOND WITH: {"map": {string: [string]}

If there are no updates, output an empty object.
Output only the JSON object without any additional text.
"""

# Initial state and monitors
initial_state = {
    "health": 100,
    "inventory": ["sword"],
    "location": "cave",
    "map": {"cave": ["forest"]}
}
monitors = [InventoryMonitor(), MapMonitor(), HealthMonitor()]
initial_message = "You find yourself in a dimly lit cave with a sword by your side."

# Run the game
if __name__ == "__main__":
    game = GameEngine(
        initial_state=initial_state,
        system_prompt_narrative=SYSTEM_PROMPT_NARRATIVE,
        system_prompt_updates=SYSTEM_PROMPT_UPDATES,
        monitors=monitors,
        initial_message=initial_message
    )
    game.run()