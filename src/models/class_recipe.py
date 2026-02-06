from app.services.data_validation import *
import uuid

class Recipe:
    def __init__(self, name=None, ingredients=None, instructions=None, id=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.__id = id or uuid.uuid4() #uniqe id for each recipe for db integration

    def get_id(self):
        return self.__id

    def show_ingredients(self):
        print(f"\nZutaten für {self.name}:")
        for ingredient in self.ingredients:
            print(f"- {ingredient}")

    def show_instructions(self):
        print(f"\nAnleitung für {self.name}:")
        for instruction in self.instructions:
            print(f"- {instruction}")

    def fill_recipe(self):


        self.name = data_validation_name()

        self.ingredients = data_validation_ingredients()
        self.instructions = data_validation_instructions()


#code edit for json export
    def do_dict(self):
        return {
            "name": self.name,
            "ingredients":  self.ingredients,
            "instructions": self.instructions,
            "id": str(self.__id)}




recipe_list_container.controls.append(
                    flet.Container(
                        content=flet.Text(f"{icon_recipe} {recipe_info['name']}",
                                          color=app_colors.DARK_COFFE,
                                          weight=flet.FontWeight.BOLD),
                        padding=10,
                        bgcolor=app_colors.LIGHT_LATTE,
                        border_radius=5,
                        on_click=open_details,
                        ink=True
                    )
                )
