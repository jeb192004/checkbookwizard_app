import flet as ft

# checkbook wizard app icon background color - #607D8B
# app icon robe color - #1F7B4A
# app icon collar color - #C07D09
# app icon collar 2nd color - #9A6B1F
# app icon collar border color - #EADD53
# app icon text color - #71b681
# Define custom themes with specific container and text colors
def green_theme():
    return {
        "background": "#85bb65",
        "text_color": "#000000",
        "progress_bar_color": "#fed831",
        "list_item_colors": {
            "base": "#1b4a00",
            "inner_container": "#2F6D23",
            "text_color": "#000000",
            "title_color": "#fed831",
            "bill_name_color": "#000000",
            "link_color": "#7cfc00",
            "icon_color": "#fed831",
            "total_amount_title_color": ft.colors.GREY,
            "total_amount_text_color": "#000000",
            "total_amount_icon_color": "#fed831",
            "total_amount_background_color": "#ffffff",
            "total_amount_border_color": "#7cfc00"
        },
        "top_appbar_colors": {
            "background": "#118c4f",
            "text": ft.colors.WHITE,
            "icon_color": ft.colors.WHITE,
            "icon": "/header-yellow.png"
        },
        "bottom_navigation_colors": {
            "background": "#118c4f",
            "text": ft.colors.WHITE,
            "icon": ft.colors.WHITE
        },
        "bottom_sheet":{
            "background_color": "#118c4f",
            "button_text_color": "#ffffff",
            "button_color": "#4caf50"
        },
        "calc_theme": {
            "background": "#118c4f",
            "text_title": ft.colors.BLACK,
            "text": ft.colors.BLACK,
            "dropdown_text": ft.colors.WHITE,
            "dropdown_background": "#4caf50",
            "dropdown_border_color": "#1b4a00",
            "dropdown_icon_color": ft.colors.WHITE
        }
    }


def dark_theme():
    return {
        "background": ft.colors.BLACK,
        "text_color": "#ffffff",
        "progress_bar_color": "#fed831",
        "list_item_colors": {
            "base": "#262626",
            "inner_container": "#3A3A3A",
            "text_color": "#ffffff",
            "title_color": "#fed831",
            "bill_name_color": "#ffffff",
            "link_color": "silver",
            "icon_color": "#fed831",
            "total_amount_title_color": "#fed831",
            "total_amount_text_color": "#ffffff",
            "total_amount_icon_color": "#fed831",
            "total_amount_background_color": "#4E4E4E",
            "total_amount_border_color": "#ffffff"
        },
        "top_appbar_colors": {
            "background": "#292929",
            "text": ft.colors.WHITE,
            "icon_color": ft.colors.WHITE,
            "icon": "/header-colored.png"
        },
        "bottom_navigation_colors": {
            "background": "#292929",
            "text": ft.colors.WHITE,
            "icon": ft.colors.WHITE
        },
        "bottom_sheet":{
            "background_color": "#262626",
            "button_text_color": "#ffffff",
            "button_color": ft.colors.GREY
        },
        "calc_theme": {
            "background": "#262626",
            "text_title": "#fed831",
            "text": ft.colors.WHITE,
            "dropdown_text": ft.colors.WHITE,
            "dropdown_background": ft.colors.GREY,
            "dropdown_border_color": "#262626",
            "dropdown_icon_color": ft.colors.WHITE
        }
    }

def light_theme():
    return {
        "background": ft.colors.WHITE,
        "text_color": "#000000",
        "progress_bar_color": "#000000",
        "list_item_colors": {
            "base": "#BDBDBD",
            "inner_container": "#E0E0E0E0",
            "text_color": "#000000",
            "title_color": "#000000",
            "bill_name_color": "#000000",
            "link_color": "#1976D2",
            "icon_color": "#000000",
            "total_amount_title_color": "#000000",
            "total_amount_text_color": "#000000",
            "total_amount_icon_color": "#000000",
            "total_amount_background_color": "#ffffff",
            "total_amount_border_color": "#000000"
        },
        "top_appbar_colors": {
            "background": "#E0E0E0",
            "text": ft.colors.BLACK,
            "icon_color": ft.colors.BLACK,
            "icon": "/header-black.png"
        },
        "bottom_navigation_colors": {
            "background": "#E0E0E0",
            "text": ft.colors.BLACK,
            "icon": ft.colors.BLACK
        },
        "bottom_sheet":{
            "background_color": "#ffffff",
            "button_text_color": ft.colors.BLACK,
            "button_color": ft.colors.GREY
        },
        "calc_theme": {
            "background": "#E0E0E0",
            "text_title": ft.colors.BLACK,
            "text": ft.colors.BLACK,
            "dropdown_text": ft.colors.BLACK,
            "dropdown_background": ft.colors.WHITE,
            "dropdown_border_color": ft.colors.GREY,
            "dropdown_icon_color": ft.colors.BLACK
        }
    }
