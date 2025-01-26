import re
import flet as ft
import datetime
import asyncio

from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
from data.utils import navigate_to

appbar = []
def edit_bills_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    ds = DataSync(page, BASE_URL)
    loader = create_loader(page)

    bill_id_to_update = None

    date_text = ft.Text(bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"])
    def handle_change(e):
        print(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}")
        date_text.value = f"{e.control.value.strftime('%Y-%m-%d')}"
        page.update()
    def handle_dismissal(e):
        print(f"DatePicker dismissed")

    def open_date_picker(e, date_picker: ft.DatePicker):
        date_picker.pick_date()

    def on_amount_due_change(e):
        # Get the current input value, strip $, and reformat
        current_value = e.control.value.replace(".", "").replace(",", "")
        
        # Allow only digits
        if not current_value.isdigit():
            e.control.value = f"{amount_due.value}"
            page.update()
            return

        # Limit to a maximum length for formatting (e.g., max $9999.99)
        max_length = 15  # For up to "100,000,000,000.00"
        if len(current_value) > max_length:
            current_value = current_value[-max_length:]

        # Convert to dollar-and-cents format
        if len(current_value) <= 2:
            dollars = "0"
            cents = current_value.zfill(2)
        else:
            dollars = current_value[:-2]
            cents = current_value[-2:]

        formatted_value = f"{int(dollars):,}.{cents}"

        # Update the text field with the formatted value
        amount_due.value = formatted_value
        page.update()

    '''define controls here'''
    date_picker = ft.DatePicker(first_date=datetime.datetime.now(),
                                #last_date=datetime.datetime(year=2024, month=10, day=1),
                                on_change=handle_change,
                                on_dismiss=handle_dismissal,
                                )
    error_text = ft.TextField(bgcolor=ft.Colors.RED, color="white", visible=False)
    bill_id_text = ft.TextField(visible=False)
    name_text = ft.TextField(label="Company/Person/Name: ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    amount_due = ft.TextField(label="Amount Due: ", prefix_text="$", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]), on_change=on_amount_due_change)
    website = ft.TextField(label="Website(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    phone_number = ft.TextField(label="Phone Number(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    email = ft.TextField(label="Email(optional): ", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    due_date_picker = ft.ElevatedButton("Pick date",icon=ft.Icons.CALENDAR_MONTH,
                                        on_click=lambda e: open_date_picker(e, date_picker=date_picker),
                                                    bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"]
                                                    )
    due_date_column = ft.Row(controls=[ft.Column(controls=[due_date_picker, date_text], expand=True)], expand=True, visible=False)
    frequency_dropdown = ft.Dropdown(label="Frequency(how often bill is paid)",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))

    day_of_week_or_month_dropdown = ft.Dropdown(label="Day of Week or Month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    week_of_month_dropdown = ft.Dropdown(label="Select a week of the month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_dropdown = ft.Dropdown(label="Select a day of the week",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_row = ft.Row(controls=[ft.Column(controls=[week_of_month_dropdown,day_of_week_dropdown],expand=True)], expand=True,visible=False)
    day_of_month_dropdown = ft.Dropdown(label="Select a day of the month",expand=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    for i in range(1,32):
        day_of_month_dropdown.options.append(ft.dropdown.Option(str(i)))
    day_of_month_row = ft.Row(controls=[day_of_month_dropdown,], expand=True,visible=False)
    montly_row = ft.Row(controls=[
        ft.Column(controls=[
            day_of_week_or_month_dropdown,day_of_week_row,day_of_month_row
            ],expand=True),
        ], expand=True,visible=False)
    


    def frequency_dropdown_change(e):
        day_of_week_or_month_dropdown.value = None
        day_of_month_dropdown.value = None
        week_of_month_dropdown.value = None
        date_text.value = ""
        print(e.control.value)
        if e.control.value == "Weekly":
            if due_date_column.visible == True:
                due_date_column.visible = False
            if montly_row.visible == True:
                montly_row.visible = False
        
        if e.control.value == "Monthly":
            if due_date_column.visible == True:
                due_date_column.visible = False
            if montly_row.visible == False:
                montly_row.visible = True

        if e.control.value == "One Time":
            due_date_column.visible = True
            if montly_row.visible == True:
                montly_row.visible = False
        page.update()

    def day_of_week_or_month_dropdown_change(e):
        print(e.control.value)
        if e.control.value == "Day of Week (Mon, Tues, ect.)":
            if day_of_week_row.visible == False:
                day_of_week_row.visible = True
            if day_of_month_row.visible == True:
                day_of_month_row.visible = False
        if e.control.value == "Day of Month (1st, 2nd, ect.)":
            if day_of_month_row.visible == False:
                day_of_month_row.visible = True
            if day_of_week_row.visible == True:
                day_of_week_row.visible = False
        page.update()

    
    
    frequency_dropdown.options=[
            ft.dropdown.Option("Monthly"),
            ft.dropdown.Option("Weekly"),
            ft.dropdown.Option("One Time"),
        ]
    frequency_dropdown.on_change=lambda e: frequency_dropdown_change(e)

    day_of_week_or_month_dropdown.options=[
            ft.dropdown.Option("Day of Week (Mon, Tues, ect.)"),
            ft.dropdown.Option("Day of Month (1st, 2nd, ect.)"),
        ]
    day_of_week_or_month_dropdown.on_change=lambda e: day_of_week_or_month_dropdown_change(e)

    week_of_month_dropdown.options=[
            ft.dropdown.Option("First Week of the Month"),
            ft.dropdown.Option("Second Week of the Month"),
            ft.dropdown.Option("Third Week of the Month"),
            ft.dropdown.Option("Fourth Week of the Month"),
        ]
    #week_of_month_dropdown.on_change=lambda e: week_of_month_dropdown_change(e)

    day_of_week_dropdown.options=[
            ft.dropdown.Option("Sunday"),
            ft.dropdown.Option("Monday"),
            ft.dropdown.Option("Tuesday"),
            ft.dropdown.Option("Wednesday"),
            ft.dropdown.Option("Thursday"),
            ft.dropdown.Option("Friday"),
            ft.dropdown.Option("Saturday"),
        ]
    #day_of_week_dropdown.on_change=lambda e: day_of_week_dropdown_change(e)


    due_date_container = ft.Container(
        content=ft.Column(
            controls=[due_date_column,
                      montly_row,
            ],
            expand=True,
        ),
        expand=True,
    )

    def save(e):
        show_loader(page, loader)
        date_to_save = ""
        if name_text.value == "":
            name_text.border_color = ft.Colors.RED
            name_text.update()
            hide_loader(page, loader)
            return
        else:
            name_text.border_color = None
            name_text.update()
        if frequency_dropdown.value is not None:
            frequency_dropdown.border_color = None
            frequency_dropdown.update()
            if frequency_dropdown.value == "Weekly":
                date_to_save = ""
            if frequency_dropdown.value == "One Time":
                if date_text.value != "":
                    date_text.bgcolor = current_theme["list_item_colors"]['base']
                    page.update()
                    date_to_save = date_text.value #format = 2024-11-05
                    print("date_to_save: ", date_to_save)
                else:
                    date_text.value = "Please select a due date"
                    date_text.bgcolor = ft.Colors.RED
                    page.update()
                    hide_loader(page, loader)
                    return
            if frequency_dropdown.value == "Monthly":
                if day_of_week_or_month_dropdown.value is not None:
                    day_of_week_or_month_dropdown.border_color = None
                    day_of_week_or_month_dropdown.update()
                    if day_of_week_or_month_dropdown.value == "Day of Week (Mon, Tues, ect.)":
                        if week_of_month_dropdown.value is not None:
                            week_of_month_dropdown.border_color = None
                            week_of_month_dropdown.update()
                        else:
                            week_of_month_dropdown.border_color = ft.Colors.RED
                            week_of_month_dropdown.update()
                            hide_loader(page, loader)
                            return
                        if day_of_week_dropdown.value is not None:
                            day_of_week_dropdown.border_color = None
                            day_of_week_dropdown.update()
                            hide_loader(page, loader)
                        else:
                            day_of_week_dropdown.border_color = ft.Colors.RED
                            day_of_week_dropdown.update()
                            hide_loader(page, loader)
                            return
                        if week_of_month_dropdown.value and day_of_week_dropdown.value:
                            date_to_save = f"{week_of_month_dropdown.value.split()[0]}-{day_of_week_dropdown.value}"
                    if day_of_week_or_month_dropdown.value == "Day of Month (1st, 2nd, ect.)":
                        if day_of_month_dropdown.value is not None:
                            day_of_month_dropdown.border_color = None
                            date_to_save = day_of_month_dropdown.value
                            day_of_month_dropdown.update()
                        else:
                            day_of_month_dropdown.border_color = ft.Colors.RED
                            day_of_month_dropdown.update()
                            hide_loader(page, loader)
                            return
                else:
                    day_of_week_or_month_dropdown.border_color = ft.Colors.RED
                    day_of_week_or_month_dropdown.update()
                    hide_loader(page, loader)
                    return
        else:
            frequency_dropdown.border_color = ft.Colors.RED
            frequency_dropdown.update()
            hide_loader(page, loader)
            return
        if amount_due.value == "":
            amount_due.border_color = ft.Colors.RED
            amount_due.update()
            hide_loader(page, loader)
            return
        else:
            amount_due.border_color = None
            amount_due.update()

        new_update = "new"
        
        if bill_id_text.value != "":
            new_update = "update"
        print(bill_id_text.value, new_update)
        json_data = {
            "user_id": user_id,
            "new_update": new_update,
            "id": bill_id_text.value,
            "due": date_to_save,
            "name": name_text.value,
            "amount": f"${amount_due.value}",
            "frequency": "single" if frequency_dropdown.value == "One Time" else frequency_dropdown.value.lower(),
            "phone": phone_number.value,
            "website": website.value,
            "email": email.value,
        }
        error_text.visible = True
        page.update()
        print(json_data)
        response = ds.add_update_bills(json_data)
        if response == "success":
            navigate_to(page, loader, "/bills")
        else:
            error_text.value = "Something went wrong, please try again"
            error_text.visible = True
            page.update()

    def remove_bill(e, bill_id):
        json_data = {
            "user_id": user_id,
            "id": bill_id
        }
        response = ds.remove_bill_item(json_data)
        if response == "success":
            navigate_to(page, loader, "/bills")
        else:
            error_text.value = "Something went wrong, please try again"
            error_text.visible = True
            page.update()
        

    floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=save, bgcolor=ft.Colors.LIME_300)

    bill_list_button = ft.Column(
        controls=[ft.Image(src="/receipt_long.png", width=25, height=25, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Bill\nList", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    charts_button = ft.Column(
        controls=[ft.Icon(name=ft.Icons.TRENDING_UP,color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Charts", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    clear_button = ft.Column(
        controls=[ft.Icon(name=ft.Icons.CLEAR, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Clear\nForm", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )
    
    edit_bills_button = ft.Column(
        controls=[ft.Image(src="/checkbook.png", width=25, height=25, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Edit", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )
    
    save_button = ft.Column(
        controls=[ft.Icon(name=ft.Icons.SAVE, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Save", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    def bill_details(e, bill_id):
        print(f"{bill_id}")

    def edit_bill(e):
        bill = e.control.parent.data  if e != "clear" else ""
        print(f"{e.control.parent.data}" if e != "clear" else "clear")
        day_of_week_row.visible = False
        day_of_month_row.visible = False
        due_date_column.visible = False
        montly_row.visible = False
        day_of_week_or_month_dropdown.value = None
        day_of_month_dropdown.value = None
        week_of_month_dropdown.value = None
        date_text.value = ""

        bill_id_text.value = bill["id"] if e != "clear" else ""
        name_text.value = bill["name"] if e != "clear" else ""
        amount_due.value = bill["amount"].strip('$') if e != "clear" else ""
        phone_number.value = bill["phone"] if e != "clear" else ""
        email.value = bill["email"] if e != "clear" else ""
        website.value = bill["website"] if e != "clear" else ""
        bill_frequency_to_update = bill["frequency"] if e != "clear" else "clear"
        if bill_frequency_to_update == "weekly":
            frequency_dropdown.value = "Weekly"  
        elif bill_frequency_to_update == "monthly":
            frequency_dropdown.value = "Monthly"
            if len(bill["due"]) < 3 and bill["due_date"] is None:
                montly_row.visible = True
                day_of_week_or_month_dropdown.value = "Day of Month (1st, 2nd, ect.)"
                day_of_month_row.visible = True
                day_of_month_dropdown.value = bill["due"]
            else:
                day_of_week_row.visible = True
                week_of_month_dropdown.value = bill["due"].split(' ')[0]
                day_of_week_dropdown.value = bill["due"].split(' ')[1]
        elif bill_frequency_to_update == "one_time":
            frequency_dropdown.value = "One Time"
        
        bill_bottom_sheet.visible = False
        page.update()
                
    bottom_sheet_bill_list = ft.ListView(
                expand=False,
                spacing=10,
            )
    
    bill_bottom_sheet = ft.Container(
        content=ft.Container(
            content=bottom_sheet_bill_list,
            bgcolor=current_theme['bottom_sheet']['background_color'],
            border=None,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.only(top=10, left=10, right=10, bottom=10),
            margin=ft.margin.all(0),
            alignment=ft.alignment.bottom_center,
            width=400,
            height=500,
            expand=False
        ),
    visible=False,
    bottom=0,
    left=10,
    right=10,
    shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=2,
            color=current_theme["shadow_color"],
            offset=ft.Offset(0, -4),  # Negative offset for top shadow
        ),
    )

    def toggle_bill_list(e):
        if bill_bottom_sheet.visible:
            bill_bottom_sheet.visible = False
        else:
            bill_bottom_sheet.visible = True
        
        page.update()
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: navigate_to(page, loader, "/bills")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
            
    bottom_appbar = ft.BottomAppBar(
        bgcolor=current_theme["bottom_navigation_colors"]["background"],
        shape=ft.NotchShape.CIRCULAR,
        elevation=10,
        content=ft.Row(
            controls=[
                ft.Container(content=bill_list_button,expand=True, on_click=lambda _: toggle_bill_list(None)),
                ft.Container(expand=True),
                #ft.Container(content=charts_button,expand=True, on_click=lambda _: go_to_page("charts")),
                #ft.Container(expand=True),
                ft.Container(content=clear_button,expand=True, on_click=lambda _: edit_bill("clear")),
                #ft.Container(expand=True),
                #ft.Container(content=edit_bills_button,expand=True, on_click=lambda _: go_to_page("edit_bills")),
                ft.Container(expand=True),
                ft.Container(content=save_button,expand=True, on_click=lambda _: save(_)),
                
            ]
        ),
    )
    page.overlay.append(date_picker)
    page.views.append(ft.View("/charts",
                              controls=[ft.Stack(
                                  controls=[ft.Column(controls=[
                                        bill_id_text,
                                        name_text,
                                        frequency_dropdown,
                                        due_date_container,
                                        amount_due,
                                        website,
                                        phone_number,
                                        email,
                                        
                                      ],
                                      expand=True,
                                      horizontal_alignment="center",
                                      scroll=ft.ScrollMode.AUTO
                                      ),
                                      bill_bottom_sheet
                                      ],
                                      expand=True
                                    )
                                ],
                                padding=ft.padding.only(top=10, left=10, right=10, bottom=0),
                                appbar=appbar,
                                bottom_appbar=bottom_appbar,
                                #floating_action_button=floating_action_button,
                                bgcolor=current_theme["background"]
                            )
                        )
    
    def create_bill_list(page, current_theme, my_bills):
        bill_list = []
        for bill in my_bills:
            #print(bill)
            due_text = due_text = ft.Text("Due:", size=14, color=current_theme['calc_theme']['text_title'])
            if bill["frequency"] != "weekly" and bill["due"]:
                due_text = ft.Text(f"Due: {bill['due']}", size=14, color=current_theme['calc_theme']['text_title'])
            elif bill["frequency"] != "weekly" and (bill["due_date"]):
                due_text = ft.Text(f"Due: {bill['due_date']}", size=14, color=current_theme['calc_theme']['text_title'])
            elif bill["frequency"] == "weekly":
                due_text = ft.Text(f"Due: Weekly", size=14, color=current_theme['calc_theme']['text_title'])
            bill_list.append(ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(bill["name"], size=18, color=current_theme['calc_theme']['text_title'],style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                        due_text,
                        ft.Text(f'Amount: {bill["amount"]}', size=14, color=current_theme['calc_theme']['text_title']),
                        ft.Text(f'Frequency: {bill["frequency"]}', size=14, color=current_theme['calc_theme']['text_title']),
                        ft.Text(f'Phone: {bill["phone"]}', size=14, color=current_theme['calc_theme']['text_title']),
                        ft.Text(f'Email: {bill["email"]}', size=14, color=current_theme['calc_theme']['text_title']),
                        ft.Text(f'Website: {bill["website"]}', size=14, color=current_theme['calc_theme']['text_title']),
                        ft.Row(controls=[
                                ft.ElevatedButton("Delete", on_click=lambda e, bill=bill: remove_bill(e, f"{bill['id']}")),
                                ft.ElevatedButton("Edit", on_click=lambda e: edit_bill(e)),
                            ],
                            data=bill,
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ]
                ),
                bgcolor=current_theme["list_item_colors"]["inner_container"],
                border_radius=ft.border_radius.all(5),
                padding=ft.padding.all(10),
                margin=ft.margin.all(0),
            ))

        return bill_list


    async def build_bill_list():
        data = await ds.get_bills()
        if data["error"] is not None or data["error"] != "":
            profile_pic=None
            if "profile_pic" in data:
                profile_pic = data["profile_pic"]
            #user_pay_hours = data["user_pay_hours"]
            my_bills=[]
            if "my_bills" in data:
                my_bills = data["my_bills"]
                bill_list = create_bill_list(page, current_theme, my_bills)
                bottom_sheet_bill_list.controls = bill_list
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()
        else:
            print(data["error"])
    
    asyncio.run(build_bill_list())