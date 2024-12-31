import flet as ft
def home_page(page:ft.Page, BASE_URL:str):
    return ft.View(
        "/",
                    [
                        ft.AppBar(title=ft.Text(page.title), bgcolor=ft.Colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                        ft.ElevatedButton("Bills", on_click=lambda _: page.go("/bills")),
                    ],
                )