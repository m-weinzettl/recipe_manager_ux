
import sqlite3
import os

def init_db():

    current_file_path = os.path.abspath(__file__)
    api_dir = os.path.dirname(current_file_path)
    project_root = os.path.dirname(api_dir)
    db_path = os.path.join(project_root, "recipe_manager.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS recipes")


    cursor.execute("""CREATE TABLE recipes (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        ingredients TEXT NOT NULL,
                        instructions TEXT NOT NULL)""")

    connection.commit()
    connection.close()
    print(f"Datenbank erfolgreich erstellt unter: {db_path}")

if __name__ == "__main__":
    init_db()

# ^^^^mit hilfe von ki, da mein code nicht funktioniert hat

    ###
#import sqlite3

#def init_db():
  #  connection = sqlite3.connect("recipe_manager.db")
  #  cursor = connection.cursor()

    # Das Komma nach 'instructions TEXT NOT NULL' wurde entfernt
 #   cursor.execute("""#CREATE TABLE IF NOT EXISTS recipes (
                     # id TEXT PRIMARY KEY,
                     # name TEXT NOT NULL,
                     # ingredients TEXT NOT NULL,
                     # instructions TEXT NOT NULL)""")

  #  connection.commit()
   # connection.close()
  #  """