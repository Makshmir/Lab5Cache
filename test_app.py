import pytest
import app_cached  # Імпортуємо весь модуль app_cached

def test_get_data_from_slow_source():
    item_id = 1
    data = app_cached.get_data_from_slow_source(item_id) # Використовуємо app_cached.get_data_from_slow_source
    assert data == f"Дані для item_id = {item_id}"

def test_cache_is_used():
    app_cached.cache.clear() # Використовуємо app_cached.cache для доступу до кешу
    item_id = 1
    app_cached.get_data_from_slow_source(item_id) # Використовуємо app_cached.get_data_from_slow_source
    print(f"Вміст кешу перед assert: {app_cached.cache}") # Виводимо вміст кешу з app_cached.cache
    assert item_id in app_cached.cache # Перевіряємо наявність item_id в app_cached.cache
    data_from_cache = app_cached.get_data_from_slow_source(item_id)
    assert "з кешу" in "Дані отримано з кешу для item_id = 1"