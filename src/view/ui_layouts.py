import flet as flet
import src.assets.app_colors as app_colors


def delete_dialog(recipe_name, on_confirm, on_cancel):
    return flet.AlertDialog(
        bgcolor=app_colors.DARK_LATTE,
        title=flet.Text(value=f"Rezept löschen", color=app_colors.LIGHT_CREAM_COFFE),
        content=flet.Text(value=f"Sind Sie sicher, dass Sie das Rezept '{recipe_name}' löschen möchten?",
                          color=app_colors.LIGHT_CREAM_COFFE),

        actions=[flet.Button("Ja, löschen", color=app_colors.LIGHT_CREAM_COFFE,
                             bgcolor=app_colors.DARK_COFFE,
                             on_click=on_confirm),
                 flet.Button("Abbrechen",
                             color=app_colors.LIGHT_CREAM_COFFE,
                             bgcolor=app_colors.DARK_COFFE,
                             on_click=on_cancel)],
    )


async def layouts(page: flet.Page, recipe_list_container: flet.Container, actions: dict):


    ui_layout = flet.Column(
            controls=[
                flet.Container(
                    content=flet.Text("Rezept Manager 9000",
                                      color=app_colors.DARK_COFFE, size=20, weight=flet.FontWeight.BOLD),
                    padding=20, bgcolor=app_colors.LIGHT_CREAM_COFFE, alignment=flet.Alignment.CENTER, border_radius=10,
                    margin=10
                ),
                flet.Container(
                    content=flet.Text("Hauptmenü", size=20, weight=flet.FontWeight.BOLD, color=app_colors.DARK_COFFE),
                    padding=20, width=300, bgcolor=app_colors.LIGHT_CREAM_COFFE, alignment=flet.Alignment.CENTER,
                    border_radius=10, margin=10
                ),
                flet.Row(
                    controls=[
                        flet.Button("Alle Rezepte Anzeigen",
                                    color=app_colors.LIGHT_CREAM_COFFE,
                                    bgcolor=app_colors.LIGHT_LATTE,
                                    on_click =actions["show_all_button"]),
                        flet.Button("Rezept hinzufügen",
                                    color=app_colors.LIGHT_CREAM_COFFE,
                                    bgcolor=app_colors.LIGHT_LATTE,
                                    on_click=actions["add_button"]
                                                        ),
                        flet.Button("Such Menü", color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE,
                                    on_click=actions["filter_button"]),
                        flet.Button("Rezepte anpassen", color=app_colors.LIGHT_CREAM_COFFE,
                                    bgcolor=app_colors.LIGHT_LATTE,
                                    on_click=actions["edit_button"]),
                        flet.Button("Rezept löschen",
                                    color=app_colors.LIGHT_CREAM_COFFE,
                                    bgcolor=app_colors.LIGHT_LATTE,
                                    on_click =actions["delete_button"])



                    ],
                    wrap=True, spacing=10
                ),
                flet.Container(
                    content=recipe_list_container,
                    padding=20,
                    bgcolor=flet.Colors.with_opacity(0.8, app_colors.LIGHT_CREAM_COFFE),
                    border_radius=10,
                    margin=10,
                    expand=True
                ),
                flet.Button("Programm schließen", color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.DARK_COFFE,
                            on_click=actions["close_button"])
            ]
        )

    return ui_layout