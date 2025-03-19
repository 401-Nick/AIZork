import json
from typing import Dict

class GameState:
    def __init__(self, initial_state: Dict):
        """Initialize the game state with a dictionary."""
        self.state = initial_state

    def to_json(self) -> str:
        """Return the state as a JSON string."""
        return json.dumps(self.state, indent=2)

    def format_state(self) -> str:
        """Format the state for readable display in the GUI."""
        lines = []
        for key, value in self.state.items():
            if isinstance(value, list):
                value_str = ', '.join(map(str, value)) if value else 'empty'
            elif isinstance(value, dict):
                value_str = json.dumps(value, indent=2)
            else:
                value_str = str(value)
            lines.append(f"{key}: {value_str}")
        return '\n'.join(lines)