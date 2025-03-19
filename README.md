# AIZork: AI-Powered Text Adventure Game
Created from scratch with Grok 3
(This is a buggy work in progress but interesting concept so far)

A modern text adventure game engine powered by OpenAI's language models. This application combines classic text adventure gameplay with AI capabilities to create dynamic, responsive narratives.

## Overview

AIZork is a text-based adventure game that uses OpenAI's GPT models to:
- Generate narrative responses to player actions
- Extract game state updates from the narrative
- Maintain game state (inventory, location, etc.)

The game runs with a simple GUI interface built with Tkinter for easy interaction.

## Requirements

- Python 3.8+
- OpenAI API key
- Required packages:
  - openai
  - python-dotenv
  - tkinter (usually comes with Python)

## Setup and Installation

1. Clone the repository or download the code files

2. Install the required Python packages:
   ```
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the game:
   ```
   python main.py
   ```

## Project Structure

- **main.py**: Entry point of the application, contains system prompts and initial state
- **game_engine.py**: Core engine that coordinates between models and GUI
- **game_state.py**: Manages the state of the game (inventory, location, etc.)
- **game_gui.py**: Tkinter GUI implementation for the game
- **narrative_model.py**: Interfaces with OpenAI to generate narrative text
- **state_update_model.py**: Analyzes narrative to extract state updates
- **monitor_models.py**: Models that process specific types of state updates

## How to Play

1. Start the game by running `main.py`
2. Read the narrative text in the output area
3. Type your actions in the input field and press Enter
4. The AI will generate a narrative response based on your action
5. The game state (inventory, location) will update automatically
6. Continue exploring and interacting with the game world

## Modifying the Game

### Changing Initial Game State

Edit the `initial_state` dictionary in `main.py` to change:
- Starting inventory items
- Starting location
- Available map locations

```python
initial_state = {
    "inventory": ["sword", "map", "potion"],  # Change starting items
    "location": "castle",  # Change starting location
    "map": {"castle": ["forest", "town"]}  # Define available paths
}
```

### Customizing the Narrative Style

Modify the `SYSTEM_PROMPT_NARRATIVE` in `main.py` to change how the AI generates narrative responses. For example, to create a sci-fi setting:

```python
SYSTEM_PROMPT_NARRATIVE = """
You are the AI of a futuristic space station. Generate responses with a technological, sci-fi tone.
Describe alien environments and advanced technology in your responses.
Keep it immersive and concise.
"""
```

### Adding New State Monitors

1. Create a new monitor class in `monitor_models.py` by extending the `MonitorModel` base class
2. Implement the `update_state` method to handle specific state updates
3. Add your new monitor to the `monitors` list in `main.py`

Example of adding a health monitor:

```python
# In monitor_models.py
class HealthMonitor(MonitorModel):
    def update_state(self, updates: Dict, game_state: 'GameState') -> None:
        health_change = updates.get("health_change", 0)
        if health_change:
            if "health" not in game_state.state:
                game_state.state["health"] = 100
            game_state.state["health"] += health_change
            game_state.state["health"] = max(0, min(100, game_state.state["health"]))
            logger.info(f"Updated health to: {game_state.state['health']}")

# In main.py
monitors = [InventoryMonitor(), MapMonitor(), HealthMonitor()]
```

### Changing the State Update Logic

Modify the `SYSTEM_PROMPT_UPDATES` in `main.py` to change how the AI extracts state updates from narrative text. Add new update types or change existing ones.

Example of adding health updates:

```python
SYSTEM_PROMPT_UPDATES = """
You are an assistant that analyzes player input and narrative text to extract state updates.
Possible updates include:
- "inventory": {"add": [...], "remove": [...]}
- "location": "new_location"
- "health_change": integer (positive for healing, negative for damage)

Example: If player drinks a healing potion and the narrative mentions recovery, output:
{
  "inventory": {"add": [], "remove": ["healing potion"]},
  "health_change": 20
}
"""
```

### Enhancing the GUI

Modify `game_gui.py` to add new UI elements or improve the existing interface:
- Add buttons for common actions
- Include images or icons
- Add more text formatting options
- Create a more sophisticated state display

## Advanced Customization

### Using Different Models

Change the `OPENAI_MODEL` constant in both `narrative_model.py` and `state_update_model.py` to use different OpenAI models:

```python
OPENAI_MODEL = "gpt-4"  # For higher quality responses
```

### Adding Persistent Saving

Implement save/load functionality by adding methods to serialize and deserialize the `GameState`:

```python
# Save game state to file
def save_game(filename, game_state):
    with open(filename, 'w') as f:
        json.dump(game_state.state, f)

# Load game state from file
def load_game(filename):
    with open(filename, 'r') as f:
        state = json.load(f)
    return GameState(state)
```

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file contains a valid OpenAI API key
- **JSON Parsing Errors**: Check the system prompts to ensure they generate valid JSON
- **Rate Limiting**: If you encounter API rate limits, add a delay between API calls

## License

This project is provided as-is for educational and entertainment purposes.

## Acknowledgements

This game engine uses OpenAI's GPT models for generating text and analyzing user input.
