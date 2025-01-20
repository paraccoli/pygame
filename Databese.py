import json
import os

class Database:
    def __init__(self, db_path="game_data.json"):
        self.db_path = db_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_data(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_data(self, key):
        return self.data.get(key, None)

    def set_data(self, key, value):
        self.data[key] = value
        self.save_data()