import flet as ft


def create_earnings_item(data, current_theme):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(data["title"], size=18, color=current_theme["calc_theme"]["text_title"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.Text(f'Hours: {data["hours"]}', size=14, color=current_theme["calc_theme"]["text_title"]),
                ft.Text(f'Amount: {data["amount"]}', size=14, color=current_theme["calc_theme"]["text_title"]),
            ]
        ),
        padding=ft.padding.all(10),
    )