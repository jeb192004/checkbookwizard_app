import flet as ft
from ui.theme import light_theme, dark_theme, green_theme
from data.utils import navigate_to
from ui.alert import create_loader
def settings_page(current_theme, page:ft.Page):
    loader = create_loader(page)
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: navigate_to(page, loader, "/bills")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    
    def update_page_theme(page: ft.Page, theme: dict):
        # Update relevant controls in the page with the new theme colors
        appbar.bgcolor = theme["top_appbar_colors"]["background"]
        appbar.leading.controls[1].src = theme["top_appbar_colors"]["icon"]
        appbar.parent.bgcolor = theme["background"]
        appbar.leading.controls[0].icon_color = theme["top_appbar_colors"]["icon_color"]
        theme_dropdown.color = theme["calc_theme"]["dropdown_text"]
        theme_dropdown.bgcolor = theme["calc_theme"]["dropdown_background"]
        theme_dropdown.border_color = theme["calc_theme"]["dropdown_border_color"]
        theme_dropdown.select_icon_enabled_color = theme["calc_theme"]["dropdown_icon_color"]
        theme_info.color = theme["text_color"]

        # Potentially update other controls in the page based on the new theme

        # Call page.update() again if necessary to trigger a re-render
        page.update()

    def update_theme(value):
        
        page.client_storage.set("burnison.me.current.theme", value.lower())
        if value.lower() == "light" or value is None:
            new_theme = light_theme()
        elif value.lower() == "dark":
            new_theme = dark_theme()
        elif value.lower() == "green":
            new_theme = green_theme()
        update_page_theme(page, new_theme)  # Call a function to apply the new theme

        
        

    theme_dropdown = ft.Dropdown(
        width=300,
        options=[
            ft.dropdown.Option("Light"),
            ft.dropdown.Option("Dark"), 
            ft.dropdown.Option("Green")
            ],
        label="Pick A Theme",
        on_change=lambda e: update_theme(e.control.value),
        color=current_theme["calc_theme"]["dropdown_text"],
        bgcolor=current_theme["calc_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_border_color"],
        select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    theme_info = ft.Text("Theme will update upon navigating from this page", size=12, color=current_theme["text_color"])

    update_frequency_dropdown = ft.Dropdown(
        width=300,
        options=[
            ft.dropdown.Option("Once a day(default)"),
            ft.dropdown.Option("Once a week"), 
            ft.dropdown.Option("Once a month")
            ],
        label="Update Frequency",
        on_change=lambda e: page.client_storage.set("update_frequency", e.control.value),
        color=current_theme["calc_theme"]["dropdown_text"],
        bgcolor=current_theme["calc_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_border_color"],
        select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    update_frequency_info = ft.Text("How often do you want to check the server for your updated data", size=12, color=current_theme["text_color"])

    return ft.View(
        "/settings",
        bgcolor=current_theme["background"],
        controls=[
            ft.Column(controls=[theme_dropdown,
                                 theme_info,
                                 ft.Divider(color=current_theme["border_color"]),
                                 #update_frequency_dropdown,
                                 #update_frequency_info
                                 ], width=400, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            appbar=appbar
        )