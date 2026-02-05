import flet as flet
import src.assets.app_colors as app_colors
import src.controller.recipe_service as recipe_service
import src.controller.search_recipe as search_recipe

async def gui(page: flet.Page):
    icon_recipe = "🍴"
    page.color = app_colors.LIGHT_CREAM_COFFE
    page.padding = 0  # Wichtig, damit das Bild bis zum Rand geht
    recipe_list_container = flet.Column(scroll=flet.ScrollMode.AUTO, height=300)


    bg_image = flet.Image(
        src="assets/background_restaurant_0.png",
        fit=flet.BoxFit.COVER,

        width=page.window.width,
        height=page.window.height,
        margin=10
    )

    async def on_page_resize(e):
        bg_image.width = page.window.width
        bg_image.height = page.window.height
        page.update()
    page.on_resize = on_page_resize

    async def show_all_recipes(e):
        data = recipe_service.load_json_data()
        recipe_list_container.controls.clear()

        if not data:
            recipe_list_container.controls.append(flet.Text("Kein Rezept gefunden."))
        else:
            for recipe_id, recipe_info in data.items():

                async def open_details(e, current_info=recipe_info):
                    ingredients = "\n".join(f"- {item}" for item in current_info['ingredients'])
                    instructions = "\n".join(f"- {step}" for step in current_info['instructions'])

                    async def close_dialog(e):
                        details_dialog.open = False
                        page.update()

                    details_dialog = flet.AlertDialog(
                        bgcolor=app_colors.DARK_LATTE,
                        title=flet.Text(value=f"Rezept: {current_info['name']}", color=app_colors.LIGHT_CREAM_COFFE),
                        content=flet.Column([
                            flet.Text(value="Zutaten:", weight=flet.FontWeight.BOLD, color=app_colors.LIGHT_CREAM_COFFE),
                            flet.Text(value=ingredients),
                            flet.Text(value="Anleitung:", weight=flet.FontWeight.BOLD, color=app_colors.LIGHT_CREAM_COFFE),
                            flet.Text(value=instructions)
                        ], tight=True, scroll=flet.ScrollMode.AUTO),
                       actions=[flet.Button("Schließen",
                                            color=app_colors.DARK_COFFE,
                                            bgcolor=app_colors.LIGHT_CREAM_COFFE,
                                            on_click=close_dialog)],
                    )
#call overlay for recipe details
                    page.overlay.append(details_dialog)
                    details_dialog.open = True
                    page.update()

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

        page.update()


    async def close_app(e):
        await page.window.close()

    # ui elements layout
    ui_layout = flet.Column(
        controls=[
            flet.Container( #Header
                content=flet.Text("Rezept Manager 9000",
                color=app_colors.DARK_COFFE, size=20, weight=flet.FontWeight.BOLD),
                padding=20,
                bgcolor=app_colors.LIGHT_CREAM_COFFE,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Container( #Header_main_menu
                content=flet.Text("Hauptmenü", size=20, weight=flet.FontWeight.BOLD, color=app_colors.DARK_COFFE),
                padding=20,
                width=300,
                bgcolor=app_colors.LIGHT_CREAM_COFFE,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Row(
                controls=[ #menu_buttons
                    flet.Button("Alle Rezepte Anzeigen",
                                color=app_colors.LIGHT_CREAM_COFFE,
                                bgcolor=app_colors.LIGHT_LATTE,
                                on_click=show_all_recipes),
                    flet.Button("Rezept hinzufügen",color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE),
                    flet.Button("Rezept suchen",color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE),
                    flet.Button("Rezepte Namen ändern",color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE),
                    flet.Button("ID's anzeigen",color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE),
                    flet.Button("Programm beenden",color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE)
                ],
                wrap=True, # smaller buttons on small screens
                spacing=10
            ),

            flet.Container(
                content=recipe_list_container,
                padding=20,
                bgcolor=flet.Colors.with_opacity(0.8, app_colors.LIGHT_CREAM_COFFE),
                border_radius=10,
                margin=10,
                expand=True
            ),

            flet.Button("Programm schließen",
                        color=app_colors.LIGHT_CREAM_COFFE,
                        bgcolor=app_colors.DARK_COFFE,
                        on_click=close_app

            )


        ]
    )


    page.add(
        flet.Stack(
            controls=[
                bg_image,
                flet.Container(content=ui_layout, padding=10)
            ],
            expand=True
        )
    )
