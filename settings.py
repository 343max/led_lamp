import json
import os
from typing import Optional, Tuple

state_json = os.path.dirname(os.path.abspath(__file__)) + '/state.json'

def store_scene(scene_name: str, on: bool):
    with open(state_json, 'w') as json_file:
      json.dump({'scene_name': scene_name, 'on': on}, json_file)

def load_scene() -> Tuple[Optional[str], bool]:
  try:
    with open(state_json) as json_file:
      state = json.load(json_file)
      return (state['scene_name'], state['on'] if 'on' in state else False)
  except FileNotFoundError:
    return (None, False)
  except json.decoder.JSONDecodeError:
    return (None, False)
