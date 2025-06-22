# time_utils.py

from datetime import datetime, time, timedelta
import pytz

CITIES_TIMEZONES = {
    "Нью-Йорк": "America/New_York",
    "Лондон": "Europe/London",
    "Токіо": "Asia/Tokyo"
}

EXCHANGE_HOURS = {
    "Нью-Йорк": {"open": time(9, 30), "close": time(16, 0)},
    "Лондон": {"open": time(8, 0), "close": time(16, 30)},
    "Токіо": {"open": time(9, 0), "close": time(15, 0)}
}

def get_current_time(city: str) -> str:
    """Отримує поточний час у заданому місті."""
    try:
        timezone = pytz.timezone(CITIES_TIMEZONES[city])
        city_time = datetime.now(timezone)
        return city_time.strftime("%H:%M:%S")
    except Exception as e:
        print(f"Помилка при отриманні часу для {city}: {e}")
        return "Немає даних"

def is_exchange_active(city: str) -> bool:
    """Визначає, чи біржа у заданому місті зараз відкрита, враховуючи вихідні."""
    try:
        timezone = pytz.timezone(CITIES_TIMEZONES[city])
        now = datetime.now(timezone)
        
        if now.weekday() in [5, 6]: # 5 = Субота, 6 = Неділя
            return False

        open_time = EXCHANGE_HOURS[city]["open"]
        close_time = EXCHANGE_HOURS[city]["close"]
        return open_time <= now.time() <= close_time
    except Exception as e:
        print(f"Помилка при визначенні статусу біржі для {city}: {e}")
        return False

def get_time_until_open(city: str) -> str:
    """Розраховує час до наступного відкриття біржі, враховуючи вихідні."""
    try:
        target_timezone = pytz.timezone(CITIES_TIMEZONES[city])
        target_now = datetime.now(target_timezone)
        
        open_time = EXCHANGE_HOURS[city]["open"]
        next_open_date = target_now.date()

        # Визначення дати наступного робочого дня
        if target_now.weekday() == 4 and target_now.time() >= open_time: # П'ятниця після відкриття
            next_open_date += timedelta(days=3)
        elif target_now.weekday() == 5: # Субота
            next_open_date += timedelta(days=2)
        elif target_now.weekday() == 6: # Неділя
            next_open_date += timedelta(days=1)
        elif target_now.time() >= open_time: # Будній день після відкриття
             next_open_date += timedelta(days=1)

        next_opening_datetime = target_timezone.localize(datetime.combine(next_open_date, open_time))
        delta = next_opening_datetime - target_now

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours} год {minutes} хв"
    except Exception as e:
        print(f"Помилка при розрахунку часу до відкриття для {city}: {e}")
        return "Невідомо"