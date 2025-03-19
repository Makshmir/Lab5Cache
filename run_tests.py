import test_app

if __name__ == "__main__":
    test_app.test_get_data_from_slow_source()
    test_app.test_cache_is_used()
    print("Всі тести виконано (якщо не було помилок вище)!")
