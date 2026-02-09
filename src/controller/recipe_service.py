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


def add_recipe_to_db(new_recipe):
    current_data = load_json_data()
    current_data[new_recipe.name] = new_recipe.do_dict()

    with open("recipe_json.json", 'w', encoding='utf-8') as db:
        json.dump(current_data, db, ensure_ascii=False, indent=4)

def delete_recipe_from_db(recipe_name):
    data = load_json_data()
    if recipe_name in data:
        del data[recipe_name]
        with open("recipe_json.json", 'w', encoding='utf-8') as db:
            json.dump(data, db, ensure_ascii=False, indent=4)