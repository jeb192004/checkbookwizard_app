import flet as ft
import asyncio

from data.data_sync import get_bills
from ui.alert import create_loader, show_loader, hide_loader
from data.utils import navigate_to

my_bills = []

def charts_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    '''async def build_bill_list():
        data = await get_bills(page, user_id, BASE_URL)
        if data["error"] is not None or data["error"] != "":
            profile_pic = data["profile_pic"]
            user_pay_hours = data["user_pay_hours"]
            my_bills = data["my_bills"]
            unpaid_bills = data["unpaid_bills"]
            return {"profile_pic":profile_pic, "user_pay_hours":user_pay_hours, "my_bills":my_bills}
        else:
            print(data["error"])'''
    loader = create_loader(page)
    pie_chart_container = ft.Container()
    colors = [
    ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN, ft.Colors.YELLOW,
    ft.Colors.ORANGE, ft.Colors.PINK, ft.Colors.PURPLE, ft.Colors.TEAL,
    ft.Colors.CYAN, ft.Colors.INDIGO, ft.Colors.LIME, ft.Colors.AMBER,
    ft.Colors.BROWN, ft.Colors.GREY, ft.Colors.AMBER, ft.Colors.LIGHT_BLUE,
    ft.Colors.LIGHT_GREEN, ft.Colors.GREEN_300, ft.Colors.TEAL_700, ft.Colors.YELLOW_300

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

    def create_chart_items(chart_type, chart, monthly_pay, my_bills):
        total_bills = 0
        total_bill_percentage = 0
        for index, bill in enumerate(my_bills):
            total_bills += float(bill['amount'].replace('$', ''))
            '''chart.bar_groups.append(
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=float(bill['amount'].replace('$', '').replace(',', '')),
                            width=10,
                            color=colors[index],
                            tooltip=bill['name'],
                            border_radius=0,
                        ),
                    ],
                ),
            )'''
            bill_percentage = round((float(bill['amount'].replace('$', '').replace(',', '')) / (monthly_pay)) * 100, 2)
            total_bill_percentage += bill_percentage
            #print(total_bill_percentage)
            if chart_type == "pie_chart":
                chart.sections.append(
                    ft.PieChartSection(
                    bill_percentage,
                    title=f"{bill['name']}\n${float(bill['amount'].replace('$', '').replace(',', '')):,.2f}",
                    title_style=normal_title_style,
                    color=colors[index],
                    radius=normal_radius,
                    ),
                )
        return total_bills, total_bill_percentage, chart

    total_bills_text=ft.Text("Total Bills: $0.00", size=18, color=current_theme['calc_theme']['text'])

    def create_pie_chart_from_pay(pie_chart, monthly_pay, my_bills):
        total_bills,total_bill_percentage, pie_chart = create_chart_items("pie_chart", pie_chart, monthly_pay, my_bills)
        pie_chart.sections.append(
                ft.PieChartSection(
                100 - total_bill_percentage,
                title=f"Left over\n${monthly_pay - total_bills:,.2f}",
                title_style=normal_title_style,
                color=ft.Colors.ORANGE,
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
            monthly_pay = float(e.split('$')[1].replace(',', ''))*4
            chosen_pay.value = f"Monthly Earnings: ${monthly_pay:,.2f}"
            pie_chart.sections = []
            create_pie_chart_from_pay(pie_chart, monthly_pay, my_bills)
            page.update()

    earnings_dropdown = ft.Dropdown(
            width=300,
            #options=user_pay_hours,
            label="Earnings",
            on_change=lambda e: update_chosen_pay(e.control.value),
            color=current_theme["calc_theme"]["dropdown_text"],
            bgcolor=current_theme["calc_theme"]["dropdown_background"],
            border_color=current_theme["calc_theme"]["dropdown_border_color"],
            icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
        )


    '''data = asyncio.run(build_bill_list())
    if "error" not in data:
        profile_pic = data["profile_pic"]
        user_pay_hours = data["user_pay_hours"]
        my_bills = data["my_bills"]
        #unpaid_bills = data["unpaid_bills"]

        
        max_y_graph = 0
        fourty_hours_month = 0
        avg_hours_month = 0
        for p in user_pay_hours:
            if "40 Hours:" in p.key:
                fourty_hours_month = float(p.key.split('$')[1].replace(',', ''))*4
                print(fourty_hours_month)
            if "Average Pay:" in p.key:
                avg_hours_month = float(p.key.split('$')[1].replace(',', ''))*4
            print(p.key)
            pay = float(p.key.split('$')[1].replace(',', ''))
            if pay > max_y_graph:
                max_y_graph = pay

        chart = ft.BarChart(
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Earnings"), title_size=40),
            bottom_axis=ft.ChartAxis(labels_size=0, title=ft.Text("Bills"), title_size=40),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            max_y=max_y_graph,
            interactive=True,
            expand=True,
            )
        

        
    else:
        print(data['error'])
        navigate_to(page, loader, "/bills")
'''
    
    appbar = ft.AppBar(
            leading=ft.Image(
                src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN
            ),
            leading_width=200,
            bgcolor=current_theme["top_appbar_colors"]["background"],
            shadow_color=current_theme["shadow_color"],
        )

    page.views.append(ft.View(
        "/charts",
                    [ft.Stack(
                        
                        controls=[ft.Column(controls=[
                            earnings_dropdown,
                            chosen_pay,
                            total_bills_text,
                            #chart,
                            pie_chart_container

                            ],
                            expand=True,
                            horizontal_alignment="center",
                            scroll=ft.ScrollMode.ADAPTIVE),
                            
                            ]
                    )
                        
                    ],
                appbar=appbar,
                bgcolor=current_theme["background"]
                )
    )

    async def build_bill_list():
        data = await get_bills(page, user_id, BASE_URL)
        if data["error"] is not None or data["error"] != "":
            profile_pic = data["profile_pic"]
            user_pay_hours = data["user_pay_hours"]
            if user_pay_hours:
                earnings_dropdown.options = user_pay_hours
            #my_bills = data["my_bills"]
            #unpaid_bills = data["unpaid_bills"]
            if profile_pic:
                appbar_actions = [ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))]
                appbar.actions = appbar_actions
                page.update()
            return data["my_bills"]
        else:
            print(data["error"])
    
    my_bills = asyncio.run(build_bill_list())
    
