# tracker.py

import requests

def get_all_coins_data(symbols: list[str]) -> dict:
    """
    Отримує 24-годинні дані з Binance для списку символів.
    Це єдина функція, яку буде викликати GUI.
    """
    all_data = {}
    for symbol in symbols:
        try:
            params = {'symbol': symbol}
            response = requests.get('https://api.binance.com/api/v3/ticker/24hr', params=params)
            response.raise_for_status()
            all_data[symbol] = response.json()
        except requests.RequestException as e:
            print(f"Помилка при отриманні даних з Binance для {symbol}: {e}")
            all_data[symbol] = None # Позначаємо, що дані для цього символу отримати не вдалося
            
    return all_data