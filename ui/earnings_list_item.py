import flet as ft
from ui.my_controls import TextField, DeleteButton, Title


def delete_earning(e, earning_id):
    print(f"Deleting earning with ID: {earning_id}")


def create_earnings_item(data, current_theme):
    return ft.Container(
                ft.Column(
                    controls=[
                        Title(value=data["title"], size=18, color=current_theme["earnings_list_title_color"]),
                        ft.Row(
                            controls=[
                                TextField(label='Hours', value=data["hours"], read_only=True, width=60, text_size=14, height=42),
                                TextField(label='Amount', value=data["amount"], read_only=True, width=130, text_size=14, height=42),
                                ft.Row(controls=[DeleteButton(on_click=lambda e: delete_earning(e, data["id"]))],
                                       alignment=ft.MainAxisAlignment.END,
                                       expand=True
                                       )
                            ],
                            expand=True
                        )
                    ]
                ),
              
        padding=ft.padding.all(10),
        margin=ft.margin.all(10),
        border_radius=10,
        border=ft.border.all(1,current_theme["border_color"]),
        bgcolor=current_theme["list_item_colors"]["base"],
    )