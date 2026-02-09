import flet as flet
from src.models.class_recipe import Recipe
import src.assets.app_colors as app_colors
import src.controller.recipe_service as recipe_service


async def open_add_recipe_dialog(page: flet.Page, on_recipe_added_callback=None):

    name_field = flet.TextField(
        label="Rezeptname",
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE
    )

    ingredients_field = flet.TextField(
        label="Zutaten (mit Komma trennen)",
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE,
        multiline=True
    )

    instructions_field = flet.TextField(
        label="Anleitung (mit Komma trennen)",
        color=app_colors.DARK_COFFE,
        bgcolor=app_colors.LIGHT_LATTE,
        focused_border_color=app_colors.DARK_LATTE,
        multiline=True
    )

    async def save_new_recipe(e):
        name_field.error_text = None

        if not name_field.value or len(name_field.value) > 200:
            name_field.error_text = "Rezeptname muss zwischen 1 und 200 Zeichen lang sein."
            page.update()
            return

# new class instance
        new_recipe = Recipe(
            name=name_field.value,
            ingredients=[item.strip() for item in ingredients_field.value.split(',') if item.strip()],
            instructions=[item.strip() for item in instructions_field.value.split(',') if item.strip()]
        )


        recipe_service.add_recipe_to_db(new_recipe)

        add_dialog.open = False
        page.update()

        if on_recipe_added_callback:
            await on_recipe_added_callback(None)

    add_dialog = flet.AlertDialog(
        bgcolor=app_colors.DARK_LATTE,
        title=flet.Text("Neues Rezept hinzufügen", color=app_colors.LIGHT_CREAM_COFFE),
        content=flet.Column([
            name_field,
            ingredients_field,
            instructions_field
        ], tight=True),
        actions=[
            flet.Button(
                "Speichern",
                on_click=save_new_recipe,
                color=app_colors.DARK_COFFE,
                bgcolor=app_colors.LIGHT_CREAM_COFFE
            ),
            flet.Button(
                "Abbrechen",
                on_click=lambda _: setattr(add_dialog, "open", False) or page.update(),
                color=app_colors.DARK_COFFE,
                bgcolor=app_colors.LIGHT_CREAM_COFFE
            )
        ]
    )

    page.overlay.append(add_dialog)
    add_dialog.open = True
    page.update()