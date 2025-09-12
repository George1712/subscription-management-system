from datetime import date, datetime, timedelta
import os
from re import sub
from typing import Optional, Union


def get_current_date() -> str :
    return datetime.now().strftime('%Y-%m-%d')


def format_date(date_obj: Union[date, datetime, str]) -> str :
    # return a string date on the format "YYY-MM-DD"
    if isinstance(date_obj, str) :
        try :
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d');
        except ValueError :
            return date_obj

    if isinstance(date_obj, (date, datetime)) :
        return date_obj.strftime('%Y-%m-%d')
    
    return str(date_obj)


def parse_date(date_str: str) -> Optional[date] :
    try :
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError) :
        return None


def add_days_to_date(start_date: Union[date, str], days: int) -> date :

    if isinstance(start_date, str) :
        start_date = parse_date(start_date)
        if start_date is None :
            raise ValueError("Invalid date format")
        
    return start_date + timedelta(days=days)

    
def days_between_dates(start_date: Union[date, str], end_date: Union[date, str]) -> int :
    if isinstance(start_date, str):
        start_date = parse_date(start_date)
    if isinstance(end_date, str):
        end_date = parse_date(end_date)

    if start_date is None or end_date is None :
        return 0
    
    return (end_date - start_date).days


def clear_screen() :
    os.system('cls' if os.name == 'nt' else 'clear')

# def print_separator(unit: str, length: int) :
#     print(str(unit) * length)

def press_enter_to_continue(message: str = "Press Enter to continue") :
    input(f"\n{message}")

def get_confirmation(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'.")


def format_currency(amount: float) :
    return f"${amount:,.2f}"

def truncate_text(text: str, max_length: int) -> str :
    if len(text) <= max_length :
        return text
    return text[: max_length - 3] + "..."


def calculate_subscription_end_date(start_date: Union[date, str], duration: int) :
    return add_days_to_date(start_date, duration)


def format_duration(days: int) -> str :

    try:
        total_days = int(days)
        if total_days <= 0:
            return "0 days"
    except (ValueError, TypeError):
        return "0 days"

    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days_remaining = remaining_days % 30

    duration = []
    
    if years > 0:
        duration.append(f"{years} year{'s' if years > 1 else ''}")
    if months > 0:
        duration.append(f"{months} month{'s' if months > 1 else ''}")
    if days_remaining > 0:
        duration.append(f"{days_remaining} day{'s' if days_remaining > 1 else ''}")

    return " ".join(duration) if duration else "0 days"


def sanitize_input(input_str: str) :
    if not input_str :
        return ""
    sanitized = sub(r"\s+", " ", input_str).strip()
    return sanitized


def is_valid_id(id_str: str) -> bool:
    try:
        id_num = int(id_str)
        return id_num > 0
    except (ValueError, TypeError):
        return False

