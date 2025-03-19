"""
Простий Flask веб-застосунок без кешування.
Демонструє повільне отримання даних.
"""
import time
from flask import Flask

app = Flask(__name__)

def get_data_from_slow_source(item_id):
    """
    Імітує отримання даних з повільного джерела.

    Args:
        item_id (int): Ідентифікатор елемента, дані якого потрібно отримати.

    Returns:
        str: Рядок з даними для вказаного item_id.
    """
    time.sleep(2)
    return f"Дані для item_id = {item_id}"

@app.route('/item/<int:item_id>')
def get_item(item_id):
    """
    Обробляє запит на отримання даних про елемент за item_id.

    Args:
        item_id (int): Ідентифікатор елемента.

    Returns:
        str: Веб-сторінка з даними про елемент.
    """
    data = get_data_from_slow_source(item_id)
    return f"Отримано дані: {data}"

if __name__ == '__main__':
    app.run(debug=True)
