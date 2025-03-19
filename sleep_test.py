import time

start_time = time.time()
time.sleep(2) # Затримка на 2 секунди
end_time = time.time()
time_taken = end_time - start_time

print(f"Затримка часу: {time_taken} секунд")
if time_taken > 1.9 and time_taken < 2.5: # Перевірка, що затримка приблизно 2 секунди
    print("time.sleep(2) працює коректно!")
else:
    print("time.sleep(2) НЕ працює коректно!")
