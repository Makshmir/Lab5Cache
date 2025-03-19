import requests
import time
import subprocess
import pytest

@pytest.fixture(scope="module")
def app_process():
    """Фікстура pytest для запуску та зупинки Flask застосунку app.py (без кешування)."""
    process = subprocess.Popen(["python", "app.py"]) # Запускаємо app.py замість app_cached.py
    time.sleep(3)
    yield process
    process.terminate()
    process.wait()

def test_no_cache_integration(app_process): # Змінено назву тесту
    """Інтеграційний тест для перевірки відсутності кешування в app.py."""
    base_url = "http://127.0.0.1:5000"
    item_id = 1

    # Перший запит - має бути повільним
    start_time = time.time()
    response1 = requests.get(f"{base_url}/item/{item_id}")
    response1.raise_for_status()
    time_taken1 = time.time() - start_time

    print(f"Час першого запиту (без кешування): {time_taken1}")
    assert time_taken1 > 1.5 # Перевірка, що перший запит повільний

    # Другий запит - також має бути повільним (оскільки кешування немає)
    start_time = time.time()
    response2 = requests.get(f"{base_url}/item/{item_id}")
    response2.raise_for_status()
    time_taken2 = time.time() - start_time

    print(f"Час другого запиту (без кешування): {time_taken2}")
    assert time_taken2 > 1.5 # Перевірка, що другий запит теж повільний (без кешування)
