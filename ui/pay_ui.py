import asyncio
import flet as ft
from data.utils import format_dollar
from data.data_sync import add_update_earnings, get_earnings
from ui.alert import create_loader, show_loader, hide_loader
from data.earnings_list_item import create_earnings_item

payday_value = "5"

def pay_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    loader = create_loader(page)
    pay_list = ft.ListView()

    def radiogroup_changed(e):
        payday_value = e.control.value
        print(f"Your favorite color is:  {payday_value}")
        

    payday_options = ft.RadioGroup(content=ft.Column([
            ft.Radio(value="0", label="Sunday", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="1", label="Monday", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="2", label="Tuesday", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="3", label="Wednesday", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="4", label="Thursday", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="5", label="Friday(default)", label_style={"color": current_theme["text_color"]}),
            ft.Radio(value="6", label="Saturday", label_style={"color": current_theme["text_color"]})
        ]), on_change=radiogroup_changed)
    payday_options.value = "3"

    payday_column = ft.Column(col={"sm": 6}, controls=[
        ft.Text("Please select the day of the week you pay your bills", weight=ft.FontWeight.BOLD, size=28),
        payday_options])
    payday_container = ft.Container(content=payday_column, padding=ft.padding.all(10))
    
    hour_input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")

    avg_pay = ft.TextField(value="", label="Average Pay", prefix="$", border_color = current_theme["list_item_colors"]["total_amount_border_color"], color=current_theme["list_item_colors"]["total_amount_text_color"], on_change=lambda e: format_dollar(e, page, avg_pay))
    fourty_hours = ft.TextField(value="", label="40 Hour Pay", border_color = current_theme["list_item_colors"]["total_amount_border_color"], color=current_theme["list_item_colors"]["total_amount_text_color"], on_change=lambda e: format_dollar(e, page, fourty_hours))
    additional_hours_title = ft.TextField(value="", label="Title", border_color = current_theme["list_item_colors"]["total_amount_border_color"], color=current_theme["list_item_colors"]["total_amount_text_color"])
    additional_hours = ft.TextField(value="", label="Hours", border_color = current_theme["list_item_colors"]["total_amount_border_color"], color=current_theme["list_item_colors"]["total_amount_text_color"], input_filter=hour_input_filter)
    additional_hours_amount = ft.TextField(value="", label="Amount", border_color = current_theme["list_item_colors"]["total_amount_border_color"], color=current_theme["list_item_colors"]["total_amount_text_color"], on_change=lambda e: format_dollar(e, page, additional_hours))
    
    def save_update_data(e, type):
        title = None
        hours = 0
        amount = None
        if type == "avg":
            title = "Average Pay"
            amount = avg_pay.value
            avg_pay.border_color = current_theme["list_item_colors"]["total_amount_border_color"]
            if amount == "":
                avg_pay.border_color = "red"
                page.update()
                return
        elif type == "fourty":
            title = "40 Hour Pay"
            hours = 40
            amount = fourty_hours.value
            fourty_hours.border_color = current_theme["list_item_colors"]["total_amount_border_color"]
            if amount == "":
                fourty_hours.border_color = "red"
                page.update()
                return
        else:
            title = additional_hours_title.value
            hours = additional_hours.value
            amount = additional_hours_amount.value
            additional_hours_title.border_color = current_theme["list_item_colors"]["total_amount_border_color"]
            additional_hours.border_color = current_theme["list_item_colors"]["total_amount_border_color"]
            additional_hours_amount.border_color = current_theme["list_item_colors"]["total_amount_border_color"]
            if amount == "" or hours == "" or title == "":
                if title == "":
                    additional_hours_title.border_color = "red"
                if hours == "":
                    additional_hours.border_color = "red"
                if amount == "":
                    additional_hours_amount.border_color = "red"
                page.update()
                return
            
        page.update()
        show_loader(page, loader)
        
        avg_pay_value = avg_pay.value
        fourty_hours_value = fourty_hours.value
        json_data = {
            "user_id": user_id,
            "hours": hours,
            "amount": amount,
            "title": title
            
        }
        
        response = add_update_earnings(page, BASE_URL, json_data)
        hide_loader(page, loader)
        if response["error"] is None:
            if type == "avg":
                pass
            elif type == "fourty":
                pass
            else:
                additional_hours_title.value = ""
                additional_hours.value = ""
                additional_hours_amount.value = ""
                pay_list.controls.append(create_earnings_item(json_data, current_theme))
                page.update()
        else:
            if type == "avg":
                avg_pay.value = "There was an error, please try again"
            elif type == "fourty":
                fourty_hours.value = "There was an error, please try again"
            else:
                additional_hours_title.value = "There was an error, please try again"
                additional_hours.value = ""
                additional_hours_amount.value = ""

    pay_column = ft.Column(controls=[
        ft.Text("Pay(optional)", weight=ft.FontWeight.BOLD, size=28),
        avg_pay,
        ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=lambda e: save_update_data(e, "avg")),
        fourty_hours,
        ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=lambda e: save_update_data(e, "fourty")),
        ft.Text("Additional Hours of Pay(optional)", weight=ft.FontWeight.BOLD, size=28),
        additional_hours_title,
        additional_hours,
        additional_hours_amount,
        ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=lambda e: save_update_data(e, None)),
        
    ])
    pay_container = ft.Container(content=pay_column, padding=ft.padding.all(10))

    body = ft.ResponsiveRow([
        ft.Column(col={"sm": 6}, controls=[payday_container]),
        ft.Column(col={"sm": 6}, controls=[pay_container])
    ])

    
    
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: page.go("/bills")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    #floating_action_button = ft.FloatingActionButton(icon=ft.Icons.SAVE, on_click=save_update_data, bgcolor=current_theme["bottom_navigation_colors"]["background"], foreground_color=current_theme["bottom_navigation_colors"]["icon"], tooltip="Save or update data")
    
    page.views.append(
        ft.View(
            "/pay",
            padding=ft.padding.all(0),
            scroll=True,
            controls=[
                body,
                ft.Container(content=pay_list,padding=ft.padding.only(bottom=80)),
            ],
            appbar=appbar,
            #floating_action_button=floating_action_button,
            #bottom_appbar=bottom_appbar,
        )
    )

    async def build_earnings_list():
        data = await get_earnings(page, BASE_URL, user_id)
        print(data)
        if data["error"] is None:
            profile_pic = data["data"][0]["image_url"]
            day_of_week = data["data"][0]["day_of_week"]
            payday_options.value = day_of_week
            page.update()
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()
            for item in data["data"]:
                if item["title"] == "Average Pay":
                    avg_pay.value = item["amount"]
                elif item["title"] == "40 Hour Pay":
                    fourty_hours.value = item["amount"]
                else:
                    pay_list.controls.append(create_earnings_item(item, current_theme))
            page.update()
        else:
            print(data["error"])
    
    asyncio.run(build_earnings_list())
    
