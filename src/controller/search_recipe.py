
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
                    if any(search_input in ingredients.lower() for ingredients in info["ingredients"])}
    return found_recipe



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

