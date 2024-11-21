import flet as ft
def create_loader(page):
    progress_bar = ft.ProgressBar(width=250, right=20, bottom=0, bar_height=10,border_radius=5, color="#71b681")
    loader = ft.AlertDialog(
        content=ft.Stack(
            controls=[
                ft.Image(src="/header-colored.png", width=300),
                progress_bar
            ],
            height=125,
        ),
        modal=True
    )
    page.overlay.append(loader)
    return loader

def show_loader(page, loader):
    loader.open = True
    page.update()

def hide_loader(page, loader):
    loader.open = False
    page.update()