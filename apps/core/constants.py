import calendar
from datetime import datetime, date

UNIT_CHOICES = (
    ("Kg", "Kg"),
    ("Grams", "Grams"),
    ("Pieces", "Pieces"),
    ("Boxes", "Boxes"),
    ("Cartons", "Cartons"),
    ("Metres", "Metres"),
    ("Litres", "Litres"),
)


MONTHS_LIST = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

YEARS_LIST = [2025, 2026, 2027, 2028, 2029, 2030]


def get_month_number(month_name: str) -> int:
    try:
        # Normalize to capitalize first letter only, e.g. "january" → "January"
        month_name = month_name.capitalize()
        return list(calendar.month_name).index(month_name)
    except ValueError:
        return -1  # return -1 if invalid


def get_month_name(month_number: int) -> str:
    return calendar.month_name[month_number]


def format_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def format_datetime(date_str: str):
    """
    Parses a date or datetime string and returns a datetime object.
    Supports formats:
      - 'YYYY-MM-DD'
      - 'YYYY-MM-DD HH:MM'
      - 'YYYY-MM-DDTHH:MM'
    """
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")
