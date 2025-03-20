''' take in GAME_STATE.location
  "Private Office": {"coordinates": [1, 1], "description": "Private Office", "objects": ["Pen", "Paper"]},
  
THEN

  use an LLM to generate a whole world around the player
 "Office Building": {
 "coordinates": [0, 0], 
 "description": "Office Building", 
 "rooms": ["Private Office": {
            "coordinates": [1, 1], 
            "description": "Private Office", 
            "objects": ["General Office Items"]}, 
        "Conference Room": {
            "coordinates": [1, 0], 
            "description": "Conference Room", 
            "objects": ["General Office Items"]}, 
        "Lobby": {
            "coordinates": [0, 1], 
        "description": "Lobby", 
        "objects": ["General Items found in lobby"],
        "Canteen": {
            "coordinates": [0, 2], 
        "description": "Canteen", 
        "objects": ["General Food Items"]
    ]
}
'''


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate a world around the player."}
    ]
)

print(response.choices[0].message.content)