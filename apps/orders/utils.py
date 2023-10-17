from datetime import datetime

from django.utils import timezone

current_time = timezone.now()
datetime_time = datetime.now().hour

times = f"""
    1. TZ. Time: {current_time},
    2. DT. Time: {datetime_time}
"""

def determin_meal_time():
    meal_time = ""
    if datetime_time >= 1 and datetime_time < 12:
        meal_time = "Breakfast"
    elif datetime_time >= 12 and datetime_time <= 16:
        meal_time = "Lunch"
    elif datetime_time >= 16:
        meal_time = "Supper"

    print(f"Meal Time: {meal_time}")
    return meal_time
    
