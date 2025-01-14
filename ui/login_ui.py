import flet as ft
from data.user import login
from ui.alert import create_loader, show_loader


def login_page(current_theme, page:ft.Page, BASE_URL:str):
        loader = create_loader(page)
        appbar = ft.AppBar(ft.Row(controls=[ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
        code_input = ft.TextField(label="Code", width=300, height=50, color=current_theme["list_item_colors"]["text_color"])
        return ft.View(
            controls=[
                ft.Text(spans=[ft.TextSpan("To log in, please login to your account on "),
                        ft.TextSpan("checkbookwizard.com", ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=ft.Colors.BLUE, color=ft.Colors.BLUE), on_click=lambda _: page.launch_url(BASE_URL)),
                        ft.TextSpan(", go to \"Settings\" and click the \"Generate Code\" button and the \"Copy Code\" button.  Then return to this app and paste the login code below.")],
                        color=current_theme["list_item_colors"]["text_color"],
                ),
                ft.ElevatedButton("Open checkbookwizard.com in browser", on_click=lambda _: page.launch_url(BASE_URL), bgcolor=current_theme["bottom_sheet"]["button_color"], color=current_theme["bottom_sheet"]["button_text_color"],),
                code_input,
                ft.ElevatedButton("Login with code", on_click=lambda _: login(page, code_input.value, BASE_URL, loader), bgcolor=current_theme["bottom_sheet"]["button_color"], color=current_theme["bottom_sheet"]["button_text_color"]),
            ],
            appbar=appbar,
            bgcolor=current_theme["background"]
        )
