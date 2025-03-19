import requests
import time
import subprocess
import pytest

@pytest.fixture(scope="module")
def app_process():
    """Фікстура pytest для запуску та зупинки Flask застосунку як підпроцесу."""
    process = subprocess.Popen(["python", "app_cached.py"]) # Запускаємо app_cached.py як підпроцес
    time.sleep(3)  # Даємо час серверу запуститися (збільшено до 3 секунд)
    yield process  # Тести будуть виконуватися тут
    process.terminate() # Зупиняємо процес після завершення тестів
    process.wait()

def test_cache_integration(app_process):
    """Інтеграційний тест для перевірки кешування через HTTP запити."""
    base_url = "http://127.0.0.1:5000"
    item_id = 1

    # Перший запит - кеш має бути порожнім (відключаємо кешування requests)
    start_time = time.time()
    response1 = requests.get(f"{base_url}/item/{item_id}", headers={'Cache-Control': 'no-cache'})
    response1.raise_for_status() # Перевірка на HTTP помилки
    time_taken1 = time.time() - start_time

    print(f"Час першого запиту: {time_taken1}") # Доданий вивід часу першого запиту
    assert time_taken1 > 1.5 # Перевірка, що перший запит був повільним (через time.sleep(2) в get_data_from_slow_source)

    # Другий запит - кеш має спрацювати
    start_time = time.time()
    response2 = requests.get(f"{base_url}/item/{item_id}")
    response2.raise_for_status()
    time_taken2 = time.time() - start_time

    print(f"Час другого запиту: {time_taken2}") # Доданий вивід часу другого запиту
    assert time_taken2 < 0.5 # Перевірка, що другий запит був швидким (з кешу)