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
        "border_color":"#fed831",
        "shadow_color": "#000000",
        "divider_color":"#fed831",
        "alert_background_color":"#85bb65",
        "alert_button_color":"#1b4a00",
        "text_field":{
            "label_color_focused": "#fed831",
            "label_color": "#ffffff",
            "text_color": "#ffffff",
            "background_color": "#1b4a00",
            "border_color": "#fed831"
        },
        "elevated_button":{
            "background": "#1b4a00",
            "text": "#ffffff",
            "icon_color": "#ffffff", 
        },
        "label":{
            "color": "#ffffff"
        },
        "radio":{
            "fill_color": "#fed831",
            "label_color": "#ffffff",
            "background_color": "#1b4a00",
            "border_color": "#fed831"
        },
        "earnings_list_title_color": "#ffffff",
        "header_text_color": "#000000",
         "dropdown":{
            "background":"#E0E0E0"
        },
         "dropdown":{
            "background":"#1b4a00"
        },
        "list_item_colors": {
            "base": "#1b4a00",
            "inner_container": "#2F6D23",
            "text_color": "#000000",
            "title_color": "#fed831",
            "bill_name_color": "#000000",
            "link_color": "#7cfc00",
            "icon_color": "#fed831",
            "total_amount_title_color": ft.Colors.GREY,
            "total_amount_text_color": "#000000",
            "total_amount_icon_color": "#fed831",
            "total_amount_background_color": "#ffffff",
            "total_amount_border_color": "#7cfc00"
        },
        "top_appbar_colors": {
            "background": "#118c4f",
            "text": ft.Colors.WHITE,
            "icon_color": ft.Colors.WHITE,
            "icon": "/header-yellow.png"
        },
        "bottom_navigation_colors": {
            "background": "#118c4f",
            "text": ft.Colors.WHITE,
            "icon": ft.Colors.WHITE
        },
        "bottom_sheet":{
            "background_color": "#118c4f",
            "button_text_color": "#ffffff",
            "button_color": "#4caf50"
        },
        "calc_theme": {
            "background": "#118c4f",
            "text_title": ft.Colors.BLACK,
            "text": ft.Colors.BLACK,
            "dropdown_text": ft.Colors.WHITE,
            "dropdown_background": "#4caf50",
            "dropdown_border_color": "#4caf50",
            "dropdown_icon_color": ft.Colors.WHITE
        },
        "settings_theme": {
            "dropdown_background": ft.Colors.GREY,
            "dropdown_text": ft.Colors.WHITE
        }
    }


def dark_theme():
    return {
        "background": ft.Colors.BLACK,
        "text_color": "#ffffff",
        "progress_bar_color": "#fed831",
        "border_color":"#ffffff",
        "shadow_color": "#ffffff",
        "text_field_label_color": "#fed831",
        "header_text_color": "#ffffff",
        "earnings_list_title_color": "#ffffff",
        "divider_color":"#ffffff",
        "alert_background_color":"#4E4E4E",
        "alert_button_color":"#3A3A3A",
        "text_field":{
            "label_color_focused": "#ffffff",
            "label_color": "#ffffff",
            "text_color": "#ffffff",
            "background_color": "#4E4E4E",
            "border_color": "#ffffff"
        },
        "elevated_button":{
            "background": "#3A3A3A",
            "text": "#ffffff",
            "icon_color": "#ffffff", 
        },
        "label":{
            "color": "#ffffff"
        },
        "radio":{
            "fill_color": "#ffffff",
            "label_color": "#ffffff",
            "background_color": "#4E4E4E",
            "border_color": "#ffffff"
        },
         "dropdown":{
            "background":"#4E4E4E"
        },
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
            "text": ft.Colors.WHITE,
            "icon_color": ft.Colors.WHITE,
            "icon": "/header-colored.png"
        },
        "bottom_navigation_colors": {
            "background": "#292929",
            "text": ft.Colors.WHITE,
            "icon": ft.Colors.WHITE
        },
        "bottom_sheet":{
            "background_color": "#262626",
            "button_text_color": "#ffffff",
            "button_color": ft.Colors.GREY
        },
        "calc_theme": {
            "background": "#262626",
            "text_title": "#fed831",
            "text": ft.Colors.WHITE,
            "dropdown_text": ft.Colors.WHITE,
            "dropdown_background": ft.Colors.GREY,
            "dropdown_border_color": "#262626",
            "dropdown_icon_color": ft.Colors.WHITE
        },
         "settings_theme": {
            "dropdown_background": ft.Colors.GREY,
            "dropdown_text": ft.Colors.WHITE
        }
    }

def light_theme():
    return {
        "background": ft.Colors.WHITE,
        "text_color": "#000000",
        "progress_bar_color": "#000000",
        "border_color":"#000000",
        "text_field_label_color": "#fed831",
        "shadow_color": "#000000",
        "header_text_color": "#000000",
        "earnings_list_title_color": "#000000",
        "divider_color":"#000000",
        "alert_background_color":ft.Colors.WHITE,
        "alert_button_color":"#E0E0E0E0",
        "text_field":{
            "label_color_focused": "#000000",
            "label_color": "#000000",
            "text_color": "#000000",
            "background_color": "#E0E0E0E0",
            "border_color": "#000000"
        },
        "elevated_button":{
            "background": "#000000",
            "text": "#ffffff",
            "icon_color": "#ffffff", 
        },
        "label":{
            "color": "#000000"
        },
        "radio":{
            "fill_color": "#000000",
            "label_color": "#000000",
            "background_color": "#E0E0E0E0",
            "border_color": "#000000"
        },
        "dropdown":{
            "background":"#E0E0E0"
        },
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
            "text": ft.Colors.BLACK,
            "icon_color": ft.Colors.BLACK,
            "icon": "/header-black.png"
        },
        "bottom_navigation_colors": {
            "background": "#E0E0E0",
            "text": ft.Colors.BLACK,
            "icon": ft.Colors.BLACK
        },
        "bottom_sheet":{
            "background_color": "#BDBDBD",
            "button_text_color": ft.Colors.BLACK,
            "button_color": ft.Colors.WHITE
        },
        "calc_theme": {
            "background": "#BDBDBD",
            "text_title": ft.Colors.BLACK,
            "text": ft.Colors.BLACK,
            "dropdown_text": ft.Colors.BLACK,
            "dropdown_background": ft.Colors.WHITE,
            "dropdown_border_color": ft.Colors.GREY,
            "dropdown_icon_color": ft.Colors.BLACK
        },
        "settings_theme": {
            "dropdown_background": ft.Colors.GREY,
            "dropdown_text": ft.Colors.WHITE
        }
    }
