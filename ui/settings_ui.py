import asyncio
import flet as ft
from ui.theme import light_theme, dark_theme, green_theme
from data.utils import navigate_to
from ui.alert import create_loader, show_loader, hide_loader
from data.data_sync import DataSync
def settings_page(current_theme, page:ft.Page, BASE_URL):
    ds = DataSync(page, BASE_URL)
    loader = create_loader(page)
    appbar = ft.AppBar(leading=ft.Row(controls=[ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=current_theme["top_appbar_colors"]["icon_color"], on_click=lambda _: navigate_to(page, loader, "/bills")),ft.Image(src=current_theme["top_appbar_colors"]["icon"], fit=ft.ImageFit.CONTAIN)]), leading_width=200, bgcolor=current_theme["top_appbar_colors"]["background"])
    divider1=ft.Divider(color=current_theme["divider_color"])
    divider2=ft.Divider(color=current_theme["divider_color"])
    divider3=ft.Divider(color=current_theme["divider_color"])
    
    timezones = {
    "America/New_York": "EST/EDT",
    "America/Chicago": "CST/CDT",
    "America/Denver": "MST/MDT",
    "America/Los_Angeles": "PST/PDT",
    "America/Anchorage": "AKST/AKDT",
    "Pacific/Honolulu": "HST/HDT",
    "America/Toronto": "EST/EDT",  # Canada - Eastern
    "America/Vancouver": "PST/PDT",  # Canada - Pacific
    "America/Edmonton": "MST/MDT",  # Canada - Mountain
    "Europe/London": "GMT/BST",  # UK
    "Europe/Dublin": "GMT/IST",  # Ireland
    "Australia/Sydney": "AEST/AEDT",
    "Australia/Melbourne": "AEST/AEDT",
    "Australia/Brisbane": "AEST",
    "Australia/Adelaide": "ACST/ACDT",
    "Australia/Perth": "AWST",
    "Pacific/Auckland": "NZST/NZDT",  # New Zealand
    "Africa/Johannesburg": "SAST",  # South Africa
    "UTC": "UTC",
    "America/Halifax": "AST/ADT", #Canada - Atlantic
    "America/St_Johns": "NST/NDT" #Canada - Newfoundland
}
    def update_page_theme(page: ft.Page, theme: dict):
        # Update relevant controls in the page with the new theme colors
        appbar.bgcolor = theme["top_appbar_colors"]["background"]
        appbar.leading.controls[1].src = theme["top_appbar_colors"]["icon"]
        appbar.parent.bgcolor = theme["background"]
        appbar.leading.controls[0].icon_color = theme["top_appbar_colors"]["icon_color"]
        theme_dropdown.color = theme["calc_theme"]["dropdown_text"]
        theme_dropdown.bgcolor = theme["calc_theme"]["dropdown_background"]
        theme_dropdown.border_color = theme["calc_theme"]["dropdown_border_color"]
        theme_info.color = theme["text_color"]
        divider1.color = theme["divider_color"]
        divider2.color = theme["divider_color"]
        divider3.color = theme["divider_color"]
        timezone_dropdown.color = theme["calc_theme"]["dropdown_text"]
        timezone_dropdown.border_color = theme["calc_theme"]["dropdown_border_color"]
        delete_data_info.color = theme["text_color"]
        #timezone_dropdown.label_style = {"color": current_theme["text_field"]["label_color"]},
        timezone_dropdown.border_color=current_theme["calc_theme"]["dropdown_border_color"],
        
        
        page.update()

    def update_theme(value):
        
        page.client_storage.set("burnison.me.current.theme", value.lower())
        if value.lower() == "light" or value is None:
            new_theme = light_theme()
        elif value.lower() == "dark":
            new_theme = dark_theme()
        elif value.lower() == "green":
            new_theme = green_theme()
        update_page_theme(page, new_theme)  # Call a function to apply the new theme



    theme_dropdown = ft.Dropdown(
        width=300,
        options=[
            ft.DropdownOption("Light"),
            ft.DropdownOption("Dark"), 
            ft.DropdownOption("Green")
            ],
        label="Pick A Theme",
        on_change=lambda e: update_theme(e.control.value),
        color=current_theme["settings_theme"]["dropdown_text"],
        label_style = {"color": current_theme["text_field"]["label_color"]},
        bgcolor=current_theme["settings_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_border_color"],
        #select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    theme_info = ft.Text("Theme will update upon navigating from this page", size=12, color=current_theme["text_color"])


    def update_timezone(e):
        show_loader(page, loader)
        print("timezone", e.control.value)
        ds.update_timezone(data={"timezone": e.control.value})
        hide_loader(page, loader)

    timezone_dropdown=ft.Dropdown(width=300,
                                  label="Timezone",
                                  color=current_theme["calc_theme"]["dropdown_text"],
                                  label_style = {"color": current_theme["text_field"]["label_color"]},
                                  border_color=current_theme["calc_theme"]["dropdown_border_color"],
                                  options=[ft.DropdownOption(
                text=f"{abbr} ({iana})",
                key=iana,
                #tooltip=f"{iana} (IANA Time Zone): This is the most accurate identifier for {abbr}. It automatically adjusts for daylight saving time.",
            )
            for iana, abbr in timezones.items()],
    )
    timezone_dropdown.on_change=lambda e: update_timezone(e)
    timezone_info = ft.Text("Timezone will update on Changing the selection", size=12, color=current_theme["text_color"])


    async def delete_user_data():
        show_loader(page, loader)
        print("delete user data")
        await ds.delete_user_data()
        hide_loader(page, loader)

    delete_modal = ft.AlertDialog()
    def close_modal(e):
        page.close(delete_modal)
    delete_modal.modal=True
    delete_modal.title=ft.Text("Please confirm")
    delete_modal.content=ft.Text("Do you really want to delete all of your data?\nThis will also delete your account.")
    delete_modal.actions=[
            ft.TextButton("Yes", on_click=lambda _: asyncio.run(delete_user_data())),
            ft.TextButton("No", on_click=close_modal),
        ]
    delete_modal.actions_alignment=ft.MainAxisAlignment.END
    delete_modal.on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed"),
        )
    #page.overlay.append(delete_modal)
    
    delete_user_data_button=ft.ElevatedButton("Delete My Data", color=ft.Colors.BLACK, bgcolor=ft.Colors.RED, on_click=lambda _: page.open(delete_modal))
    delete_data_info = ft.Text("This will delete all of your data from the server and log you out.", size=12, color=current_theme["text_color"])


    update_frequency_dropdown = ft.Dropdown(
        width=300,
        options=[
            ft.DropdownOption("Once a day(default)"),
            ft.DropdownOption("Once a week"), 
            ft.DropdownOption("Once a month")
            ],
        label="Update Frequency",
        on_change=lambda e: page.client_storage.set("update_frequency", e.control.value),
        color=current_theme["calc_theme"]["dropdown_text"],
        bgcolor=current_theme["calc_theme"]["dropdown_background"],
        border_color=current_theme["calc_theme"]["dropdown_border_color"],
        #select_icon_enabled_color=current_theme["calc_theme"]["dropdown_icon_color"],
    )
    update_frequency_info = ft.Text("How often do you want to check the server for your updated data", size=12, color=current_theme["text_color"])

    
    page.views.append(ft.View(
        "/settings",
        bgcolor=current_theme["background"],
        controls=[
            ft.Column(controls=[theme_dropdown,
                                 theme_info,
                                 divider1,
                                 timezone_dropdown,
                                 timezone_info,
                                 divider2,
                                 delete_user_data_button,
                                 delete_data_info,
                                 divider3,
                                 #update_frequency_info
                                 ], width=400, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            appbar=appbar
        )
    )
    page.update()


    async def build_bill_list():
        show_loader(page, loader)
        data= await ds.get_timezone()
        if data["error"] is not None or data["error"] != "":
            print(data)
            tzone_data=data["data"]
            
            if tzone_data is not None:
                timezone=tzone_data["timezone"]
                timezone_dropdown.value=timezone
                page.update()
        hide_loader(page, loader)
    asyncio.run(build_bill_list())