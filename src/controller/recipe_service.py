import json
from api.route import get_db_connection

def add_recipe_to_db(new_recipe):
    recipe_data_new = new_recipe.do_dict()

    query = """INSERT INTO  recipes(id, name, ingredients, instructions) VALUES (?, ?, ?, ?)
            ON CONFLICT (id) DO UPDATE SET
            name=excluded.name,
            ingredients=excluded.ingredients,
            instructions=excluded.instructions;"""

    with get_db_connection() as connection:
        connection.execute(query,
                           (recipe_data_new["id"],
                            recipe_data_new["name"],
                            json.dumps(recipe_data_new["ingredients"]),
                            json.dumps(recipe_data_new["instructions"])))


        connection.commit()



def load_data_from_db():
    query = """SELECT * FROM recipes;"""
    with get_db_connection() as connection:
        rows = connection.execute(query).fetchall()


        recipe_dict = {}
        for row in rows:
            recipe_dict[row["name"]] = {
                "id": row["id"],
                "name": row["name"],
                "ingredients": json.loads(row["ingredients"]),
                "instructions": json.loads(row["instructions"])
            }
        return recipe_dict


def delete_recipe_from_db(recipe_name):
    query = """DELETE FROM recipes WHERE name = ?"""

    with get_db_connection() as connection:
        connection.execute(query, (recipe_name,))
        connection.commit()