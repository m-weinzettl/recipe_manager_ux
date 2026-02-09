
import flet as flet
import src.assets.app_colors as app_colors
import src.controller.recipe_service as recipe_service
import src.controller.search_recipe as search_recipe
import view.new_recipe_dialog as data_validation
import src.view.show_secret_id as secret_id


async def gui(page: flet.Page):
    icon_recipe = "🍴"
    page.color = app_colors.LIGHT_CREAM_COFFE
    page.padding = 0  # Wichtig, damit das Bild bis zum Rand geht
    recipe_list_container = flet.Column(scroll=flet.ScrollMode.AUTO, height=300)
    filter_menu = flet.Column(scroll=flet.ScrollMode.AUTO, height=100)

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

    def get_info():
        data = recipe_service.load_json_data()
        for id_info, recipe_info in data.items():
            return recipe_info
        return None

    async def open_details(e, current_info=None):
        if current_info is None:
            current_info = get_info()

        if not current_info:
            return

        current_active_dialog["data"] = current_info

        ingredients = "\n".join(f"- {item}" for item in current_info['ingredients'])
        instructions = "\n".join(f"- {step}" for step in current_info['instructions'])

        async def close_dialog(e):
            details_dialog.open = False
            page.update()

        details_dialog = flet.AlertDialog(
            bgcolor=app_colors.DARK_LATTE,
            title=flet.Text(value=f"Rezept: {current_info['name']}", color=app_colors.LIGHT_CREAM_COFFE),
            content=flet.Column([
                flet.Text(value="Zutaten:", weight=flet.FontWeight.BOLD,
                          color=app_colors.LIGHT_CREAM_COFFE),
                flet.Text(value=ingredients, color=app_colors.LIGHT_CREAM_COFFE),
                flet.Text(value="Anleitung:", weight=flet.FontWeight.BOLD,
                          color=app_colors.LIGHT_CREAM_COFFE),
                flet.Text(value=instructions, color=app_colors.LIGHT_CREAM_COFFE)
            ], tight=True, scroll=flet.ScrollMode.AUTO),
            actions=[flet.Button("Schließen",
                                 color=app_colors.DARK_COFFE,
                                 bgcolor=app_colors.LIGHT_CREAM_COFFE,
                                 on_click=close_dialog)],
        )

        page.overlay.append(details_dialog)
        details_dialog.open = True
        page.update()

    async def show_all_recipes(e, mode="view"):
        data = recipe_service.load_json_data()
        recipe_list_container.controls.clear()

        if not data:
            recipe_list_container.controls.append(
                flet.Text("Kein Rezept gefunden.", color=app_colors.DARK_COFFE)
            )
        else:
            for rid, recipe_info in data.items():
                if mode == "edit":
                    import src.view.update_recipe as update_window
                    click_handler = lambda e, info=recipe_info: page.run_task(
                        update_window.update_recipe, page, info, show_all_recipes
                    )
                    button_text = f"✎ {recipe_info['name']}"
                elif mode == "delete":
                    click_handler = lambda e, name = recipe_info['name']: page.run_task(confirm_delete, name
                    )
                    button_text = f"🗑️ {recipe_info['name']}"
                else:
                    click_handler = lambda e, info=recipe_info: page.run_task(
                        open_details, e, info
                    )
                    button_text = f"{icon_recipe} {recipe_info['name']}"

                recipe_list_container.controls.append(
                    flet.Button(
                        button_text,
                        on_click=click_handler,
                        color=app_colors.LIGHT_CREAM_COFFE,
                        bgcolor=app_colors.LIGHT_LATTE,
                        width=400
                    )
                )
        page.update()

    async def confirm_delete(recipe_name):
        def do_delete(e):
            recipe_service.delete_recipe_from_db(recipe_name)
            delete_dialog.open = False
            page.update()
            page.run_task(show_all_recipes, e, mode="delete")

        delete_dialog = flet.AlertDialog(
            bgcolor=app_colors.DARK_LATTE,
            title=flet.Text(value=f"Rezept löschen", color=app_colors.LIGHT_CREAM_COFFE),
            content=flet.Text(value=f"Sind Sie sicher, dass Sie das Rezept '{recipe_name}' löschen möchten?",
                              color=app_colors.LIGHT_CREAM_COFFE),
            actions=[flet.Button("Ja, löschen", color=app_colors.DARK_COFFE, on_click=do_delete),
                        flet.Button("Abbrechen",
                                    color=app_colors.DARK_COFFE,
                                    on_click=lambda e: setattr(delete_dialog,
                                                               "open", False) or page.update())],
        )

        page.overlay.append(delete_dialog)
        delete_dialog.open = True
        page.update()

    async def filter_recipes(e):
        recipe_list_container.controls.clear()

        async def update_recipe_list(results):
            recipe_list_container.controls.clear()
            recipe_list_container.controls.append(
                flet.Button("<- Zurück zum Such-Menü",
                            on_click=filter_recipes,
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE)
            )

            if not results:
                recipe_list_container.controls.append(flet.Text("Kein Rezept gefunden.", color=app_colors.DARK_COFFE))
            else:
                for rid, info in results.items():
                    recipe_list_container.controls.append(
                        flet.Button(f"{icon_recipe} {info['name']}",
                                    on_click=lambda e, i=info: page.run_task(open_details, e, i))
                    )
            page.update()

        async def show_search_input(mode):
            recipe_list_container.controls.clear()

            search_input = flet.TextField(
                label=f"Suche nach {mode}...",
                color=app_colors.DARK_COFFE,
                bgcolor=app_colors.LIGHT_LATTE,
                focused_border_color=app_colors.DARK_LATTE
            )



            async def trigger_search(e):
                data = recipe_service.load_json_data()
                if mode == "Name":
                    res = search_recipe.filter_by_name(data, search_input.value)
                else:
                    res = search_recipe.filter_by_ingredient(data, search_input.value)
                await update_recipe_list(res)

            recipe_list_container.controls.extend([
                flet.Text(f"Filter-Modus: {mode}",
                          weight=flet.FontWeight.BOLD,
                          color=app_colors.DARK_COFFE),
                search_input,
                flet.Button("Jetzt Suchen", on_click=trigger_search,
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE),
                flet.Button("Abbrechen",
                            on_click=filter_recipes,
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE)
            ])
            page.update()

        filter_button_row = flet.Row(
            controls=[
                flet.Button("Filtern nach Name",
                            on_click=lambda _: page.run_task(show_search_input, "Name"),
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE),
                flet.Button("Filtern nach Zutat",
                            on_click=lambda _: page.run_task(show_search_input, "Zutat"),
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE),
                flet.Button("Schließen",
                            on_click=lambda _: recipe_list_container.controls.clear() or page.update(),
                            color=app_colors.LIGHT_CREAM_COFFE,
                            bgcolor=app_colors.LIGHT_LATTE)
            ],
            wrap=True
        )
        recipe_list_container.controls.append(filter_button_row)
        page.update()

    current_active_dialog = {"data": None}

    async def sec_id_window_key(e: flet.KeyboardEvent):
        if e.key == "F3" and current_active_dialog.get("data"):
            await secret_id.show_secret_id(page, current_active_dialog["data"])
    page.on_keyboard_event = sec_id_window_key

    async def close_app(e):
        await page.window.close()

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
                                on_click = lambda e: page.run_task(show_all_recipes, e)),
                    flet.Button("Rezept hinzufügen",
                                color=app_colors.LIGHT_CREAM_COFFE,
                                bgcolor=app_colors.LIGHT_LATTE,
                                on_click=lambda _: page.run_task(data_validation.open_add_recipe_dialog,
                                                                 page,
                                                                 show_all_recipes)
                                                    ),
                    flet.Button("Such Menü", color=app_colors.LIGHT_CREAM_COFFE, bgcolor=app_colors.LIGHT_LATTE,
                                on_click=filter_recipes),
                    flet.Button("Rezepte anpassen", color=app_colors.LIGHT_CREAM_COFFE,
                                bgcolor=app_colors.LIGHT_LATTE,
                                on_click=lambda e: page.run_task(show_all_recipes, e, mode="edit")),
                    flet.Button("Rezept löschen",
                                color=app_colors.LIGHT_CREAM_COFFE,
                                bgcolor=app_colors.LIGHT_LATTE,
                                on_click = lambda e: page.run_task(show_all_recipes, e, mode="delete"))



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
                        on_click=close_app)
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