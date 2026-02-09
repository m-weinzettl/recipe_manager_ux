
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

#code edit for json export
    def do_dict(self):
        return {
            "name": self.name,
            "ingredients":  self.ingredients,
            "instructions": self.instructions,
            "id": str(self.__id)}



