import json

def load_json_data():
    file_path = "recipe_json.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as from_json:
            recipe_data_new = json.load(from_json)
        return recipe_data_new
    except FileNotFoundError:
        print("Fehler: JSON-Datei nicht gefunden.")
        return {}