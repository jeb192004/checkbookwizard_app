import flet as ft
from ui.theme import light_theme, dark_theme, green_theme


current_theme = None
class InitMyControls(dict):
    def __init__(self,page):
        global current_theme
        self.page = page
        saved_theme = page.client_storage.get("burnison.me.current.theme")
        current_theme = None
        if saved_theme == "light" or saved_theme is None:
            current_theme = light_theme()
        elif saved_theme == "dark":
            current_theme = dark_theme()
        elif saved_theme == "green":
            current_theme = green_theme()


def focus(e):
    e.control.label_style = {"color": current_theme["text_field"]["label_color_focused"]}
    e.control.update()

def blur(e):
    if e.control.value == "" or e.control.value is None:
        e.control.label_style = {"color": current_theme["text_field"]["label_color"]}
    else:
        e.control.label_style = {"color": current_theme["text_field"]["label_color_focused"]}
    e.control.update()
    
class TextField(ft.TextField):
    def __init__(self, label, value, read_only=False, width=None, height=None, text_size=None, on_change=None, input_filter=None, prefix=None):
        super().__init__()
        self.label = label
        self.value = value
        self.read_only = read_only
        self.width = width
        self.height = height
        self.text_size = text_size
        self.label_style = {"color": current_theme["text_field"]["label_color_focused"]} if value else {"color": current_theme["text_field"]["label_color"]}
        self.color=current_theme["text_field"]["text_color"]
        self.border_color=current_theme["text_field"]["border_color"]
        self.bgcolor=current_theme["text_field"]["background_color"]
        self.border_width=1
        self.border_radius=5
        self.on_focus = lambda e: focus(e)
        self.on_blur = lambda e: blur(e)
        self.on_change = on_change
        self.input_filter = input_filter
        self.prefix = prefix
        
class ElevatedButton(ft.ElevatedButton):
    def __init__(self, text=None, icon=None, on_click=None, expand=False, bgcolor=None, color=None):
        super().__init__()
        self.text = text
        self.icon = icon
        self.bgcolor = bgcolor if bgcolor else current_theme["elevated_button"]['background']
        self.color = color if color else current_theme["elevated_button"]['text']
        self.on_click = on_click
        self.expand = expand
        self.icon_color = color if color else current_theme["elevated_button"]['icon_color']

class DeleteButton(ft.ElevatedButton):
    def __init__(self, on_click=None):
        super().__init__()
        self.text = "Delete"
        self.icon = ft.Icons.DELETE
        self.bgcolor = ft.Colors.RED
        self.color = ft.Colors.WHITE
        self.on_click = on_click

class Label(ft.Text):
    def __init__(self, text, size=None):
        super().__init__()
        self.text = text
        self.size = size
        self.color = current_theme["label"]["text"]
        self.style = ft.TextStyle(weight=ft.FontWeight.BOLD)

class Title(ft.Text):
    def __init__(self, value, size=None, color=None):
        super().__init__()
        self.value = value
        self.size = size
        self.color = color if color else current_theme["earnings_list_title_color"]
        self.style = ft.TextStyle(weight=ft.FontWeight.BOLD)

class Radio(ft.Container):
    def __init__(self, value, label):
        super().__init__()
        self.content = ft.Radio(value=value, label=label, fill_color=current_theme["radio"]["fill_color"], label_style={"color": current_theme["radio"]["label_color"]})
        self.bgcolor = current_theme["radio"]['background_color']
        self.border_radius=5
        self.border=ft.border.all(1,current_theme["radio"]["border_color"])
        self.padding=ft.padding.all(10)    

