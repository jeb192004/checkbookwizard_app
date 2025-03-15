import re
import flet as ft
import datetime
import asyncio

from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
from data.utils import navigate_to
from ui.my_controls import ElevatedButton

appbar = []
def edit_bills_page(current_theme, page:ft.Page, BASE_URL:str):
    ds = DataSync(page, BASE_URL)
    loader = create_loader(page)

    bill_id_to_update = None

    date_text = ft.Text(bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"])
    selected_text=ft.TextField(label="Selected Frequency", border_color=current_theme["text_field"]["border_color"], read_only=True, bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))

    def handle_change(e):
        print(f"Date changed: {e.control.value.strftime('%Y-%m-%d')}")
        selected_text.value = f"{e.control.value.strftime('%Y-%m-%d')}"
        page.update()
    def handle_dismissal(e):
        print(f"DatePicker dismissed")

    def open_date_picker(e, date_picker: ft.DatePicker):
        page.open(date_picker)

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
    name_text = ft.TextField(label="Company/Person/Name: ", border_color=current_theme["text_field"]["border_color"], bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    item_width=name_text.width
    amount_due = ft.TextField(label="Amount Due: ", border_color=current_theme["text_field"]["border_color"], prefix_text="$", bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]), on_change=on_amount_due_change)
    website = ft.TextField(label="Website(optional): ", border_color=current_theme["text_field"]["border_color"], bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    phone_number = ft.TextField(label="Phone Number(optional): ", border_color=current_theme["text_field"]["border_color"], bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    email = ft.TextField(label="Email(optional): ", border_color=current_theme["text_field"]["border_color"], bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    due_date_picker = ft.ElevatedButton("Pick date",icon=ft.Icons.CALENDAR_MONTH,
                                        on_click=lambda e: open_date_picker(e, date_picker=date_picker),
                                                    bgcolor=current_theme["list_item_colors"]['base'], color=current_theme["text_color"]
                                                    )
    due_date_column = ft.Row(controls=[ft.Column(controls=[due_date_picker, date_text], expand=True)], expand=True, visible=False)
    frequency_dropdown = ft.Dropdown(label="Frequency(how often bill is paid)", width=300, fill_color=current_theme["dropdown"]['background'], filled=True, bgcolor=current_theme["list_item_colors"]['base'],expand=True, color=current_theme["text_color"], border_color=current_theme["text_field"]["border_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_or_month_dropdown = ft.Dropdown(label="Day of Week or Month", width=300, bgcolor=current_theme["list_item_colors"]['base'], border_color=current_theme["text_field"]["border_color"], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    week_of_month_dropdown = ft.Dropdown(label="Select a week of the month", width=200, bgcolor=current_theme["list_item_colors"]['base'], border_color=current_theme["text_field"]["border_color"], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_dropdown = ft.Dropdown(label="Select a day of the week", width=200, bgcolor=current_theme["list_item_colors"]['base'], border_color=current_theme["text_field"]["border_color"], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    day_of_week_row = ft.Container(content=ft.Column(controls=[week_of_month_dropdown,day_of_week_dropdown]), expand=True, alignment=ft.alignment.center)
    day_of_month_dropdown = ft.Dropdown(label="Select a day of the month", max_menu_height=300, width=200, bgcolor=current_theme["dropdown"]['background'], border_color=current_theme["text_field"]["border_color"], color=current_theme["text_color"], label_style=ft.TextStyle(color=current_theme["text_color"]))
    for i in range(1,32):
        day_of_month_dropdown.options.append(ft.DropdownOption(text=str(i), style=ft.ButtonStyle(color=current_theme["text_color"])))
    day_of_month_row = ft.Row(controls=[day_of_month_dropdown,])
    montly_row = ft.Row(controls=[
        ft.Column(controls=[
            day_of_week_or_month_dropdown,day_of_week_row,day_of_month_row
            ],
            expand=True,
            alignment=ft.alignment.center,),
        ], expand=True,visible=False)
    
    frequency_modal = ft.AlertDialog()

    def week_modal_submit(e):
        page.close(week_modal)
        if week_of_month_dropdown.value and day_of_week_dropdown.value:
            date_to_save = f"{week_of_month_dropdown.value.split()[0]}-{day_of_week_dropdown.value}"
        selected_text.value=date_to_save
        page.update()

    week_modal = ft.AlertDialog(
        modal=True,
        content=ft.Container(content=ft.Column(controls=[
            day_of_week_row
        ]),
        height=100,
        alignment=ft.alignment.center,
        expand=True),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            ft.TextButton("Submit", on_click=lambda e: week_modal_submit(week_modal),style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.TextButton("Cancel", on_click=lambda e: page.close(week_modal),style=ft.ButtonStyle(color=current_theme["text_color"])),
        ],
        bgcolor=current_theme["alert_background_color"]
    )

    def day_modal_submit(e):
        page.close(day_modal)
        selected_text.value=day_of_month_dropdown.value
        page.update()
        
    day_modal = ft.AlertDialog(
        modal=True,
        content=ft.Container(content=ft.Column(controls=[
            day_of_month_dropdown
        ]),
        height=50,
        alignment=ft.alignment.center,
        expand=True),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            ft.TextButton("Submit", on_click=lambda e: day_modal_submit(day_modal),style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.TextButton("Cancel", on_click=lambda e: page.close(day_modal),style=ft.ButtonStyle(color=current_theme["text_color"])),
        ],
        bgcolor=current_theme["alert_background_color"]
    )
    def open_month_modal(e):
        page.close(frequency_modal)
        if e=="week":
            page.open(week_modal)
        elif e=="day":
            page.open(day_modal)
        else:
            pass
        
    
    frequency_modal.modal=True
    frequency_modal.content=ft.Container(content=ft.Column(controls=[
            ft.Row(controls=[ElevatedButton(text="Day of Week (Mon, Tues, ect.)",  on_click=lambda e:open_month_modal("week"), expand=True, bgcolor=current_theme["alert_button_color"], color=current_theme["text_color"])]),
            ft.Row(controls=[ElevatedButton(text="Day of Month (1st, 2nd, ect.)",  on_click=lambda e:open_month_modal("day"), expand=True, bgcolor=current_theme["alert_button_color"], color=current_theme["text_color"])]),
        ], spacing=20),
        height=100,
        )
    frequency_modal.actions=[
            ft.TextButton("Cancel", on_click=lambda e: page.close(frequency_modal), style=ft.ButtonStyle(color=current_theme["text_color"])),
        ]
    frequency_modal.actions_alignment=ft.MainAxisAlignment.END
    frequency_modal.bgcolor=current_theme["alert_background_color"]

    def frequency_dropdown_change(e):
        if e.control.value == "One Time":
            open_date_picker(e, date_picker=date_picker)
        elif e.control.value == "Weekly":
            selected_text.value=e.control.value
            page.update()
        else:
            page.open(frequency_modal)
        

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
            ft.DropdownOption(text="Monthly", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.DropdownOption(text="Weekly", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.DropdownOption(text="One Time", style=ft.ButtonStyle(color=current_theme["text_color"])),
        ]
    frequency_dropdown.on_change=lambda e: frequency_dropdown_change(e)

    '''day_of_week_or_month_dropdown.options=[
            ft.dropdown.Option("Day of Week (Mon, Tues, ect.)"),
            ft.dropdown.Option("Day of Month (1st, 2nd, ect.)"),
        ]
    day_of_week_or_month_dropdown.on_change=lambda e: day_of_week_or_month_dropdown_change(e)
'''
    week_of_month_dropdown.options=[
            ft.dropdown.Option(text="First Week of the Month", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Second Week of the Month", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Third Week of the Month", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Fourth Week of the Month", style=ft.ButtonStyle(color=current_theme["text_color"])),
        ]
    #week_of_month_dropdown.on_change=lambda e: week_of_month_dropdown_change(e)

    day_of_week_dropdown.options=[
            ft.dropdown.Option(text="Sunday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Monday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Tuesday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Wednesday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Thursday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Friday", style=ft.ButtonStyle(color=current_theme["text_color"])),
            ft.dropdown.Option(text="Saturday", style=ft.ButtonStyle(color=current_theme["text_color"])),
        ]
    #day_of_week_dropdown.on_change=lambda e: day_of_week_dropdown_change(e)

    def save(e):
        show_loader(page, loader)
        if name_text.value == "":
            name_text.border_color = ft.Colors.RED
            name_text.update()
            hide_loader(page, loader)
            return
        else:
            name_text.border_color = None
            name_text.update()
        if selected_text.value != "":
            frequency_dropdown.border_color = None
            selected_text.border_color = None
            selected_text.update()
        else:
            selected_text.boarder_color=ft.Colors.RED
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
        #print(bill_id_text.value, new_update)
        json_data = {
            "new_update": new_update,
            "id": bill_id_text.value,
            "due": "" if frequency_dropdown.value == "One Time" else selected_text.value,
            "due_date": selected_text.value if frequency_dropdown.value == "One Time" else "",
            "name": name_text.value,
            "amount": f"${amount_due.value}",
            "frequency": "single" if frequency_dropdown.value == "One Time" else frequency_dropdown.value.lower(),
            "phone": phone_number.value,
            "website": website.value,
            "email": email.value,
        }
        error_text.visible = True
        page.update()
        #print(json_data)
        response = ds.add_update_bills(json_data)
        if response == "success":
            navigate_to(page, loader, "/refresh_edit_bills")
        else:
            error_text.value = "Something went wrong, please try again"
            error_text.visible = True
            page.update()

    def remove_bill(e, bill_id):
        show_loader(page, loader)
        json_data = {
            "id": bill_id
        }
        response = ds.remove_bill_item(json_data)
        hide_loader(page, loader)
        if response == "success":
            navigate_to(page, loader, "/refresh_edit_bills")
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
        #date_text.value = ""

        bill_id_text.value = bill["id"] if e != "clear" else ""
        name_text.value = bill["name"] if e != "clear" else ""
        amount_due.value = bill["amount"].strip('$') if e != "clear" else ""
        phone_number.value = bill["phone"] if e != "clear" else ""
        email.value = bill["email"] if e != "clear" else ""
        website.value = bill["website"] if e != "clear" else ""
        bill_frequency_to_update = bill["frequency"] if e != "clear" else "clear"
        if bill_frequency_to_update == "weekly":
            frequency_dropdown.value = "Weekly"  
            selected_text.value="Weekly"
        elif bill_frequency_to_update == "monthly":
            frequency_dropdown.value = "Monthly"
            selected_text.value = bill["due"]
        elif bill_frequency_to_update == "single":
            frequency_dropdown.value = "One Time"
            selected_text.value = bill["due_date"]
        else:
            frequency_dropdown.value = None
            selected_text.value = ""
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
                                        selected_text,
                                        amount_due,
                                        website,
                                        phone_number,
                                        email,
                                        
                                      ],
                                      #expand=True,
                                      horizontal_alignment="center",
                                      #scroll=ft.ScrollMode.AUTO
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
        data = await ds.get_bill_list()
        #print(data)
        if data["error"] is not None or data["error"] != "":
            profile_pic=None
            if "profile_pic" in data:
                profile_pic = data["profile_pic"]
            if "data" in data:
                data=data["data"]
                my_bills=[]
                if data is not None:
                    my_bills = data["bills"]
                    #print(my_bills)
                    bill_list = create_bill_list(page, current_theme, my_bills)
                    bottom_sheet_bill_list.controls = bill_list
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()
        else:
            print(data["error"])
    
    asyncio.run(build_bill_list())