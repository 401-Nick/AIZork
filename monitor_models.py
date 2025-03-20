# monitor_models.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable
import logging
from game_state import GameState  # Import GameState for type hints

logger = logging.getLogger(__name__)

class MonitorModel(ABC):
    @abstractmethod
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        """Update the game state based on provided updates."""
        pass

class GenericMonitor(MonitorModel):
    def __init__(self, key: str, update_func: Callable[[Any, 'GameState'], None]):
        """
        Initialize a generic monitor.
        
        :param key: The key in the updates dictionary to monitor.
        :param update_func: A function that updates the game state based on the update data.
        """
        self.key = key
        self.update_func = update_func

    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        """Update the game state if the monitored key is in the updates."""
        if self.key in updates:
            update_data = updates[self.key]
            self.update_func(update_data, game_state)
            logger.info(f"Updated state for key '{self.key}'")

# CUSTOM MONITORS -------------------
# Add your custom monitor logic below

def update_inventory(update_data: Dict, game_state: GameState) -> None:
    """Update the inventory in the game state."""
    game_state.state["inventory"] = update_data

def update_location(update_data: str, game_state: GameState) -> None:
    """Update the location in the game state."""
    game_state.state["location"] = update_data

def update_health(update_data: int, game_state: GameState) -> None:
    """Update the health in the game state with bounds checking."""
    if "health" not in game_state.state:
        game_state.state["health"] = 100
    game_state.state["health"] = max(0, min(100, update_data))

def update_limbs(update_data: Dict, game_state: GameState) -> None:
    """Update the limb states in the game state."""
    if "limb" not in game_state.state:
        game_state.state["limb"] = {}
    for limb_name, limb_data in update_data.items():
        game_state.state["limb"][limb_name] = limb_data

def update_skill(update_data: Dict, game_state: GameState) -> None:
    """Update the skill in the game state."""
    if "skill" not in game_state.state:
        game_state.state["skill"] = {}
    for skill_name, skill_level in update_data.items():
        game_state.state["skill"][skill_name] = skill_level

def update_time(update_data: str, game_state: GameState) -> None:
    """Update the time in the game state."""
    game_state.state["time"] = update_data


def update_relationships(update_data: Dict, game_state: GameState) -> None:
    """Update the relationships in the game state."""
    if "relationships" not in game_state.state:
        game_state.state["relationships"] = {}
    for character, relationship_score in update_data.items():
        game_state.state["relationships"][character] = relationship_score

def update_armor(update_data: Dict, game_state: GameState) -> None:
    """Update the armor in the game state."""
    if "armor" not in game_state.state:
        game_state.state["armor"] = {}
    for armor_part, armor_data in update_data.items():
        game_state.state["armor"][armor_part] = armor_data
# -----------------------------------