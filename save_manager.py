# FILE: save_manager.py
import json

def load_save_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_game(file_path, save_data):
    with open(file_path, 'w') as file:
        json.dump(save_data, file, indent=4)

def get_selected_save_slot():
    with open('save/selected_save_slot.json', 'r') as file:
        return json.load(file)["selected_slot"]