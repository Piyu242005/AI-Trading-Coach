import json
import os

def load_dataset():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "nevup_seed_dataset.json")
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

dataset = load_dataset()