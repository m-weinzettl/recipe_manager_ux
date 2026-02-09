import flet as flet
import src.assets.app_colors as app_colors
from src.models.class_recipe import Recipe

async def show_secret_id(page: flet.Page, recipe_data: dict):

    recipe_id = recipe_data.get("id") or "Keine ID verfügbar"

    async def close_dialog(e):
        secret_id_dialog.open = False
        page.update()

    secret_id_dialog = flet.AlertDialog(
        title=flet.Text("Geheime ID", color=app_colors.DARK_COFFE, bgcolor=app_colors.LIGHT_CREAM_COFFE),
        content=flet.Text(
            value=f"Die geheime ID für das Rezept '{recipe_data['name']}' ist:\n{recipe_id}",
            color=app_colors.DARK_LATTE
        ),
        actions=[
            flet.ElevatedButton("OK", on_click=close_dialog)
        ],
        bgcolor=app_colors.DARK_COFFE,
    )

    page.overlay.append(secret_id_dialog)
    secret_id_dialog.open = True
    page.update()