import flet as ft
from data.user import login


def login_page(current_theme, page:ft.Page, BASE_URL:str):
        appbar = ft.AppBar(leading=ft.Image(src="/header.png", fit=ft.ImageFit.CONTAIN), leading_width=200, bgcolor=ft.colors.SURFACE_VARIANT)
        code_input = ft.TextField(label="Code", width=300, height=50)
        return ft.View(
            controls=[
                ft.Text(spans=[ft.TextSpan("To log in, please login to your account on "),
                        ft.TextSpan("j-bills.com", ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=ft.colors.BLUE, color=ft.colors.BLUE), on_click=lambda _: page.launch_url(BASE_URL)),
                        ft.TextSpan(", go to \"Settings\" and click the \"Generate Code\" button and the \"Copy Code\" button.  Then return to this app and paste the login code below.")],
                ),
                ft.ElevatedButton("Open j-bills.com in browser", on_click=lambda _: page.launch_url(BASE_URL)),
                code_input,
                ft.ElevatedButton("Login with code", on_click=lambda _: login(page, code_input.value, BASE_URL)),
            ],
            appbar=appbar
        )
