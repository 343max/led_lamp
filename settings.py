import json
import os
from typing import Optional

state_json = os.path.dirname(os.path.abspath(__file__)) + '/state.json'

def store_scene(scene_name: Optional[str]):
    with open(state_json, 'w') as json_file:
      json.dump({'scene_name': scene_name}, json_file)

def load_scene() -> Optional[str]:
  try:
    with open(state_json) as json_file:
      state = json.load(json_file)
      return state['scene_name']
  except FileNotFoundError:
    return None
  except json.decoder.JSONDecodeError:
    return None
