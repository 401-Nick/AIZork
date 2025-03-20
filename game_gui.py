# game_gui.py
import tkinter as tk
from typing import Callable

class GameGUI:
    def __init__(self, root: tk.Tk, process_input_callback: Callable[[tk.Event], None]):
        """Initialize the GUI with a root window and input callback."""
        self.root = root
        self.root.title("Text Adventure Game")
        self.root.configure(bg='#2d2d2d')

        # Configure color scheme with a list of cycling colors
        self.colors = {
            'background': '#2d2d2d',
            'text': '#e0e0e0',
            'input_bg': '#3d3d3d',
            'state_bg': '#1d1d1d',
            'error': '#ff4444'
        }
        self.response_colors = ['#ff00ff', '#ffff00']
        self.color_index = 0

        # Output area with scrollbar
        self.output_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.output = tk.Text(self.output_frame, height=20, width=80, 
                            bg=self.colors['background'], fg=self.colors['text'],
                            wrap=tk.WORD, state=tk.DISABLED)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.output_frame, command=self.output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.config(yscrollcommand=self.scrollbar.set)
        
        # Configure text tags
        self.output.tag_config('error', foreground=self.colors['error'])
        self.output.tag_config('normal', foreground=self.colors['text'])
        self.output.tag_config('loading', foreground='#aaaaaa')  # Gray for loading text

        # State display
        self.state_frame = tk.Frame(self.root, bg=self.colors['state_bg'])
        self.state_frame.pack(pady=5, fill=tk.X)

        # to set the font size, use the FONT parameter as show
        #self.state_text = tk.Text(self.state_frame, font=('Arial', 12))
        
        self.state_text = tk.Text(self.state_frame,font=('Arial', 10), height=20, width=80, 
                                bg=self.colors['state_bg'], fg=self.colors['text'],
                                wrap=tk.WORD, state=tk.DISABLED)
        self.state_text.pack(padx=5, pady=5)

        # Input area
        self.input_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.input_frame.pack(pady=5, fill=tk.X)

        self.input_field = tk.Entry(self.input_frame, width=100, 
                                  bg=self.colors['input_bg'], fg=self.colors['text'],
                                  insertbackground=self.colors['text'])
        self.input_field.pack(side=tk.LEFT, padx=5)
        self.input_field.bind("<Return>", lambda event: self._handle_input(event, process_input_callback))
        self.input_field.bind("<Up>", self._prev_history)
        self.input_field.bind("<Down>", self._next_history)

        # Error display
        self.error_label = tk.Label(self.root, text="", fg=self.colors['error'],
                                  bg=self.colors['background'])
        self.error_label.pack()

        self.history = []
        self.history_pos = -1
        self.loading = False  # Track loading state
        self.loading_id = None  # Store animation ID

    def display(self, text: str, is_error: bool = False) -> None:
        """Display text in the output area with cycling colors or error styling."""
        self.output.config(state=tk.NORMAL)
        if is_error:
            tag = 'error'
        else:
            tag = f'color_{self.color_index}'
            self.output.tag_config(tag, foreground=self.response_colors[self.color_index])
            self.color_index = (self.color_index + 1) % len(self.response_colors)
        
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def update_state_label(self, state_text: str) -> None:
        """Update the state display with formatted text."""
        self.state_text.config(state=tk.NORMAL)
        self.state_text.delete(1.0, tk.END)
        self.state_text.insert(tk.END, state_text)
        self.state_text.config(state=tk.DISABLED)

    def show_error(self, message: str) -> None:
        """Display a temporary error message."""
        self.error_label.config(text=message)
        self.root.after(3000, lambda: self.error_label.config(text=""))

    def _handle_input(self, event: tk.Event, callback: Callable[[tk.Event], None]) -> None:
        """Handle Enter key press, show loading animation, and process input."""
        if self.loading:  # Prevent multiple submissions
            return

        command = self.input_field.get().strip()
        if not command:
            return

        self.history.append(command)
        self.history_pos = -1
        self.input_field.delete(0, tk.END)

        self.loading = True
        self._start_loading_animation()
        self.root.after(1000, lambda: self._process_input(event, callback))  # Simulate processing delay

    def _start_loading_animation(self) -> None:
        """Start the loading animation with cycling dots."""
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, "Loading", 'loading')
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)
        self._animate_loading_dots(0)

    def _animate_loading_dots(self, dot_count: int) -> None:
        """Animate loading dots (e.g., Loading..., Loading....)."""
        if not self.loading:
            return

        dots = "." * ((dot_count % 3) + 1)
        self.output.config(state=tk.NORMAL)
        self.output.delete("end-2l", "end-1l")  # Remove previous loading line
        self.output.insert(tk.END, f"Loading{dots}\n", 'loading')
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

        self.loading_id = self.root.after(200, lambda: self._animate_loading_dots(dot_count + 1))

    def _process_input(self, event: tk.Event, callback: Callable[[tk.Event], None]) -> None:
        """Process the input and stop the loading animation."""
        self.loading = False
        if self.loading_id:
            self.root.after_cancel(self.loading_id)
        self.output.config(state=tk.NORMAL)
        self.output.delete("end-2l", "end-1l")  # Remove loading text
        self.output.config(state=tk.DISABLED)
        callback(event)  # Call the original processing function

    def _prev_history(self, event=None) -> None:
        """Navigate up through command history."""
        if self.history_pos < len(self.history)-1:
            self.history_pos += 1
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.history[-(self.history_pos+1)])

    def _next_history(self, event=None) -> None:
        """Navigate down through command history."""
        if self.history_pos > 0:
            self.history_pos -= 1
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.history[-(self.history_pos+1)])
        elif self.history_pos == 0:
            self.history_pos = -1
            self.input_field.delete(0, tk.END)