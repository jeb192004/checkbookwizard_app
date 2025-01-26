import flet as ft
from ui.alert import show_loader
from datetime import date, timedelta


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


def navigate_to(page: ft.Page, loader, route: str):
    if route != "/settings":
        show_loader(page, loader)
    page.go(route)

def sort_earnings(earnings, sort_by: str):
    if sort_by == "amount":
        return sorted(earnings, key=lambda x: float(x.get('amount', '0').replace(',', '')) if 'amount' in x and x['amount'] else 0)
    elif sort_by == "hours":
        return sorted(earnings, key=lambda x: x['amount'])
    else:
        return earnings       
    
def day_of_week_to_day_of_month(day_of_week, week_of_month, current_date):
    month=current_date.month
    year=current_date.year
    before_date = current_date + timedelta(days=6)
    #print(before_date.day)
    if week_of_month==0 and before_date.day<7:
        month = month+1 if month < 12 else 1
    firstDay = date(year=year, month=month, day=1)
    # Adjust weekday_index if Sunday is 0
    adjusted_weekday_index = (day_of_week + 1) % 7 
    # Calculate the offset to the first occurrence of the specified weekday
    offset = (day_of_week - firstDay.isoweekday() + 7) % 7
    # Calculate the date of the specified occurrence
    result_date = firstDay + timedelta(days=offset + week_of_month * 7)
    # Calculate the date of the specified occurrence
    target_date = result_date - timedelta(weeks=(week_of_month - 1))
    '''if occurrence == 0:
        target_date = result_date'''
    
    return f'{year}-{int(result_date.day):02d}-{month}'
