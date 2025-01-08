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