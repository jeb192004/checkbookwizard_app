import flet as ft
from ui.my_controls import TextField, DeleteButton, Title
from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
import asyncio

async def delete_earnings(e, BASE_URL, id, user_id):
    page = e.control.page
    ds = DataSync(page, BASE_URL)
    loader = create_loader(page)
    show_loader(page, loader)
    response = await ds.delete_earning(id)
    if response["error"] is None:
        list_item = e.control.parent.parent.parent.parent
        listview = list_item.parent
        listview.controls.remove(list_item)
        listview.update()
    else:
        print(response["error"])
    hide_loader(page, loader)


def create_earnings_item(data, BASE_URL, current_theme):
    print(data)
    return ft.Container(
        content=ft.Column(
                    controls=[
                        Title(value=data["title"], size=18, color=current_theme["earnings_list_title_color"]),
                        ft.Row(
                            controls=[
                                TextField(label='Hours', value=data["hours"], read_only=True, width=70, text_size=14, height=42),
                                TextField(label='Amount', value=data["amount"], read_only=True, width=130, text_size=14, height=42),
                                ft.Row(controls=[DeleteButton(on_click=lambda e: asyncio.run(delete_earnings(e, BASE_URL=BASE_URL, id=data["id"], user_id=data["user_id"])) )],
                                       alignment=ft.MainAxisAlignment.END,
                                       expand=True
                                       )
                            ],
                            #expand=True
                        )
                    ]
                ),
        padding=ft.padding.all(10),
        margin=ft.margin.all(10),
        border_radius=10,
        border=ft.border.all(1,current_theme["border_color"]),
        bgcolor=current_theme["list_item_colors"]["base"]
    )