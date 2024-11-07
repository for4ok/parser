import requests
from bs4 import BeautifulSoup
import json
import time

# URL для начальной страницы
base_url = 'https://quotes.toscrape.com/'

# Пустой список для сохранения всех цитат
quotes_data = []

# Стартовая страница
page = 1

# Цикл для прохода по всем страницам
while True:
    # Создаем URL для текущей страницы
    url = f'{base_url}page/{page}/'

    # Запрос на страницу
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code != 200:
        print("Все страницы обработаны.")
        break

    # Парсинг HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск всех блоков с цитатами
    quotes = soup.find_all('div', class_='quote')

    # Если на странице нет цитат, прекращаем цикл
    if not quotes:
        break

    # Обработка каждой цитаты
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]

        # Добавление цитаты в список данных
        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    print(f"Обработана страница {page}")

    # Переход к следующей странице
    page += 1

    # Задержка между запросами
    time.sleep(1)

# Сохранение собранных данных в JSON-файл
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в quotes.json")