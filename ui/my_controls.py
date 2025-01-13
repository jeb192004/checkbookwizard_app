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
        self.color = current_theme["label"]["color"]
        self.style = ft.TextStyle(weight=ft.FontWeight.BOLD)

class Title(ft.Text):
    def __init__(self, value, size=None, color=None):
        super().__init__()
        self.value = value
        self.size = size
        self.color = color if color else current_theme["title_color"]
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
    def __init__(self, bill, due_date, isEditable, week_date, past_due, website_onclick=None, phone_onclick=None, email_onclick=None):
        super().__init__()
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
                    ft.TextSpan(website, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, overflow=None, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=website_onclick),])
        if phone:
            phone_row = ft.Text(size=15, spans=[ft.TextSpan("Phone: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                    ft.TextSpan(phone, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=phone_onclick),])
        if email:
            email_row = ft.Text(size=15, spans=[ft.TextSpan("Email: ",ft.TextStyle(weight=ft.FontWeight.BOLD ,decoration_color=current_theme["list_item_colors"]["text_color"],color=current_theme["list_item_colors"]["text_color"])),
                    ft.TextSpan(email, ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, decoration_color=current_theme["list_item_colors"]["link_color"], color=current_theme["list_item_colors"]["link_color"]), on_click=email_onclick),])
        self.content=ft.Column([
            ft.Row(controls=[ft.Text(bill["name"], size=20, color=current_theme["list_item_colors"]["bill_name_color"], style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Container(expand=True), checkbox],),
            ft.Row(controls=[ft.Row(controls=[ft.Text(f"DUE: ", size=bill_item_text_size, color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(f"{due_date}", size=bill_item_text_size, color=bill_item_text_color)]), ft.Row(expand=True),ft.Row(controls=[ft.Text(f"Amount: ", size=bill_item_text_size,color=current_theme["list_item_colors"]["title_color"],style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.Text(f"{bill['amount']}", size=bill_item_text_size, color=bill_item_text_color)])], expand=True),
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