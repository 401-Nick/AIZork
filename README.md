# AIZork - AI-Powered Text Adventure Game

## Description
A modern text adventure game with dynamic AI-generated narratives using OpenAI's API and Tkinter GUI

## Features
- 🧠 GPT-powered story generation
- 🖥️ Tkinter-based graphical interface
- ⚙️ Complex state tracking (inventory, health, skills, relationships)
- 🕹️ Interactive fiction mechanics
- ⏳ Real-time game world simulation

## Installation
```bash
git clone https://github.com/yourusername/AIZork.git
cd AIZork
python -m venv venv

venv\Scripts\activate 
or 
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration
1. Create `.env` file with your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Usage
```bash
python main.py
```

## Project Structure
```
AIZork/
├── main.py             - Main entry point
├── game_engine.py      - Core game loop and state management
├── game_gui.py         - Tkinter GUI implementation
├── game_state.py       - Game state management
├── narrative_model.py  - AI story generator
├── monitor_models.py   - State update handlers
├── state_update_model.py - State update model
├── requirements.txt    - Dependencies
├── world_generator.py  - World generator (WIP)
└── .env                - Configuration
```

## Dependencies
- OpenAI Python client
- python-dotenv
- Tkinter

# Custom Monitor Implementation (ex stamina)
1. In main.py, add instructions and any rules to SYSTEM_PROMPT_UPDATES 
```python
SYSTEM_PROMPT_UPDATES = """
"inventory": List[str] - List of items in the inventory.
If the user mentions an item that is not in the inventory, they will not be able to use it. If the inventory is overfilled, drain stamina as a result.

"health": int - Current health level.
If the user is out of health, they will be unable to perform some actions. The user will die in the game.

"stamina": int (Max: 100) - Current stamina level. 
If the user is out of stamina, they will be unable to perform some actions.
...

"""
```
2. Add object to initial state
```python
INITIAL_STATE{ 
    "health": 100,
    "stamina": 100,
    ... 
}
```
3. Add the key to MONITORS
```python
MONITORS = [ 
    GenericMonitor("health", update_health),
    GenericMonitor("stamina", update_stamina),
    ...  
]
```
4. Add update function to monitor_models.py
```python
# This function will be called if "stamina" is within the update_data
# as set by:
# GenericMonitor("stamina", update_stamina) in main.py
# syntax: GenericMonitor(key, update_func)
def update_stamina(update_data: int, game_state: GameState) -> None:
    """Update the stamina in the game state with bounds checking."""
    
    # Initialize stamina if not present
    if "stamina" not in game_state.state:
        game_state.state["stamina"] = 100

    # Validate stamina bounds (0 - 100)
    game_state.state["stamina"] = max(0, min(100, update_data))

    # Log the update
    print(f"Updated stamina: {game_state.state['stamina']}")
```
