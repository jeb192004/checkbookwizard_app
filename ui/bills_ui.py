import flet as ft
from datetime import datetime, date, timedelta
import json
from data.bills import get_bills, save_unpaid_bills, remove_unpaid_bills
from ui.alert import create_loader, show_loader, hide_loader

selected_total_bills_amount = 0
def bills_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    loader = create_loader(page)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)#365
    day_of_week = 5  # Friday(default)
    billListItems = []
    my_bills = []
    unpaid_bills = []
    profile_page = None
    profile_pic = None
    user_pay_hours = []
    
    def remove_unpaid(e):
        selected = []
        bill_list = e.control.parent.parent.parent.controls[1].content.content.controls
        for bill in bill_list:
            if "row" not in str(bill.content):
                c_box = bill.content.controls[0].controls[2]
                if c_box.visible ==True:
                    c_box.visible = False
                else:
                    c_box.visible = True
                if c_box.value == True:
                    '''for m_bill in my_bills:
                        if m_bill["id"] == c_box.data["bill_id"]:
                            m_bill["payday"] = c_box.data["payday"].strftime("%Y-%m-%d")'''
                    selected.append({"id":c_box.data["bill_id"], "payday": c_box.data["payday"].strftime("%Y-%m-%d")})
        if e.control.icon == "edit":
            e.control.icon = ft.icons.SAVE
        elif e.control.icon == "save":
            e.control.icon = ft.icons.EDIT
        if len(selected)>0:
            show_loader(page, loader)
            remove_unpaid_bills(page, selected, BASE_URL)
            selected = []
            bills_page(current_theme, page, BASE_URL, user_id)
        page.update()

    def edit_bill_list(e):
        selected = []
        bill_list = e.control.parent.parent.parent.controls[1].content.content.controls
        for bill in bill_list:
            if "row" not in str(bill.content):
                c_box = bill.content.controls[0].controls[2]
                if c_box.visible ==True:
                    c_box.visible = False
                else:
                    c_box.visible = True
                if c_box.value == False:
                    for m_bill in my_bills:
                        if m_bill["id"] == c_box.data["bill_id"]:
                            m_bill["payday"] = c_box.data["payday"].strftime("%Y-%m-%d")
                            selected.append(m_bill)
        if e.control.icon == "edit":
            e.control.icon = ft.icons.SAVE
        elif e.control.icon == "save":
            e.control.icon = ft.icons.EDIT
        if len(selected)>0:
            show_loader(page, loader)
            save_unpaid_bills(page, selected, BASE_URL)
            selected = []
            bills_page(current_theme, page, BASE_URL, user_id)
        page.update()

        

    
    def get_weekly_dates(start_date, day_of_week, end_date):
        current = start_date.replace()
        print(end_date.date())
        result = []
        while current.date() != end_date.date():
            if current.isoweekday() == day_of_week:
                result.append(current)
                #print(current.isoweekday(), current.date())
            if current.date() != end_date.date():
                try:
                    current = current + timedelta(days=1)
                except OverflowError:
                    print("OverflowError: Current date is too large", current)
                    break
            # Check for end_date and weekday match to break the loop
            if current.date() == end_date.date():
                break
            
        return result

    # Get weekly dates for the next year
    weekly_dates = get_weekly_dates(start_date, day_of_week, end_date)

    
    def create_bill_item(bill, due_date, isEditable, week_date, past_due):

            checkbox = ft.Container()
            checkbox_value = True
            if past_due:
                checkbox_value = False
            if isEditable:
                checkbox = ft.Checkbox(label="Paid", value=checkbox_value, label_position=ft.LabelPosition.LEFT, data={"bill_id": bill["id"], "payday": week_date}, visible=False)
            bill_item_text_size = 15
            bill_item_text_color = current_theme["list_item_colors"]["text_color"]
            website_row = ft.Row()
            phone_row = ft.Row()
            email_row = ft.Row()
            website = bill["website"]
            phone = bill["phone"]
            email = bill["email"]
            if website:
                website_row = ft.Text(size=15, spans=[ft.TextSpan("Website: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                        ft.TextSpan(website, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: page.launch_url(website)),])
            if phone:
                phone_row = ft.Text(size=15, spans=[ft.TextSpan("Phone: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                        ft.TextSpan(phone, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: page.launch_url(f"tel:{phone}")),])
            if email:
                email_row = ft.Text(size=15, spans=[ft.TextSpan("Email: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                        ft.TextSpan(email, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: page.launch_url(f"mailto:{email}")),])
            return ft.Container(
                content=ft.Column([
                    ft.Row(controls=[ft.Text(bill["name"], size=20, color=current_theme["list_item_colors"]["bill_name_color"], style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Container(expand=True), checkbox],),
                    ft.Row(controls=[ft.Row(controls=[ft.Text(f"DUE: ", size=bill_item_text_size, color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(f"{due_date}", size=bill_item_text_size, color=bill_item_text_color)]), ft.Row(expand=True),ft.Row(controls=[ft.Text(f"Amount: ", size=bill_item_text_size,color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(f"{bill['amount']}", size=bill_item_text_size, color=bill_item_text_color)])], expand=True),
                    website_row,
                    phone_row,
                    email_row,
                    ft.Divider(height=2, color=ft.colors.BLACK),
                    ],
                    spacing=2,
                    ),
                margin=ft.margin.all(10),
                )
            
    def getWeekdayOfMonth(year, month, week_date, weekdayIndex, occurrence):
        #print(weekdayIndex, occurrence)
        firstDay = datetime(year=year, month=month, day=1)
        # Adjust the first day of the month to treat Sunday as 0
        first_day_adjusted = (firstDay.weekday() + 1) % 7
        # Find the first occurrence of the given weekday in the month
        days_to_add = (weekdayIndex - first_day_adjusted + 7) % 7
        first_occurrence = firstDay + timedelta(days=days_to_add)
        # Calculate the date of the specified occurrence
        target_date = first_occurrence + timedelta(weeks=occurrence - 1)
        
        return target_date.day

    def build_bill_list(bills, week_date, past_due, isEditable):
        week_date = week_date.date()
        week_date2 = week_date + timedelta(days=6)
        day = week_date
        month = week_date.month
        week = week_date.isocalendar().week
        year = week_date.year
        month2 = week_date2.month
        bill_list = []
        bills_total_amount = 0
        for bill in bills:
            dueDate = None
            due = bill['due']
            if bill["frequency"] == "weekly":
                due = week_date.day
            elif bill["frequency"] == "single":
                due = bill["due_date"]
            elif bill["frequency"] == "monthly" and past_due == False:
                if  len(due) > 2:
                    #print(due)
                    weekdayIndex = 0
                    occurrence = 0
                    if due.split('-')[1] == 'Sunday': weekdayIndex = 0 
                    if due.split('-')[1] == 'Monday': weekdayIndex = 1 
                    if due.split('-')[1] == 'Tuesday': weekdayIndex = 2 
                    if due.split('-')[1] == 'Wednesday': weekdayIndex = 3 
                    if due.split('-')[1] == 'Thursday': weekdayIndex = 4 
                    if due.split('-')[1] == 'Friday': weekdayIndex = 5 
                    if due.split('-')[1] == 'Saturday': weekdayIndex = 6 

                    if due.split('-')[0] == 'First': occurrence = 0; due_date_text = '1st ' + due.split('-')[1] 
                    if due.split('-')[0] == 'Second': occurrence = 7; due_date_text = '2nd ' + due.split('-')[1] 
                    if due.split('-')[0] == 'Third': occurrence = 7 + 7; due_date_text = '3rd ' + due.split('-')[1] 
                    if due.split('-')[0] == 'Fourth': occurrence = 7 + 7 + 7; due_date_text = '4th ' + due.split('-')[1] 

                    
                    dayOfMonth = getWeekdayOfMonth(year, month, week_date, weekdayIndex, occurrence)
                    due = dayOfMonth
            
            if bill["frequency"] == "single":
                dueDate = due
            else:
                dueDate = f'{week_date.year}-{int(due):02d}-{week_date.month}'
            
            #print(week_date, dueDate, bill['name'])
            try:
                dueDate = datetime.strptime(str(dueDate), "%Y-%d-%m").date()
                if bill["frequency"] == "single":
                    dueDate = datetime.strptime(str(dueDate), "%Y-%m-%d").date()
                    y = dueDate.year
                    m = dueDate.month
                    d = dueDate.day
                    dueDate = datetime.strptime(str(f'{y}-{d:02d}-{m}'), "%Y-%m-%d").date()
                    #print(y, m, d, dueDate)
            except ValueError as e:
                if e.args[0] == 'day is out of range for month':
                    #print(e, due, bill['name'])
                    due = int(due)-6
                    dueDate = datetime.strptime(str(f'{week_date.year}-{due:02d}-{week_date.month}'), "%Y-%d-%m").date()
                else:
                    print(e)
                
            if month != month2 and dueDate.day < 6 and dueDate<week_date2:
                #print(dueDate, 'duedate')
                
                dueDateMonth = week_date.month+1
                dueDay = dueDate.day
                dueDateYear = week_date.year
                if dueDateMonth == 13:
                        dueDateMonth = 1
                        dueDateYear = week_date.year+1
                
                try:
                    
                    dueDate = datetime.strptime(str(f'{dueDateYear}-{dueDate}-{dueDateMonth:02d}'), "%Y-%dd-%m").date()
                except ValueError as e:
                    try:
                        dueDate = datetime.strptime(str(f'{dueDateYear}-{dueDay:02d}-{dueDateMonth:02d}'), "%Y-%d-%m").date()
                    except ValueError as e:
                        print(e, week_date.year, f"\ndueDate: {dueDay:02d}\n", dueDateMonth, bill['name'])
                
                
            week_date = datetime.strptime(str(week_date), "%Y-%m-%d").date()
            week_date2 = datetime.strptime(str(week_date2), "%Y-%m-%d").date()
            '''if bill['name'] == 'DTE' and str(week_date) == '2025-01-03':
                print(dueDate, week_date, week_date2, bill['name'])'''
            if (dueDate >= week_date and dueDate <= week_date2) or past_due:
                due_date_text = dueDate.strftime('%a %b %d')
                if bill["frequency"] == "weekly":
                    due_date_text = 'Weekly'
                bill_list.append(create_bill_item(bill, due_date_text, isEditable, week_date, past_due))
                bills_total_amount+=float(bill['amount'].replace('$', '').replace(',', ''))
            
            

        if bills_total_amount>0:
                bill_list.append(ft.Container(
                    content=ft.Row(controls=[ft.Text(f"Total: ", size=18, color=current_theme["list_item_colors"]["total_amount_title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Row(expand=True), ft.Row(controls=[ft.IconButton(ft.icons.CALCULATE, icon_color=current_theme["list_item_colors"]["total_amount_icon_color"], on_click=lambda e: toggle_calc_bottom_sheet(bills_total_amount)),ft.Text(f"${bills_total_amount:.2f}", size=18, color=current_theme["list_item_colors"]["total_amount_text_color"])])], expand=True),
                    margin=ft.margin.all(10),
                    border=ft.border.all(2, color=current_theme["list_item_colors"]["total_amount_border_color"]),
                    bgcolor=current_theme["list_item_colors"]["total_amount_background_color"],
                    border_radius=ft.border_radius.all(5),
                    padding=ft.padding.all(10),
                ))
        return ft.Column(controls=bill_list, spacing=2)
    
    chosen_pay = ft.Text()
    total_due = ft.Text()
    total_after_bills_paid = ft.Text()
    def update_chosen_pay(e):
        print(selected_total_bills_amount)
        pay = float(e.split('$')[1].replace(',', ''))
        chosen_pay.value = pay
        total_bills_due = float(total_due.value)
        total_after_bills_paid.value = f"{pay - total_bills_due:.2f}"
        page.update()

    
    
    data = get_bills(page, user_id, BASE_URL)
    if data['error'] is None or data['error'] == "":
        profile_pic = data["profile_pic"]
        user_pay_hours = data["user_pay_hours"]
        my_bills = data["my_bills"]
        unpaid_bills = data["unpaid_bills"]
    else:
        print(data['error'])
        
    dd = ft.Dropdown(
        width=100,
        options=user_pay_hours,
        label="Pay Options",
        on_change=lambda e: update_chosen_pay(e.control.value),
        color=current_theme["calc_theme"]["dropdown_text"],
        bgcolor=current_theme["calc_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_border_color"],
        icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    chosen_pay=ft.Text(f"{dd.value if dd.value else '0.00'}", size=18, color=current_theme['calc_theme']['text'])
    total_due=ft.Text(f"{dd.value if dd.value else '0.00'}", size=18, color=current_theme['calc_theme']['text'])
    total_after_bills_paid=ft.Text(f"{dd.value if dd.value else '0.00'}", size=18, color=current_theme['calc_theme']['text'])
    calc_bottom_sheet = ft.Container(
        content=ft.Container(
            content=ft.ListView([
                dd,
                ft.Row(controls=[ft.Text("Chosen Pay: $", size=18, color=current_theme['calc_theme']['text_title'],style=ft.TextStyle(weight=ft.FontWeight.BOLD)),chosen_pay], expand=True, alignment=ft.MainAxisAlignment.CENTER, ),
                ft.Row(controls=[ft.Text("Total Bills Due: $", size=18, color=current_theme['calc_theme']['text_title'],style=ft.TextStyle(weight=ft.FontWeight.BOLD)),total_due], expand=True, alignment=ft.MainAxisAlignment.CENTER,),
                ft.Row(controls=[ft.Text("Total After Bills Paid: $", size=18, color=current_theme['calc_theme']['text_title'],style=ft.TextStyle(weight=ft.FontWeight.BOLD)),total_after_bills_paid], expand=True, alignment=ft.MainAxisAlignment.CENTER,),
                ],
                expand=False,
                spacing=10,
            ),
            bgcolor=current_theme['bottom_sheet']['background_color'],
            border=None,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, right=10, top=0, bottom=0),
            alignment=ft.alignment.bottom_center,
            width=400,
            height=300,
            expand=False
        ),
    visible=False,
    bottom=0,
    left=10,
    right=10,
    )

    
    weekly_bill_lists = []
    if len(unpaid_bills) > 0:
        edit_button = ft.IconButton(ft.icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e))
        save_button = ft.IconButton(ft.icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e), visible=False)
            
        weekly_bill_lists.append(
            ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(controls=[
                                ft.Text("Past Due", size=22, color=current_theme['list_item_colors']['title_color'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                        ft.Container(
                                            expand=True,),
                                        edit_button,save_button],
                                        expand=True),
                            margin=ft.margin.only(left=10, top=10, right=10),
                        ),
                        ft.Card(
                            content=ft.Container(content=build_bill_list(unpaid_bills.copy(), datetime.today(), past_due=True, isEditable=True)),
                            color=current_theme['list_item_colors']['inner_container'],
                            ),
                        
                    ]
                ),
                color=current_theme['list_item_colors']['base'],
            )
        )
    
    for index, week_date in enumerate(weekly_dates):
        edit_button = ft.Container()
        isEditable = False
        if index == 0:
            edit_button = ft.IconButton(ft.icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: edit_bill_list(e))
            save_button = ft.IconButton(ft.icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: edit_bill_list(e), visible=False)
            isEditable = True
        weekly_bill_lists.append(
            ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(controls=[
                                ft.Text(f"{week_date.strftime('%A, %b %d %Y')}", size=22, color=current_theme['list_item_colors']['title_color'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                        ft.Container(
                                            expand=True,),
                                        edit_button,save_button],
                                        expand=True),
                            margin=ft.margin.only(left=10, top=10, right=10),
                        ),
                        ft.Card(
                            content=ft.Container(content=build_bill_list(my_bills.copy(), week_date, past_due=False, isEditable=isEditable)),
                            color=current_theme['list_item_colors']['inner_container'],
                            ),
                        
                    ]
                ),
                color=current_theme['list_item_colors']['base'],
            )
        )

    bill_list = ft.ListView(controls=weekly_bill_lists,expand=1, spacing=10, padding=ft.padding.only(left=5, right=5, top=10, bottom=10))
    
    bill_list_button = ft.Column(
        controls=[ft.Image(src="/receipt_long.png", width=25, height=25, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Bills", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    charts_button = ft.Column(
        controls=[ft.Icon(name=ft.icons.TRENDING_UP,color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Charts", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    payments_button = ft.Row(
        controls=[ft.Image(src="/payments.png", width=25, height=25, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Earnings", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        #horizontal_alignment="center",
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
    
    menu_button = ft.Column(
        controls=[ft.Image(src="/menu.png", width=25, height=25, color=current_theme["bottom_navigation_colors"]["icon"]),
                  ft.Text("Menu", size=12, color=current_theme["bottom_navigation_colors"]["text"], style=ft.TextStyle(weight=ft.FontWeight.BOLD))],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )
    
    
    
    bottom_sheet = ft.Container(
        content=ft.Container(
            content=ft.ListView([
                ft.ElevatedButton(content=payments_button, expand=True, on_click=lambda _: page.go("/pay"), bgcolor=current_theme['bottom_sheet']['button_color']),
                ft.ElevatedButton("Setings", icon=ft.icons.SETTINGS, width=400, color=current_theme['bottom_sheet']['button_text_color'], expand=True, on_click=lambda _: page.go("/settings"), bgcolor=current_theme['bottom_sheet']['button_color']),
                ft.ElevatedButton("Log Out", icon=ft.icons.LOGOUT, width=400, color=current_theme['bottom_sheet']['button_text_color'], expand=True, on_click=lambda _: page.go("/"), bgcolor=current_theme['bottom_sheet']['button_color']),
                ],
                expand=False,
                spacing=10,
            ),
            bgcolor=current_theme['bottom_sheet']['background_color'],
            border=None,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, right=10, top=0, bottom=0),
            alignment=ft.alignment.bottom_center,
            width=400,
            expand=False
        ),
    visible=False,
    bottom=0,
    left=10,
    right=10,
    )

    def toggle_calc_bottom_sheet(e):
        total_due.value = f"{e:.2f}"
        chosen_pay.value = "0.00"
        total_after_bills_paid.value = "0.00"
        dd.value = None

        if bottom_sheet.visible:
            bottom_sheet.visible = False
        if calc_bottom_sheet.visible:
            calc_bottom_sheet.visible = False
        else:
            calc_bottom_sheet.visible = True
        page.update()
    
    def toggle_bottom_sheet(e):
        if calc_bottom_sheet.visible:
            calc_bottom_sheet.visible = False
        elif bottom_sheet.visible:
            bottom_sheet.visible = False
        else:
            bottom_sheet.visible = True
        page.update()

    def go_to_page(e):
        show_loader(page, loader)
        if e == "edit_bills":
            page.go("/edit_bills")
        elif e == "charts":
            page.go("/charts")

    bottom_appbar = ft.BottomAppBar(
        bgcolor=current_theme["bottom_navigation_colors"]["background"],
        shape=ft.NotchShape.CIRCULAR,
        elevation=10,
        content=ft.Row(
            controls=[
                ft.Container(content=bill_list_button,expand=True, on_click=lambda _: bill_list.scroll_to(0)),
                #ft.Container(expand=True),
                ft.Container(content=charts_button,expand=True, on_click=lambda _: go_to_page("charts")),
                #ft.Container(expand=True),
                #ft.Container(content=payments_button,expand=True, on_click=lambda _: page.go("/pay")),
                #ft.Container(expand=True),
                ft.Container(content=edit_bills_button,expand=True, on_click=lambda _: go_to_page("edit_bills")),
                #ft.Container(expand=True),
                ft.Container(content=menu_button,expand=True, on_click=lambda _: toggle_bottom_sheet(None)),
                
            ]
        ),
    )
    if profile_pic:
        appbar = ft.AppBar(leading=ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"], actions=[ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))])
    else:
        appbar = ft.AppBar(leading=ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    
    page.views.append(ft.View(
            "/bills",
            padding=ft.padding.all(0),
            controls=[ft.Stack(
                controls=[
                    ft.Container(content=bill_list,
                             bgcolor=current_theme['background'], 
                             padding=ft.padding.all(0),
                             margin=ft.margin.all(0),
                             expand=True,
                             ),
                             bottom_sheet,
                             calc_bottom_sheet,
                            ],
                            expand=True,
                        )
            ],
            appbar=appbar,
            bottom_appbar=bottom_appbar,
        )
    )