class BillItem(ft.Container):
    def __init__(self, b, past_due, website_onclick=None, phone_onclick=None, email_onclick=None):
        
        super().__init__()
        bill=b["bill"]
        checkbox = ft.Container()
        if b["isEditable"]:
            checkbox = ft.Checkbox(label="Paid", value=True, label_style=ft.TextStyle(color=current_theme["text_color"]), label_position=ft.LabelPosition.LEFT, data={"name": bill["name"], "payday": b["week_date"], "website":bill["website"], "phone":bill["phone"], "email":bill["email"], "frequency":bill["frequency"], "amount":bill["amount"], "due_date":bill["due_date"], "due":bill["due"]}, visible=False)
        if past_due:
            checkbox = ft.Checkbox(label="Paid", value=False, label_style=ft.TextStyle(color=current_theme["text_color"]), label_position=ft.LabelPosition.LEFT, data={"id": bill["id"]}, visible=False)
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
                    ft.TextSpan(website, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, overflow=None, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: self.page.launch_url(website)),])
        if phone:
            phone_row = ft.Text(size=15, spans=[ft.TextSpan("Phone: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                    ft.TextSpan(phone, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: page.launch_url(f"tel:{phone}")),])
        if email:
            email_row = ft.Text(size=15, spans=[ft.TextSpan("Email: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                    ft.TextSpan(email, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=lambda _: page.launch_url(f"mailto:{email}")),])
        self.content=ft.Column([
            ft.Row(controls=[ft.Text(bill["name"], size=20, color=current_theme["list_item_colors"]["bill_name_color"], style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Container(expand=True), checkbox],),
            ft.Row(controls=[ft.Row(spacing=1, controls=[ft.Text(f"DUE: ", size=bill_item_text_size, color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(b["due_date_text"], size=bill_item_text_size, color=bill_item_text_color)]),
                             ft.Row(expand=True),
                             ft.Row(spacing=1, controls=[ft.Text(f"Amount: ", size=bill_item_text_size,color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(f"{bill['amount']}", size=bill_item_text_size, color=bill_item_text_color)])],
                #expand=True,
                spacing=2),
            website_row,
            phone_row,
            email_row,
            ft.Divider(height=2, color=ft.Colors.BLACK),
            ],
            spacing=2,
        )
        self.margin=ft.margin.all(10)

class BillTotalDue(ft.Container):
    def __init__(self, bills_total_amount, toggle_click):
        super().__init__()
        self.content=ft.Row(controls=[ft.Text(f"Total: ", size=18, color=current_theme["list_item_colors"]["total_amount_title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Row(expand=True), ft.Row(controls=[ft.IconButton(ft.Icons.CALCULATE, icon_color=current_theme["list_item_colors"]["total_amount_icon_color"], on_click=toggle_click),ft.Text(f"${bills_total_amount:.2f}", size=18, color=current_theme["list_item_colors"]["total_amount_text_color"])])], expand=True)
        self.margin=ft.margin.all(10)
        self.border=ft.border.all(2, color=current_theme["list_item_colors"]["total_amount_border_color"])
        self.bgcolor=current_theme["list_item_colors"]["total_amount_background_color"]
        self.border_radius=ft.border_radius.all(5)
        self.padding=ft.padding.all(10)

class EarningsDropdown(ft.DropdownOption):
    def __init__(self, title, hours, amount):
        super().__init__()
        self.content=ft.Container(content=ft.Column(controls=[
            ft.Row(controls=[Title(title),]),
            ft.Row(controls=[TextField(label="Hours", value=hours, width=75), TextField(label="Amount", value=amount, width=125)])
        ]),
        padding=ft.padding.all(10),
        margin=ft.margin.only(bottom=5, top=5),
        border_radius=10,
        bgcolor=current_theme["list_item_colors"]["inner_container"]
        )
        self.key=amount

class NoDataInfo(ft.Column):
    def __init__(self, type):
        super().__init__()
        if type == "bills":
            self.controls=[
                    ft.Row(controls=[ft.Text(value="You don't have any bills yet.\nPlease go to Edit Bills and add some bills.", color=current_theme["label"]["color"])]),
                    ft.Row(controls=[ElevatedButton(text="Go to Edit Bills page", on_click=lambda e: self.page.go("/edit_bills"))])
                ]
        if type == "earnings":
            self.controls=[
                    ft.Row(controls=[ft.Text(value="You don't have any Earnings yet.\nPlease go to the Earnings page and add some.", color=current_theme["label"]["color"])]),
                    ft.Row(controls=[ElevatedButton(text="Go to Earnings page", on_click=lambda e: self.page.go("/pay"))])
                ]