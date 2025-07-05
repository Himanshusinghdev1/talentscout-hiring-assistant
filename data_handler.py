# data_handler.py
import json
import os

DATA_FILE = "candidates.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_candidate(candidate_info):
    data = load_data()
    data.append(candidate_info)
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
