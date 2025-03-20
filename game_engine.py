#game_engine.py
import tkinter as tk
from typing import List, Optional, Dict
from game_state import GameState
from narrative_model import MainNarrativeModel
from state_update_model import StateUpdateModel
from game_gui import GameGUI
from dotenv import load_dotenv
import os

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class GameEngine:
    def __init__(self, initial_state: Dict, system_prompt_narrative: str, system_prompt_updates: str, monitors: List['MonitorModel'], initial_message: Optional[str] = None):
        """Initialize the game engine with state, prompts, monitors, and optional initial message."""
        self.game_state = GameState(initial_state)
        self.narrative_model = MainNarrativeModel(api_key, system_prompt=system_prompt_narrative)
        self.state_update_model = StateUpdateModel(api_key, system_prompt=system_prompt_updates)
        self.monitors = monitors
        self.history: List[Dict] = []
        self.initial_message = initial_message

        self.root = tk.Tk()
        self.gui = GameGUI(self.root, self.process_input)

        if self.initial_message:
            self.gui.display(self.initial_message)
            self.history.append({"role": "assistant", "content": self.initial_message})

        self.gui.update_state_label(self.game_state.format_state())

    def run(self) -> None:
        """Start the game loop."""
        self.root.mainloop()

    def process_input(self, event: tk.Event) -> None:
        """Process user input and update the game."""
        user_input = self.gui.input_field.get()
        self.gui.input_field.delete(0, tk.END)
        self.history.append({"role": "user", "content": user_input})

        narrative = self.narrative_model.generate_narrative(user_input, self.game_state, self.history)
        self.gui.display(narrative)
        self.history.append({"role": "assistant", "content": narrative})

        updates, error_message = self.state_update_model.analyze_narrative(user_input, narrative, self.game_state)
        if error_message:
            self.gui.display(f"Error: {error_message}")
        else:
            for monitor in self.monitors:
                monitor.update_state(updates, self.game_state)
            self.gui.update_state_label(self.game_state.format_state())