import flet as ft

def create_check_list(page: ft.Page, bills, bills_column: ft.Column, current_theme):
    for bill in bills:
        amount=bill["amount"]
        if bill["frequency"]=="weekly":
            amount=f"{float(bill['amount'].replace('$', '').replace(',', ''))*4:.2f}"
            
        bills_column.controls.append(ft.Row([
            ft.Column(controls=[ft.Text(value=bill["name"], style=ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["header_text_color"],color=current_theme["header_text_color"])), ft.Text(value=amount, color=current_theme["text_color"])]),
            ft.Row(expand=True),
            ft.Checkbox(value=True)
        ]))
        bills_column.controls.append(ft.Divider(color=current_theme["border_color"]))
    page.update()