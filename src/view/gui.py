import flet as flet
import src.assets.app_colors as app_colors
import src.controller.recipe_service as recipe_service

async def gui(page: flet.Page):
    page.color = app_colors.GHOST_WHITE
    page.padding = 0  # Wichtig, damit das Bild bis zum Rand geht
    recipe_list_container = flet.Column(scroll=flet.ScrollMode.AUTO, height=300)

    # 1. Das Hintergrundbild vorbereiten
    bg_image = flet.Image(
        src="assets/background_0.png",
        fit=flet.BoxFit.COVER,
        width=page.window.width,
        height=page.window.height,
    )
    #Bildgröße an Fenstergröße anpassen
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

                    def close_dialog(e):
                        details_dialog.open = False
                        page.update()

                    details_dialog = flet.AlertDialog(
                        title=flet.Text(value=f"Rezept: {current_info['name']}"),
                        content=flet.Column([
                            flet.Text(value="Zutaten:", weight=flet.FontWeight.BOLD),
                            flet.Text(value=ingredients),
                            flet.Text(value="Anleitung:", weight=flet.FontWeight.BOLD),
                            flet.Text(value=instructions)
                        ], tight=True,
                            scroll=flet.ScrollMode.AUTO,
                        ),
                        actions=[flet.TextButton("Schließen", on_click=close_dialog)],
                    )


                    # Set the dialog and open it
                    page.dialog = details_dialog
                    details_dialog.open = True
                    page.update()

                recipe_list_container.controls.append(flet.Container(
                                                      content=flet.Text(f"🍴 {recipe_info['name']}", color="white"),
                                                        padding=10,
                                                        bgcolor=app_colors.MAGENTA,
                                                        border_radius=5, on_click=open_details,
                                                        ink=True))
        page.update()


    # 2. Die UI-Elemente in eine Column packen
    ui_layout = flet.Column(
        controls=[
            flet.Container( #Header
                content=flet.Text("Rezept Manager 9000", color=app_colors.GHOST_WHITE, size=20, weight=flet.FontWeight.BOLD),
                padding=20,
                bgcolor=app_colors.MAGENTA,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Container( #Header_main_menu
                content=flet.Text("Hauptmenü", size=20, weight=flet.FontWeight.BOLD),
                padding=20,
                width=300,
                bgcolor=app_colors.ELECTRIC_SKY_BLUE,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Row(
                controls=[ #menu_buttons
                    flet.Button("Alle Rezepte Anzeigen",
                                color=app_colors.GHOST_WHITE,
                                bgcolor=app_colors.MAGENTA,
                                on_click=show_all_recipes),
                    flet.Button("Rezept hinzufügen",color=app_colors.GHOST_WHITE, bgcolor=app_colors.MAGENTA),
                    flet.Button("Rezept suchen",color=app_colors.GHOST_WHITE, bgcolor=app_colors.MAGENTA),
                    flet.Button("Rezepte Namen ändern",color=app_colors.GHOST_WHITE, bgcolor=app_colors.MAGENTA),
                    flet.Button("ID's anzeigen",color=app_colors.GHOST_WHITE, bgcolor=app_colors.MAGENTA),
                    flet.Button("Programm beenden",color=app_colors.GHOST_WHITE, bgcolor=app_colors.MAGENTA)
                ],
                wrap=True,  # Falls die Buttons zu breit für den Bildschirm sind
                spacing=10
            ),

            flet.Container(
                content=recipe_list_container,
                padding=20,
                bgcolor=flet.Colors.with_opacity(0.8, app_colors.GHOST_WHITE),
                border_radius=10,
                margin=10,
                expand=True
            )
        ]
    )

    # 3. Den Stack als einziges Haupt-Element hinzufügen
    # Das zuerst genannte Element (bg_image) liegt ganz unten.
    page.add(
        flet.Stack(
            controls=[
                bg_image,
                flet.Container(content=ui_layout, padding=10)
            ],
            expand=True
        )
    )


flet.run(gui)