# main.py
import logging
from game_engine import GameEngine
from monitor_models import * # Import all monitors

# Define system prompts as constants for clarity and reusability
SYSTEM_PROMPT_NARRATIVE = """
You are the narrator of a text-based adventure game. Based on the player's input and the conversation history, generate an interactive narrative response that remains hyper engaging and immersive.
"""

SYSTEM_PROMPT_UPDATES = """
You are a game engine that analyzes the player's input and the narrative text from a text-based adventure game to extract state updates. Based on the input and narrative, provide a JSON object with updates for the game state. The possible updates are:
Multiple updates can be batched in a single response.

IF AN ITEM THE USER MENTIONS ISN'T IN THE GAME, DO NOT ALLOW THE USER TO SPAWN IT.
"I pick up the coin" - "You look around but don't see a coin"
"I drop the coin" - "You search your inventory but don't see a coin"


"inventory": List[str] - List of items in the inventory.
"location": Dict[str, Dict[str, str]] - Current location and its shortened description. GENERATE ADDITIONAL LOCATIONS BASED ON THE USER'S INPUT.
"health": int - Current health level.
"skill": Dict[str, int] - Skill levels.
"limb": Dict[str, Dict[str, int]] - Limb states. {"left_leg": {"hp": 100, "status": "(healthy|injured|decapitated|amputated|broken|fractured|)"}}
"map": Dict[str, List[str]] - Map of locations and their connections. ADD LOCATIONS TO THE MAP AS THE USER EXPLORES THE GAME WORLD.
"time": str - Current time. (UPDATE THIS EVERY INTERACTION)
"relationships": Dict[str, int] (-100: Hostile, 0: Neutral, 100: Friendly) - Updated relationship scores with characters, reflecting changes in their perception of the player based on actions and narrative events.
"armor": Dict[str, Dict[str, int]] - Armor states. {"head": {"name": "knight helmet", "hp": 100, "status": "(perfect|good|damaged|destroyed|)"}}


DO NOT ALLOW TO USER TO SPAWN ITEMS OR DIRECTLY MODIFY THE GAME STATE. REMAIN 100% HYPERREALISTIC TO THE GAME STATE.

IF THE GAME DOESN'T INCLUDE MAGIC, DO NOT ALLOW THE USER TO CAST SPELLS.

You can batch 

If updates are needed, return an multiple objects within {"key": value}.
If no updates are needed, return an empty object: {}
ONLY RETURN THE RAW JSON OBJECT.
DO NOT DUPLICATE KEYS OR ITEMS.
HERE IS THE CURRENT GAME STATE:
"""

# Initial game state with adjusted values for a negotiation-themed game
INITIAL_STATE = {
    "health": 100,
    "coordinates": [0, 0],
    "inventory": ["Pipboy", "Food", "Water", "9mm Ammo", "9mm Pistol"],
    "relationships": {
        "NCR": 0,
        "Caesars Legion": 0,
        "Brotherhood of Steel": 0,
    },
    "location": {
        "Private Office": {"coordinates": [0, 0], "description": "Private Office", "objects": ["Pen", "Paper"]},
        "Conference Room": {"coordinates": [1, 0], "description": "Conference Room", "objects": [""]},
        "Lobby": {"coordinates": [0, 1], "description": "Lobby", "objects": []}
    },
    "map": {
        "Building": ["Private Office", "Conference Room", "Lobby"]
    },
    "skill": {
        "strength": 50,
        "perception": 50,
        "endurance": 50,
        "charisma": 50,
        "intelligence": 50,
        "agility": 50,
        "luck": 50
    },
    "limb": {
        "right_hand": {"hp": 100, "status": "healthy", "holding": "nothing"},
        "left_hand": {"hp": 100, "status": "healthy", "holding": "nothing"},
        "left_leg": {"hp": 100, "status": "healthy"},
        "right_leg": {"hp": 100, "status": "healthy"},
        "left_arm": {"hp": 100, "status": "healthy"},
        "right_arm": {"hp": 100, "status": "healthy"},
        "head": {"hp": 100, "status": "healthy"},
        "torso": {"hp": 100, "status": "healthy"},
        "stomach": {"hp": 100, "status": "healthy"}
    },
    "time": "2:32 PM",
    "armor":{
        "head": {"name": "t-60 helmet", "hp": 100, "status": "perfect"},
        "chest": {"name": "t-60 chestplate", "hp": 100, "status": "perfect"},
        "legs": {"name": "t-60 leggings", "hp": 100, "status": "perfect"},
        "gloves": {"name": "t-60 gloves", "hp": 100, "status": "perfect"},
        "boots": {"name": "t-60 boots", "hp": 100, "status": "perfect"}
    },
}

# List of monitors to track and update game state GenericMonitor(key, update_function)
MONITORS = [
    GenericMonitor("inventory", update_inventory),
    GenericMonitor("location", update_location),
    GenericMonitor("health", update_health),
    GenericMonitor("limb", update_limbs),
    GenericMonitor("skill", update_skill),
    GenericMonitor("time", update_time),
    GenericMonitor("relationships", update_relationships),
    GenericMonitor("armor", update_armor)
]

# Initial message to set the scene for the player
INITIAL_MESSAGE = "You find yourself in New Vegas. A once prosperous city, now a desolate gated city full of degenerate criminals and various factions."

# Main execution block
if __name__ == "__main__":
    try:
        # Initialize and run the game
        game = GameEngine(
            initial_state=INITIAL_STATE,
            system_prompt_narrative=SYSTEM_PROMPT_NARRATIVE,
            system_prompt_updates=SYSTEM_PROMPT_UPDATES,
            monitors=MONITORS,
            initial_message=INITIAL_MESSAGE
        )
        logging.info("Game started successfully.")
        game.run()
    except Exception as e:
        logging.error(f"Failed to start the game: {str(e)}")
        raise