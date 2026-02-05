
import json

from controller import recipe_service

data = recipe_service.load_json_data()


def filter_by_name(data, search_input):
    search_input = search_input.lower().strip()

    if not search_input:
        return data
                    #name in name info in info
    found_recipe = {name: info for name, info in data.items()
                    if search_input in name.lower()}

    return found_recipe



def filter_by_ingredient(data, search_input):
    search_input = search_input.lower().strip()

    if not search_input:
        return data

    found_recipe = {name : info for name , info in data.items()
                    if search_input in info["ingredients"]}
    return found_recipe

def recipe_search_by_ingredient(data):
    search_ingredient = input("Bitte Zutat eingeben: ").lower()
    found = False

    for id, info in data.items():
        for ingredient in info["ingredients"]:
            if search_ingredient in ingredient.lower():
                found = True
                print(f"Zutat '{ingredient}' im Rezept '{id}' gefunden!")
                show = input("Rezept anzeigen? (y/n): ")
                if show.lower() == "y":
                    print(f"\nRezept: {id}")
                    print("Zutaten:")
                    for ing in info["ingredients"]:
                        print(f" - {ing}")
                    print("Anleitung:")
                    for instr in info["instructions"]:
                        print(f" - {instr}")
                break

    if not found:
        print("Keine Rezepte mit dieser Zutat gefunden.")


def delete_recipe(data):
    search_name = input("Bitte Rezeptname eingbene: ").lower()
    found = False
    recipe_found = None
    for id, info in data.items():
         if search_name.lower() == id.lower():
            recipe_found = id
            break

    print(f"Rezept {recipe_found} gefunden!")
    delete_yn = input("Wollen Sie das Rezept löschen?")
    if delete_yn.lower() == "y":
        del data[recipe_found]
    with open("recipe_json.json", 'w', encoding='utf-8') as db:
        json.dump(data, db, ensure_ascii=False, indent=4)
        print(f"Rezept {recipe_found} gelöscht!")

    return data

