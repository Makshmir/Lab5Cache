"""
Простий Flask веб-застосунок з кешуванням в пам'яті та експортом метрик Prometheus.
(Використовується простий Gauge без lambda для CACHE_SIZE - обхідний шлях)
"""
import time
from flask import Flask
from prometheus_client import Counter, Histogram, Gauge
from prometheus_client.exposition import make_wsgi_app

app = Flask(__name__)
cache = {}


REQUEST_COUNT = Counter('http_requests_total', 'Загальна кількість HTTP запитів')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Затримка HTTP запитів')
CACHE_HIT_COUNT = Counter('cache_hits_total', 'Кількість попадань в кеш')
CACHE_MISS_COUNT = Counter('cache_misses_total', 'Кількість промахів кешу')
CACHE_SIZE = Gauge('cache_size', 'Розмір кешу в пам\'яті')

def get_data_from_slow_source(item_id):
    """Імітація отримання даних з повільного джерела."""
    time.sleep(2)
    return f"Дані для item_id = {item_id}"

@app.route('/item/<int:item_id>')
def get_item(item_id):
    """
    Обробляє запит на отримання даних про елемент за item_id.
    Використовує кеш для прискорення повторних запитів.
    """
    REQUEST_COUNT.inc()

    with REQUEST_LATENCY.time():
        if item_id in cache:
            CACHE_HIT_COUNT.inc()
            data = cache[item_id]
            print(f"Дані отримано з кешу для item_id = {item_id}")
        else:
            CACHE_MISS_COUNT.inc()
            data = get_data_from_slow_source(item_id)
            cache[item_id] = data
            print(f"Дані отримано з повільного джерела та закешовано для item_id = {item_id}")
    CACHE_SIZE.set(len(cache)) 
    return f"Отримано дані: {data}"

@app.route('/metrics')
def metrics():
    """Експортує Prometheus метрики."""
    return make_wsgi_app()

if __name__ == '__main__':
    app.run(debug=True)
