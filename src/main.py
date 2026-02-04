import flet as flet
import src.assets.app_colors as app_colors


async def main(page: flet.Page):
    page.bgcolor = app_colors.GHOST_WHITE
    page.padding = 0  # Wichtig, damit das Bild bis zum Rand geht

    # 1. Das Hintergrundbild vorbereiten
    bg_image = flet.Image(
        src="assets/background_0.png",
        fit="cover",
        width=page.window.width,
        height=page.window.height,
    )
    #Bildgröße an Fenstergröße anpassen
    async def on_page_resize(e):
        bg_image.width = page.window.width
        bg_image.height = page.window.height
        page.update()
    page.on_resize = on_page_resize


    # 2. Die UI-Elemente in eine Column packen
    ui_layout = flet.Column(
        controls=[
            flet.Container( #Header
                content=flet.Text("Rezept Manager 9000", color=app_colors.GHOST_WHITE, size=20, weight="bold"),
                padding=20,
                bgcolor=app_colors.MAGENTA,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Container( #Header_main_menu
                content=flet.Text("Hauptmenü", size=20, weight="bold"),
                padding=20,
                width=300,
                bgcolor=app_colors.ELECTRIC_SKY_BLUE,
                alignment=flet.Alignment.CENTER,
                border_radius=10,
                margin=10
            ),
            flet.Row(
                controls=[ #menu_buttons
                    flet.Button("Alle Rezepte Anzeigen"),
                    flet.Button("Rezept hinzufügen"),
                    flet.Button("Rezept suchen"),
                    flet.Button("Rezepte Namen ändern"),
                    flet.Button("ID's anzeigen"),
                    flet.Button("Programm beenden")
                ],
                wrap=True,  # Falls die Buttons zu breit für den Bildschirm sind
                spacing=10
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


flet.run(main)