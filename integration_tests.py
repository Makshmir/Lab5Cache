import requests
import time
import subprocess
import pytest

@pytest.fixture(scope="module")
def app_process():
    """Фікстура pytest для запуску та зупинки Flask застосунку як підпроцесу."""
    process = subprocess.Popen(["python", "app_cached.py"]) 
    time.sleep(3) 
    yield process 
    process.terminate()
    process.wait()

def test_cache_integration(app_process):
    """Інтеграційний тест для перевірки кешування через HTTP запити."""
    base_url = "http://127.0.0.1:5000"
    item_id = 1


    start_time = time.time()
    response1 = requests.get(f"{base_url}/item/{item_id}", headers={'Cache-Control': 'no-cache'})
    response1.raise_for_status() 
    time_taken1 = time.time() - start_time

    print(f"Час першого запиту: {time_taken1}") 
    assert time_taken1 > 1.5


    start_time = time.time()
    response2 = requests.get(f"{base_url}/item/{item_id}")
    response2.raise_for_status()
    time_taken2 = time.time() - start_time

    print(f"Час другого запиту: {time_taken2}")
    assert time_taken2 < 0.5
