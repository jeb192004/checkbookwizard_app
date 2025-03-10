import flet as ft
import asyncio

from data.data_sync import DataSync
from ui.alert import create_loader, show_loader, hide_loader
from data.utils import navigate_to
from ui.charts_page.charts_check_list import create_check_list
from ui.my_controls import EarningsDropdown, NoDataInfo

my_bills = []
column_size = {"sm": 6, "md": 6, "lg":6, "xl": 6}

def charts_page(current_theme, page:ft.Page, BASE_URL:str):
    ds = DataSync(page, BASE_URL)
    loader=create_loader(page)
    pie_chart_container = ft.Container()
    colors = [
    ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN, ft.Colors.YELLOW,
    ft.Colors.PINK, ft.Colors.PURPLE, ft.Colors.TEAL,
    ft.Colors.CYAN, ft.Colors.INDIGO, ft.Colors.LIME, ft.Colors.AMBER,
    ft.Colors.BROWN, ft.Colors.GREY, ft.Colors.AMBER, ft.Colors.LIGHT_BLUE,
    ft.Colors.LIGHT_GREEN, ft.Colors.ORANGE, ft.Colors.GREEN_300, ft.Colors.TEAL_700, 
    ft.Colors.YELLOW_300,
    ft.Colors.BLACK45, ft.Colors.GREY_500, ft.Colors.BLUE_GREY

    ]
    
    normal_radius = 100
    hover_radius = 120
    normal_title_style = ft.TextStyle(
        size=0, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD,
    )
    hover_title_style = ft.TextStyle(
        size=22,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
    )
    
    bills_column = ft.Column(controls=[], expand=True)

    def create_chart_items(chart_type, chart, monthly_pay, my_bills):
        total_bills = 0
        total_bill_percentage = 0
        index=0
        all_bills = bills_column.controls
        for bill in all_bills:
            if "row" in str(bill):
                b_item = bill.controls
                bill_name=b_item[0].controls[0].value
                bill_amount=b_item[0].controls[1].value
                isChecked = b_item[-1].value
                if isChecked:
                    total_bills += float(bill_amount.replace('$', ''))
                    bill_percentage = round((float(bill_amount.replace('$', '').replace(',', '')) / (monthly_pay)) * 100, 2)
                    total_bill_percentage += bill_percentage
                    #print(total_bill_percentage)
                    if chart_type == "pie_chart":
                        chart.sections.append(
                            ft.PieChartSection(
                            bill_percentage,
                            title=f"{bill_name}\n${float(bill_amount.replace('$', '').replace(',', '')):,.2f}",
                            title_style=normal_title_style,
                            color=colors[index],
                            radius=normal_radius,
                            ),
                        )
                    index+=1
        return total_bills, total_bill_percentage, chart

    total_bills_text=ft.Text("Total Bills: $0.00", size=18, color=current_theme['calc_theme']['text'])

    def create_pie_chart_from_pay(pie_chart, monthly_pay, my_bills):
        total_bills,total_bill_percentage, pie_chart = create_chart_items("pie_chart", pie_chart, monthly_pay, my_bills)
        pie_chart.sections.append(
                ft.PieChartSection(
                100 - total_bill_percentage,
                title=f"Left over\n${monthly_pay - total_bills:,.2f}",
                title_style=normal_title_style,
                color=ft.Colors.GREEN,
                radius=normal_radius,
            ),
        )
        total_bills_text.value = f"Total Bills: ${total_bills:,.2f}"
        pie_chart_container.content = pie_chart

    pie_chart = ft.PieChart(
            sections_space=0,
            center_space_radius=40,
            expand=True,
        )
    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(pie_chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        pie_chart.update()

    pie_chart.on_chart_event=on_chart_event


    earnings_dropdown = ft.Dropdown()
    chosen_pay=ft.Text(f"{earnings_dropdown.value if earnings_dropdown.value else 'Monthly Earnings: $0.00'}", size=18, color=current_theme['calc_theme']['text'])
    def update_chosen_pay(e):
            #print(e)
            #selected_item_column=page.get_control(e.value).content.content.controls
            #selected_item_title=selected_item_column[0].controls[0].value
            #selected_item_amount=selected_item_column[1].controls[1].value
            #print(selected_total_bills_amount, selected_item_amount)
            #earnings_dropdown.value=selected_item_title
            selected_item_amount=e.data
            monthly_pay = float(selected_item_amount.replace('$', "").replace(',', ''))*4
            chosen_pay.value = f"Monthly Earnings: ${monthly_pay:,.2f}"
            pie_chart.sections = []
            create_pie_chart_from_pay(pie_chart, monthly_pay, my_bills)
            page.update()

    earnings_dropdown = ft.Dropdown(
            width=300,
            label="Earnings",
            on_change=lambda e: update_chosen_pay(e),
            color=current_theme["calc_theme"]["dropdown_text"],
            bgcolor=current_theme["calc_theme"]["dropdown_background"],
            border_color=current_theme["calc_theme"]["dropdown_border_color"],
            #select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
        )

    
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: navigate_to(page, loader, "/bills")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    
    weekly_explanation=ft.Text("Items that are marked for weekly pay are multiplied by 4", size=12, color=current_theme['calc_theme']['text'])
    
    earnings_pie_column = ft.Row(controls=[ft.Column(controls=[earnings_dropdown,chosen_pay,total_bills_text,pie_chart_container, weekly_explanation],
                                    expand=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)], col=column_size, expand=True, alignment=ft.MainAxisAlignment.CENTER)
    

    page.views.append(ft.View(
        "/charts",
                    [ft.Stack(
                        
                        controls=[ft.Column(controls=[
                            ft.ResponsiveRow(controls=[earnings_pie_column, ft.Container(content=bills_column, padding=ft.padding.only(left=10, right=10), col=column_size)],
                                              #expand=True, 
                                              alignment=ft.MainAxisAlignment.CENTER,
                                              
                                              ),
                            ],
                            #expand=True,
                            horizontal_alignment="center"
                            ),
                            
                            ]
                    )
                        
                    ],
                appbar=appbar,
                bgcolor=current_theme["background"],
                scroll=ft.ScrollMode.ADAPTIVE,
                )
    )

    async def build_bill_list():
        data = await ds.get_bill_list()
        if data["error"] is not None or data["error"] != "":
            profile_pic=None
            if "profile_pic" in data:
                profile_pic = data["profile_pic"]
            earnings_data = await ds.get_earnings()
            if earnings_data["error"] is None:
                if "data" in earnings_data:
                    #print(earnings_data["data"])
                    if len(earnings_data["data"]["income"])>0:
                        for earnings in earnings_data["data"]["income"]:
                            if earnings["amount"] is None:
                                bills_column.controls.append(NoDataInfo("earnings"))
                            else:
                                earnings_dropdown.options.append(EarningsDropdown(title=earnings["title"], hours=earnings["hours"], amount=earnings["amount"]))
                    else:
                        bills_column.controls.append(NoDataInfo("earnings"))
            else:
                bills_column.controls.append(NoDataInfo("earnings"))
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()
            if "data" in data:
                data=data["data"]
                if data is not None:
                    #print(data)
                    if len(data["bills"])>0:
                        create_check_list(page, data["bills"], bills_column, current_theme=current_theme)
                        return data["bills"]
                    else:
                        bills_column.controls.append(NoDataInfo("bills"))
                else:
                    bills_column.controls.append(NoDataInfo("bills"))
            else:
                bills_column.controls.append(NoDataInfo("bills"))
        else:
            print(data["error"])
    
    my_bills = asyncio.run(build_bill_list())
    
