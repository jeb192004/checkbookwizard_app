import flet as ft

from data.bills import get_bills
from ui.alert import create_loader, show_loader, hide_loader


def charts_page(current_theme, page:ft.Page, BASE_URL:str, user_id:str):
    #bills = Bills(page, BASE_URL)
    loader = create_loader(page)
    pie_chart_container = ft.Container()
    colors = [
    ft.colors.RED, ft.colors.BLUE, ft.colors.GREEN, ft.colors.YELLOW,
    ft.colors.ORANGE, ft.colors.PINK, ft.colors.PURPLE, ft.colors.TEAL,
    ft.colors.CYAN, ft.colors.INDIGO, ft.colors.LIME, ft.colors.AMBER,
    ft.colors.BROWN, ft.colors.GREY, ft.colors.AMBER, ft.colors.LIGHT_BLUE,
    ft.colors.LIGHT_GREEN, ft.colors.GREEN_300, ft.colors.TEAL_700, ft.colors.YELLOW_300

    ]
    
    normal_radius = 100
    hover_radius = 120
    normal_title_style = ft.TextStyle(
        size=0, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
    )
    hover_title_style = ft.TextStyle(
        size=22,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
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
                color=ft.colors.ORANGE,
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

    data = get_bills(page, user_id, BASE_URL)
    if data['error'] is None or data['error'] == "":
        profile_pic = data["profile_pic"]
        user_pay_hours = data["user_pay_hours"]
        my_bills = data["my_bills"]
        unpaid_bills = data["unpaid_bills"]

        
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
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Earnings"), title_size=40),
            bottom_axis=ft.ChartAxis(labels_size=0, title=ft.Text("Bills"), title_size=40),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=max_y_graph,
            interactive=True,
            expand=True,
            )
        


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
            options=user_pay_hours,
            label="Earnings",
            on_change=lambda e: update_chosen_pay(e.control.value),
            color=current_theme["calc_theme"]["dropdown_text"],
            bgcolor=current_theme["calc_theme"]["dropdown_background"],
            border_color=current_theme["calc_theme"]["dropdown_border_color"],
            icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
        )

        

        
    else:
        print(data['error'])
        

    def go_back(_):
        show_loader(page, loader)
        page.go("/bills")
    
    if profile_pic:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: go_back(_)),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"], actions=[ft.Container(content=ft.Image(src=profile_pic, width=40, height=40), border_radius=50, margin=ft.margin.only(right=10))])
    else:
        appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: go_back(_)),ft.Image(src=current_theme["top_appbar_colors"]["icon"], width=200, fit=ft.ImageFit.FIT_WIDTH)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    
    return ft.View(
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
                            #loader
                            ]
                    )
                        
                    ],
                appbar=appbar
                )