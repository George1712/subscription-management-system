import re
from datetime import datetime, date, timedelta

def validate_name(name, field_name="name") :
    # field_name => first_name or last_name
    # return (True/False, error message)
    if not name or not name.strip() : # Empty name
        return False, f"{field_name} cannot be empty"
    name = name.strip()
    if len(name) < 2: # Too short
        return False, f"{field_name} must be at least 2 characters long"
    if len(name) > 50: # Too long
        return False, f"{field_name} cannot exceed 50 characters"
    if not re.match(r"^[a-zA-Z\s\-']+$", name) : # Allowed characters
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""

def validate_email(email) :
    if not email :
        return True, ""
    email = email.strip()

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_pattern, email) :
        return False, "Invalid Email Address"
    if len(email) > 100 :
        return False, "Email cannot Exceed 100 characters"
    return True, ""


def validate_phone(phone) :
    if not phone :
        return True, ""

    phone = phone.strip()
    digits = re.sub(r"\D", '', phone)

    if len(digits) < 10 :
        return False, "Phone number must have at least 10 digits"
    if len(digits) > 20 :
        return False, "Phone number cannot exceed 20 digits"

    return True, ""


def validate_date(date_str, field_name = "Date", allow_future = False) :
    if not date_str :
        return False, f"{field_name} is required"
    try :
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if not allow_future and parsed_date > date.today() :
            return False, f"{field_name} cannot be in the future"
        return True, ""
    except ValueError :
        return False, f"{field_name} must be in YYYY-MM-DD format"
        

    
def validate_positive_number(value, field_name="Value", allow_zero=False) :
    try :
        num = float(value)

        if allow_zero:
            if num < 0:
                return False, f"{field_name} must be zero or greater"
        else:
            if num <= 0:
                return False, f"{field_name} must be greater than zero"

        return True, ""
    except (ValueError, TypeError) :
        return False, f"{field_name} must be a valid number"



def validate_status(status) :
    valid_statuses = ["Active", "Inactive"]

    if status not in valid_statuses :
        return False, f"Status must be one of: {', '.join(valid_statuses)}" 

    return True, ""


def validate_date_ranges(start_date_str:str, end_date_str:str, allow_future:bool=False) :

    # Validate the dates first
    valid, message = validate_date(start_date_str, "Start date")
    if not valid:
        return valid, message
    
    valid, message = validate_date(end_date_str, "End date")
    if not valid:
        return valid, message
    
    # parse the dates to datetime.date object
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    if (start_date >= end_date) :
        return False, "End date must be after start date"

    return True, ""


def validate_payment_date_range(start_date_str: str, end_date_str: str) -> tuple:
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return False, "Dates must be in YYYY-MM-DD format"
    
    today = date.today()
    
    if start_date > end_date:
        return False, "Start date must be before end date"
    return True, ""


def validate_subscription_dates(start_date_str, duration_days) :
    # returns (is_valid, error_message, end_date)

    valid, message = validate_date(start_date_str, "Start date")
    if not valid :
        return valid, message, None

    valid, message = validate_positive_number(duration_days, "Duration", allow_zero=False)
    if not valid:
        return valid, message, None
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = start_date + timedelta(days=int(duration_days))

    return True, "", end_date

