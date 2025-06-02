import json
import requests
from bs4 import BeautifulSoup
import time

# Загрузка данных из JSON-файла
with open('query.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Собираем уникальные сочетания
combinations = set()

for item in data:
    # Обрабатываем item1Label и article1
    item1_label = item.get('item1Label', '')
    article1 = item.get('article1', '')
    if article1:
        combinations.add((item1_label, article1))
    else:
        combinations.add((item1_label, "not existing article"))
    
    # Обрабатываем item2Label и article2
    item2_label = item.get('item2Label', '')
    article2 = item.get('article2', '')
    if article2:
        combinations.add((item2_label, article2))
    else:
        combinations.add((item2_label, "not existing article"))

# Функция для получения первого абзаца из статьи Wikipedia
def get_wikipedia_topic(article_url):
    try:
        # Получаем название статьи из URL
        title = article_url.split('/')[-1]
        
        # API запрос к Wikipedia
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
        
        response = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        return page.get('extract', 'No topic found')
        
    except Exception as e:
        print(f"Error fetching {article_url}: {str(e)}")
        return "Error fetching topic"

# Создаем финальный результат
result = []
for label, article in combinations:
    if article == "not existing article":
        topic = "not existing article"
    else:
        topic = get_wikipedia_topic(article)
        # Добавляем задержку между запросами
        time.sleep(1)  # Чтобы не перегружать сервер
    
    result.append({
        "label": label,
        "article": article,
        "topic": topic
    })

# Сортируем по label
result.sort(key=lambda x: x['label'])

# Сохраняем в JSON файл
with open('enriched_articles.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Результат сохранён в enriched_articles.json")