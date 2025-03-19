from abc import ABC, abstractmethod
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MonitorModel(ABC):
    @abstractmethod
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        """Update the game state based on provided updates."""
        pass

class InventoryMonitor(MonitorModel):
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        """Update the inventory in the game state."""
        inventory_updates = updates.get("inventory", {})
        add_items: List[str] = inventory_updates.get("add", [])
        remove_items: List[str] = inventory_updates.get("remove", [])

        # Initialize inventory if not present
        if "inventory" not in game_state.state:
            print("initializing inventory")
            game_state.state["inventory"] = []

        if add_items:
            print("adding items to inventory:", add_items)
            game_state.state["inventory"].extend(add_items)

        if remove_items:
            print("removing items from inventory:", remove_items)
            for item in remove_items:
                if item in game_state.state["inventory"]:
                    game_state.state["inventory"].remove(item)

class MapMonitor(MonitorModel):
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        """Update the location in the game state."""
        new_location = updates.get("location", None)
        if new_location:
            print("new location:", new_location)
            # Initialize location if not present
            if "location" not in game_state.state:
                game_state.state["location"] = new_location
            else:
                game_state.state["location"] = new_location
            logger.info(f"Updated location to: {new_location}")

class HealthMonitor(MonitorModel):
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        health_change = updates.get("health", 0)
        if health_change:
            print("health change:", health_change)
            if "health" not in game_state.state:
                game_state.state["health"] = 100
            game_state.state["health"] += health_change
            game_state.state["health"] = max(0, min(100, game_state.state["health"]))
            logger.info(f"Updated health to: {game_state.state['health']}")








