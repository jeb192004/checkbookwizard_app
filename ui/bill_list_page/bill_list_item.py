import flet as ft
from datetime import datetime, date, timedelta
from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
from ui.my_controls import BillItem, BillTotalDue
from data.utils import day_of_week_to_day_of_month

column_size = {"sm": 6, "md": 6, "lg":4, "xl": 3}
unpaid_total=0




def create_bill_item(page, current_theme, loader, BASE_URL, toggle_calc_bottom_sheet, bill_list_container, ds:DataSync, day_of_week, my_bills, unpaid_bills):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)#365
    
    weekly_bill_lists = []
    edit_button = ft.IconButton(ft.Icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e))
    save_button = ft.IconButton(ft.Icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e), visible=False)
    unpaid_bills_container = ft.Container()
    unpaid_card = ft.Card(
        col=column_size,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(controls=[
                        ft.Text("Unpaid", size=22, color=current_theme['list_item_colors']['title_color'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                        ft.Container(expand=True,),
                        edit_button,save_button],
                        expand=True),
                    margin=ft.margin.only(left=10, top=10, right=10),
                ),
                ft.Card(
                    content=unpaid_bills_container,
                    color=current_theme['list_item_colors']['inner_container'],
                ),
                        
                ]
        ),
        color=current_theme['list_item_colors']['base'],
        expand_loose=True,
        visible=False
    )
    weekly_bill_lists.append(unpaid_card)

    
    def remove_unpaid(e):
        selected = []
        controls_to_remove = []
        bill_list = e.control.parent.parent.parent.controls[1].content.content.controls
        for bill in bill_list:
            if "row" not in str(bill.content):
                c_box = bill.content.controls[0].controls[2]
                if c_box.visible ==True:
                    c_box.visible = False
                else:
                    c_box.visible = True
                if c_box.value == True:
                    controls_to_remove.append(bill)
                    '''for m_bill in my_bills:
                        if m_bill["id"] == c_box.data["bill_id"]:
                            m_bill["payday"] = c_box.data["payday"].strftime("%Y-%m-%d")'''
                    selected.append({"id":c_box.data["bill_id"], "payday": c_box.data["payday"].strftime("%Y-%m-%d")})
        if e.control.icon == "edit":
            e.control.icon = ft.Icons.SAVE
        elif e.control.icon == "save":
            e.control.icon = ft.Icons.EDIT
        if len(selected)>0:
            show_loader(page, loader)
            ds.remove_unpaid_bills(selected)
            page.go("/refresh_bills")
            '''for control in controls_to_remove:
                unpaid_bills_list = unpaid_bills_container.content.controls
                total_text = unpaid_bills_list[-1].content.controls[2].controls[-1]
                total_unpaid_value = float(total_text.value.replace("$","").replace(",",""))
                unpaid_amount_remove = float(control.content.controls[1].controls[-1].controls[-1].value.replace("$","").replace(",",""))
                new_total = total_unpaid_value-unpaid_amount_remove
                total_text.value=f"${new_total:.2f}"
                bill_list.remove(control)'''
            selected = []
            hide_loader(page, loader)
        
        page.update()

    
    
    def get_weekly_dates(start_date, day_of_week, end_date):
        day_of_week=day_of_week if day_of_week!=0 else 7
        current = start_date.replace()
        #print(day_of_week)
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
    weekly_dates = get_weekly_dates(start_date, day_of_week, end_date)

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
            due_date_text=None
            dueDate = None
            due = bill['due']
            if bill["frequency"] == "weekly":
                due = week_date.day
            elif bill["frequency"] == "single":
                due = bill["due_date"]
            elif bill["frequency"] == "monthly" and past_due == False:
                if  len(due) > 2:
                    #print(due)
                    
                    #print(occurrence, due_date_text)
                    #dueDate = getWeekdayOfMonth(year, month, week_date, weekdayIndex, occurrence)
                    dueDate, due_date_text, unused_due = day_of_week_to_day_of_month(due=due, current_date=week_date)
                    #print(dayOfMonth, due)
            if bill["frequency"] == "single":
                dueDate = due
            elif dueDate is None:
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
                
            if month != month2 and dueDate.day <= 6 and dueDate<week_date2:
                #print(dueDate, 'duedate', week_date2)
                
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
            #if bill['name'] == 'Credit Card':# and str(week_date) == '2025-02-07':
                #print(f"displayed date - {week_date} >= due date: {dueDate} <= {week_date2}(next week), {bill['name']}, {due_date_text}")
            if (dueDate >= week_date and dueDate <= week_date2) or past_due:
                #if bill['name'] == 'Truck Insurance':# and str(week_date) == '2025-02-07':
                    #print(f"displayed date - {week_date} >= due date: {dueDate} <= {week_date2}(next week), {bill['name']}, {due_date_text}")
            
                if due_date_text is None:
                    due_date_text = dueDate.strftime('%a %b %d')
                if bill["frequency"] == "weekly":
                    due_date_text = 'Weekly'
                bill_list.append(BillItem(bill, due_date_text, isEditable, week_date, past_due, website_onclick=lambda _: page.launch_url(bill["website"]), phone_onclick=lambda _: page.launch_url(f"tel:{bill['phone']}"), email_onclick=lambda _: page.launch_url(f"mailto:{bill['email']}")))
                bills_total_amount+=float(bill['amount'].replace('$', '').replace(',', ''))
            
            

        if bills_total_amount>0:
                unpaid_total = bills_total_amount
                bill_list.append(BillTotalDue(unpaid_total, toggle_click=lambda e: toggle_calc_bottom_sheet(bills_total_amount)))
        return ft.Column(controls=bill_list, spacing=2)
    
    
    if len(unpaid_bills) > 0:
        unpaid_bills_container.content = build_bill_list(unpaid_bills.copy(), datetime.today(), past_due=True, isEditable=True)
        unpaid_card.visible = True

    for index, week_date in enumerate(weekly_dates):
        edit_button = ft.Container()
        isEditable = False
        if index == 0:
            edit_button = ft.IconButton(ft.Icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: edit_bill_list(e))
            save_button = ft.IconButton(ft.Icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: edit_bill_list(e), visible=False)
            isEditable = True
        weekly_bill_lists.append(
            ft.Card(
                col=column_size,
                shadow_color=ft.Colors.WHITE,
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
    
    bill_list = ft.ResponsiveRow(controls=weekly_bill_lists, spacing=10)
    #bill_list = ft.ListView(controls=weekly_bill_lists,expand=1, spacing=10, padding=ft.padding.only(left=5, right=5, top=10, bottom=10))
    bill_list_container.controls = [ft.Column(controls=[bill_list], expand=True, scroll=True)]
    
    page.update()
    