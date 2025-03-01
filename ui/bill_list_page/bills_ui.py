import flet as ft
import flet.ads as ads
from datetime import datetime, timedelta
import json
from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
from ui.bill_list_page.bill_list_item import create_bill_item
from data.utils import navigate_to
import asyncio
from ui.my_controls import ElevatedButton, InitMyControls, EarningsDropdown, NoDataInfo, BillItem
from ui.ads import Ads

selected_total_bills_amount = 0
column_size = {"sm": 6, "md": 6, "lg":4, "xl": 3}
unpaid_total=0

def bills_page(current_theme, page: ft.Page, BASE_URL: str):
    ad = Ads(page)
    ds = DataSync(page, BASE_URL)
    InitMyControls(page)
    loader = create_loader(page)
    page.bgcolor = current_theme["background"]
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)  # 365

    chosen_pay = ft.Text()
    total_due = ft.Text()
    total_after_bills_paid = ft.Text()

    dd = ft.Dropdown(
        width=100,
        label="Pay Options",
        label_style = {"color": current_theme["text_field"]["label_color"]},
        color=current_theme["calc_theme"]["dropdown_text"],
        bgcolor=current_theme["calc_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_background"],
        select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    def update_chosen_pay(e):
        selected_item_column=page.get_control(e.value).content.content.controls
        selected_item_title=selected_item_column[0].controls[0].value
        selected_item_amount=selected_item_column[1].controls[1].value
        #print(selected_total_bills_amount, selected_item_amount)
        dd.value=selected_item_title
        pay = float(selected_item_amount.replace("$", "").replace(",", ""))
        chosen_pay.value = pay
        total_bills_due = float(total_due.value)
        total_after_bills_paid.value = f"{pay - total_bills_due:.2f}"
        page.update()
        
    
    dd.on_change=lambda e: update_chosen_pay(e.control)

    
    chosen_pay = ft.Text(
        f"{dd.value if dd.value else '0.00'}",
        size=18,
        color=current_theme["calc_theme"]["text"],
    )
    total_due = ft.Text(
        f"{dd.value if dd.value else '0.00'}",
        size=18,
        color=current_theme["calc_theme"]["text"],
    )
    total_after_bills_paid = ft.Text(
        f"{dd.value if dd.value else '0.00'}",
        size=18,
        color=current_theme["calc_theme"]["text"],
    )
    calc_bottom_sheet = ft.Container(
        content=ft.Container(
            content=ft.ListView(
                [
                    dd,
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Chosen Pay: $",
                                size=18,
                                color=current_theme["calc_theme"]["text_title"],
                                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            chosen_pay,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Total Bills Due: $",
                                size=18,
                                color=current_theme["calc_theme"]["text_title"],
                                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            total_due,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Total After Bills Paid: $",
                                size=18,
                                color=current_theme["calc_theme"]["text_title"],
                                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            total_after_bills_paid,
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                expand=False,
                spacing=10,
            ),
            bgcolor=current_theme["bottom_sheet"]["background_color"],
            border=None,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, right=10, top=0, bottom=0),
            alignment=ft.alignment.bottom_center,
            width=400,
            height=300,
            expand=False,
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

    
    bill_list_button = ft.Column(
        controls=[
            ft.Image(
                src="/receipt_long.png",
                width=25,
                height=25,
                color=current_theme["bottom_navigation_colors"]["icon"],
            ),
            ft.Text(
                "Bills",
                size=12,
                color=current_theme["bottom_navigation_colors"]["text"],
                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
        ],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    charts_button = ft.Column(
        controls=[
            ft.Icon(
                name=ft.Icons.TRENDING_UP,
                color=current_theme["bottom_navigation_colors"]["icon"],
            ),
            ft.Text(
                "Charts",
                size=12,
                color=current_theme["bottom_navigation_colors"]["text"],
                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
        ],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    payments_button = ft.Row(
        controls=[
            ft.Image(
                src="/payments.png",
                width=25,
                height=25,
                color=current_theme["bottom_navigation_colors"]["icon"],
            ),
            ft.Text(
                "Earnings",
                size=12,
                color=current_theme["bottom_navigation_colors"]["text"],
                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
        ],
        spacing=2,
        expand=True,
        # horizontal_alignment="center",
        alignment="center",
    )

    edit_bills_button = ft.Column(
        controls=[
            ft.Image(
                src="/checkbook.png",
                width=25,
                height=25,
                color=current_theme["bottom_navigation_colors"]["icon"],
            ),
            ft.Text(
                "Edit",
                size=12,
                color=current_theme["bottom_navigation_colors"]["text"],
                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
        ],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    menu_button = ft.Column(
        controls=[
            ft.Image(
                src="/menu.png",
                width=25,
                height=25,
                color=current_theme["bottom_navigation_colors"]["icon"],
            ),
            ft.Text(
                "Menu",
                size=12,
                color=current_theme["bottom_navigation_colors"]["text"],
                style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
        ],
        spacing=2,
        expand=True,
        horizontal_alignment="center",
        alignment="center",
    )

    bottom_sheet = ft.Container(
        content=ft.Container(
            content=ft.ListView(
                [
                    ft.ElevatedButton(
                        content=payments_button,
                        expand=True,
                        on_click=lambda _: navigate_to(page, loader, "/pay"),
                        bgcolor=current_theme["bottom_sheet"]["button_color"],
                    ),
                    ElevatedButton(
                        text="Setings",
                        icon=ft.Icons.SETTINGS,
                        expand=True,
                        on_click=lambda _: navigate_to(page, loader, "/settings"),
                        bgcolor=current_theme["bottom_sheet"]["button_color"],
                        color=current_theme["bottom_sheet"]["button_text_color"],
                    ),
                    ElevatedButton(
                        "Log Out",
                        icon=ft.Icons.LOGOUT,
                        expand=True,
                        on_click=lambda _: ds.logout(),
                        bgcolor=current_theme["bottom_sheet"]["button_color"],
                        color=current_theme["bottom_sheet"]["button_text_color"],
                    ),
                ],
                expand=False,
                spacing=10,
            ),
            bgcolor=current_theme["bottom_sheet"]["background_color"],
            border=None,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, right=10, top=0, bottom=0),
            alignment=ft.alignment.bottom_center,
            width=400,
            expand=False,
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

    
    bottom_appbar = ft.BottomAppBar(
        bgcolor=current_theme["bottom_navigation_colors"]["background"],
        shadow_color=current_theme["shadow_color"],
        content=ft.Row(
            controls=[
                ft.Container(
                    content=bill_list_button,
                    expand=True,
                    #on_click=lambda _: bill_list.scroll_to(0),
                ),
                # ft.Container(expand=True),
                ft.Container(
                    content=charts_button,
                    expand=True,
                    on_click=lambda _: navigate_to(page, loader, "/charts"),
                ),
                # ft.Container(expand=True),
                # ft.Container(content=payments_button,expand=True, on_click=lambda _: page.go("/pay")),
                # ft.Container(expand=True),
                ft.Container(
                    content=edit_bills_button,
                    expand=True,
                    on_click=lambda _: navigate_to(page, loader, "/edit_bills"),
                ),
                # ft.Container(expand=True),
                ft.Container(
                    content=menu_button,
                    expand=True,
                    on_click=lambda _: toggle_bottom_sheet(None),
                ),
            ]
        ),
    )
    
    appbar = ft.AppBar(
            leading=ft.Image(
                src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN
            ),
            leading_width=200,
            bgcolor=current_theme["top_appbar_colors"]["background"],
            shadow_color=current_theme["shadow_color"],
        )

    bill_list_container_padding=ft.padding.only(top=55, left=5, right=5, bottom=0) if page.platform==ft.PagePlatform.ANDROID or page.platform==ft.PagePlatform.IOS else ft.padding.only(top=5, left=5, right=5, bottom=0)
    bill_list_container = ft.ListView(
            #bgcolor=current_theme["background"],
            padding=bill_list_container_padding,
            #margin=ft.margin.all(0),
            expand=True,
            #alignment=ft.alignment.top_center,
        )
    
    banner_ad = ad.banner_ad()
    #print(banner_ad.content)
    bill_stack = ft.Stack(
                    controls=[
                        bill_list_container,
                        banner_ad,
                        bottom_sheet,
                        calc_bottom_sheet,
                    ],
                    expand=True,
                )
    
    page.views.append(
        ft.View(
            "/bills",
            padding=ft.padding.all(0),
            #scroll=True,
            controls=[
                bill_stack
            ],
            appbar=appbar,
            bottom_appbar=bottom_appbar,
        )
    )


    def save_unpaid(e):
        selected = []
        bill_list = e.control.parent.parent.parent.controls[1].content.controls
        for bill in bill_list:
            if "row" not in str(bill.content):
                c_box = bill.content.controls[0].controls[2]
                if c_box.visible ==True:
                    c_box.visible = False
                else:
                    c_box.visible = True
                if c_box.value == False:
                    selected.append(c_box.data)
        if e.control.icon == "edit":
            e.control.icon = ft.Icons.SAVE
        elif e.control.icon == "save":
            e.control.icon = ft.Icons.EDIT
        if len(selected)>0:
            #print(selected)
            show_loader(page, loader)
            response = ds.save_unpaid_bills(selected)
            page.go("/refresh_bills")
            
            selected = []
            hide_loader(page, loader)
        page.update()

    def remove_unpaid(e):
        selected = []
        controls_to_remove = []
        bill_list = e.control.parent.parent.parent.controls[1].content.controls
        for bill in bill_list:
            if "row" not in str(bill.content):
                c_box = bill.content.controls[0].controls[2]
                if c_box.visible ==True:
                    c_box.visible = False
                else:
                    c_box.visible = True
                if c_box.value == True:
                    controls_to_remove.append(bill)
                    selected.append(c_box.data["id"])
        if e.control.icon == "edit":
            e.control.icon = ft.Icons.SAVE
        elif e.control.icon == "save":
            e.control.icon = ft.Icons.EDIT
        if len(selected)>0:
            show_loader(page, loader)
            response=ds.remove_unpaid_bills(selected)
            page.go("/refresh_bills")
            selected = []
            hide_loader(page, loader)
        
        page.update()

    


    async def build_bill_list():
        show_loader(page, loader)
        data = await ds.get_bills()
        if data["error"] is not None or data["error"] != "":
            bill_data=data["data"]
            if bill_data["bills"]:
                weekly_bill_lists=[]
                for index, bill in enumerate(bill_data["bills"]):
                    bill_controls=[]
                    isPastDue=bill["past_due"]
                    for b in bill["bills"]:
                        bill_controls.append(BillItem(b, isPastDue, website_onclick=lambda _: page.launch_url(b["website"]), phone_onclick=lambda _: page.launch_url(f"tel:{b['phone']}"), email_onclick=lambda _: page.launch_url(f"mailto:{b['email']}")),)
                    date=bill["week_date"]
                    date_object = datetime.strptime(date, "%Y-%m-%d").date()
                    date_text = date_object.strftime("%b. %d, %Y")
                    if isPastDue:
                        date_text="Unpaid"
                    edit_button = ft.Container()
                    isEditable = bill["isEditable"]
                    if isEditable:
                        edit_button = ft.IconButton(ft.Icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: save_unpaid(e))
                        save_button = ft.IconButton(ft.Icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: save_unpaid(e), visible=False)
                    if isPastDue:
                        edit_button = ft.IconButton(ft.Icons.EDIT, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e))
                        save_button = ft.IconButton(ft.Icons.SAVE, bgcolor=current_theme['list_item_colors']['icon_color'], on_click=lambda e: remove_unpaid(e), visible=False)
    
                    weekly_bill_lists.append(
                        ft.Card(
                            col=column_size,
                            shadow_color=ft.Colors.WHITE,
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(controls=[
                                            ft.Text(f"{date_text}", size=22, color=current_theme['list_item_colors']['title_color'], style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                            ft.Container(
                                                expand=True,),
                                            edit_button,save_button],
                                            expand=True),
                                        margin=ft.margin.only(left=10, top=10, right=10),
                                    ),
                                    ft.Card(
                                        content=ft.Column(controls=bill_controls, spacing=2),
                                        color=current_theme['list_item_colors']['inner_container'],
                                    ),
                                ]),
                                color=current_theme['list_item_colors']['base'],
                        )
                    )
                    #print("\n------\n", bill, "\n")
                    
                bill_list = ft.ResponsiveRow(controls=weekly_bill_lists, spacing=10)
                bill_list_container.controls = [ft.Column(controls=[bill_list], expand=True, scroll=True)]
                page.update()
            '''profile_pic=None
            day_of_week=5
            if "profile_pic" in data:
                profile_pic = data["profile_pic"]
            if "day_of_week" in data:
                day_of_week=data["day_of_week"]
            earnings_data = await ds.get_earnings()
            #print(earnings_data)
            if earnings_data["error"] is None and earnings_data["data"][0]["amount"] is not None:
                for earnings in earnings_data["data"]:
                    dd.options.append(EarningsDropdown(title=earnings["title"], hours=earnings["hours"], amount=earnings["amount"]))
            if "my_bills" in data:
                my_bills = data["my_bills"]
                unpaid_bills = data["unpaid_bills"]
                
                create_bill_item(page, current_theme, loader, BASE_URL, toggle_calc_bottom_sheet, bill_list_container, ds, day_of_week, my_bills, unpaid_bills)
            else:
                bill_list_container.content=NoDataInfo("bills")
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()'''
            hide_loader(page, loader)
        else:
            print(data["error"])
            hide_loader(page, loader)
        
        
    asyncio.run(build_bill_list())
    
