import tkinter as tk
from typing import Callable

class GameGUI:
    def __init__(self, root: tk.Tk, process_input_callback: Callable[[tk.Event], None]):
        """Initialize the GUI with a root window and input callback."""
        self.root = root
        self.root.title("Text Adventure Game")

        # Output area
        self.output = tk.Text(self.root, height=20, width=80)
        self.output.pack(pady=10)

        # State display
        self.state_label = tk.Label(self.root, text="State: ", justify=tk.LEFT, anchor="nw")
        self.state_label.pack(pady=5)

        # Input field
        self.input_field = tk.Entry(self.root, width=50)
        self.input_field.pack(pady=5)
        self.input_field.bind("<Return>", process_input_callback)

    def display(self, text: str) -> None:
        """Display text in the output area."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def update_state_label(self, state_text: str) -> None:
        """Update the state display with formatted text."""
        self.state_label.config(text=f"State:\n{state_text}")