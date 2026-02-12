
from controller import recipe_service

data = recipe_service.load_data_from_db()


def filter_by_name(data_load, search_input):
    search_input = search_input.lower().strip()

    if not search_input:
        return data_load
                    #name in name info in info
    found_recipe = {name: info for name, info in data_load.items()
                    if search_input in name.lower()}

    return found_recipe



def filter_by_ingredient(data_load, search_input):
    search_input = search_input.lower().strip()

    if not search_input:
        return data_load

    found_recipe = {name : info for name , info in data_load.items()
                    if any(search_input in ingredients.lower() for ingredients in info["ingredients"])}
    return found_recipe




