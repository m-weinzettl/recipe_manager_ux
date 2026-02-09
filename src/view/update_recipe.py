import flet as flet
import src.controller.recipe_service as recipe_service
import src.models.class_recipe as Recipe
import src.assets.app_colors as app_colors

async def update_recipe(page: flet.Page, recipe_data: dict, on_success):

    ingredients_text = ", ".join(recipe_data.get("ingredients", []))
    instructions_text = ", ".join(recipe_data.get("instructions", []))

    name_field = flet.TextField(
        label="Rezeptname",
        value=recipe_data.get("name", ""),
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE
    )

    ingredients_field = flet.TextField(
        label="Zutaten (mit Komma trennen)",
        value=ingredients_text,
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE,
        multiline=True
    )

    instructions_field = flet.TextField(
        label="Anleitung (mit Komma trennen)",
        value=instructions_text,
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE,
        multiline=True
    )

    async def save_updated_recipe(e):
        name_field.error_text = None

        old_name = recipe_data.get("name", "")

        update_recipe = Recipe.Recipe(
            name = name_field.value,
            ingredients = [item.strip() for item in ingredients_field.value.split(',') if item.strip()],
            instructions = [item.strip() for item in instructions_field.value.split(',') if item.strip()]
        )

        recipe_service.delete_recipe_from_db(old_name)

        recipe_service.add_recipe_to_db(update_recipe)

        update_dialog.open = False
        page.update()


        if on_success:
            await on_success(None)

    update_dialog = flet.AlertDialog(
        bgcolor=app_colors.DARK_LATTE,
        title=flet.Text("Rezept aktualisieren",
                        color=app_colors.LIGHT_CREAM_COFFE),
        content=flet.Column([
            name_field,
            ingredients_field,
            instructions_field],
            spacing=10),
        actions=[
            flet.Button("Änderungen speichern",
                        on_click=save_updated_recipe,
                        color=app_colors.DARK_COFFE,
                        bgcolor=app_colors.LIGHT_CREAM_COFFE
            ),
            flet.Button("Abbrechen",
                        on_click=lambda e: setattr(update_dialog, "open", False) or page.update(),
                        color=app_colors.DARK_COFFE,
                        bgcolor=app_colors.LIGHT_CREAM_COFFE)
        ]
    )

    page.overlay.append(update_dialog)
    update_dialog.open = True
    page.update()