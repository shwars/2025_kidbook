import requests
import urllib3
import json
import os
import re
import shutil
from typing import Dict, List

# Отключаем предупреждения об SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_topics(topics_path: str) -> Dict[str, List[str]]:
    """Загружает словарь тем из JSON файла"""
    with open(topics_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_reverse_mapping(topics: Dict[str, List[str]]) -> Dict[str, str]:
    """Создает обратное отображение: слово -> имя файла"""
    reverse_map = {}
    for file_name, words in topics.items():
        for word in words:
            reverse_map[word.lower()] = f"./{file_name}.md"
    return reverse_map

def add_links_to_md(file_path: str, reverse_map: Dict[str, str], topics: Dict[str, List[str]]):
    """Обрабатывает MD файл, добавляя ссылки на другие темы"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('\n', 2)
    if len(parts) < 3:
        return
    
    header = parts[0] + '\n' + parts[1]
    body = parts[2]
    
    def replace_match(match):
        word = match.group(0).lower()
        return f"[{match.group(0)}]({reverse_map[word]})"
    
    pattern = re.compile(
        r'\b(' + '|'.join(re.escape(word) for words in topics.values() for word in words) + r')\b',
        flags=re.IGNORECASE
    )
    
    new_body = pattern.sub(replace_match, body)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header + '\n' + new_body)

def send_message(access_token, label, topic, topics):
    """Функция для отправки сообщения в ГигаЧат"""
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    prompt = (
        f'Привет, можешь объяснить на русском что такое "{label}". '
        f'Вот тебе небольшой текст с английской википедии: "{topic}". '
        f'Перепеши его, будто объясняешь это для 10 летнего ребенка (на русском) '
        f'и развей мысль. Ну и не пиши "Привет" и прочие вещи, просто выведи '
        f'то, что я прошу. Объем должен быть минимум 1000 символов, можно больше. '
        f'Твой ответ должен иметь определенную структуру (учти, что ответ должен '
        f'быть в формате md файла, приведи весь текст грамотно к этому формату). '
        f'Сделай его в формате небольшой статьи (и не забудь, что она должна быть '
        f'такой, будто ты говоришь все это 10 летнему ребенку).'
    )

    payload = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Ответ не найден")
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"Ошибка запроса: {str(e)}"

def insert_links_in_related_terms(related_terms, article_mapping, topics):
    """Вставляет ссылки на связанные термины в конце статьи"""
    
    links = []
    for term in related_terms:
        term_lower = term.lower()
        if term_lower in article_mapping:
            link = f"[{term}](./{article_mapping[term_lower]})"
            links.append(link)
        else:
            for key, value in topics.items():
                if term.lower() in value:
                    link = f"[{term}](./{key.replace(' ', '_')}.md)"
                    links.append(link)
                    break
            else:
                links.append(term)
    return ", ".join(links)

def main():
    # Читаем токен из файла
    with open("token.txt", "r") as file:
        access_token = file.read().strip()

    # Читаем JSON-файл с темами
    topics = load_topics("topics.json")

    # Создаём папку для статей
    articles_dir = "Articles"

    if os.path.exists(articles_dir):
        shutil.rmtree(articles_dir)

    os.makedirs(articles_dir, exist_ok=True)

    # 1. Создание всех Markdown-файлов
    article_mapping = {}

    for label in topics.keys():
        topic = topics[label]
        response_text = send_message(access_token, label, topic, topics)
        
        
        file_name = f"{label.replace(' ', '_')}.md"
        file_path = os.path.join(articles_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as md_file:
            md_file.write(f"# {label}\n\n{response_text}")

        article_mapping[label.lower()] = file_name
        print(f"Сохранён файл: {file_path}")

    # 2. Добавляем автоматические ссылки в тексты статей
    reverse_map = create_reverse_mapping(topics)
    for filename in os.listdir(articles_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(articles_dir, filename)
            add_links_to_md(file_path, reverse_map, topics)
            print(f"Добавлены ссылки в {filename}")

    # 3. Обновляем секции "Связанные термины"
if __name__ == '__main__':
    main()
