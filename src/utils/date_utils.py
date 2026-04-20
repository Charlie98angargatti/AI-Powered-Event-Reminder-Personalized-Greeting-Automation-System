from datetime import datetime

def is_today_event(date_string: str) -> bool:
    """
    Check if a given date string (MM-DD) matches today's date
    """
    today = datetime.today().strftime("%m-%d")
    return today == date_string
