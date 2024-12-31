import flet as ft


def format_dollar(e, page: ft.Page, text_field: ft.TextField):
    # Get the current input value, strip $, and reformat
    current_value = e.control.value.replace(".", "").replace(",", "")
        
    # Allow only digits
    if not current_value.isdigit():
        e.control.value = f"{text_field.value}"
        page.update()
        return

    # Limit to a maximum length for formatting (e.g., max $9999.99)
    max_length = 15  # For up to "100,000,000,000.00"
    if len(current_value) > max_length:
        current_value = current_value[-max_length:]

    # Convert to dollar-and-cents format
    if len(current_value) <= 2:
        dollars = "0"
        cents = current_value.zfill(2)
    else:
        dollars = current_value[:-2]
        cents = current_value[-2:]

    formatted_value = f"{int(dollars):,}.{cents}"

    # Update the text field with the formatted value
    text_field.value = formatted_value
    page.update()
