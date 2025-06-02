import json
import os
import re
from typing import Dict, List

def load_topics(topics_path: str) -> Dict[str, List[str]]:
    """Загружает словарь тем из JSON файла"""
    with open(topics_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_reverse_mapping(topics: Dict[str, List[str]]) -> Dict[str, str]:
    """Создает обратное отображение: слово -> имя файла"""
    reverse_map = {}
    for file_name, words in topics.items():
        md_file_name = f"{file_name}.md"
        for word in words:
            reverse_map[word.lower()] = f"./{md_file_name}"
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
    
    # Регулярное выражение для поиска существующих ссылок
    link_pattern = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
    
    # Находим все уже существующие ссылки
    existing_links = set()
    for match in link_pattern.finditer(body):
        existing_links.add(match.group(1).lower())
    
    def replace_match(match):
        word = match.group(0).lower()
        # Если слово уже является частью ссылки или нет в reverse_map
        if word in existing_links or word not in reverse_map:
            return match.group(0)
        return f"[{match.group(0)}]({reverse_map[word]})"
    
    # Создаем регулярное выражение для всех слов из topics.json
    all_words = [re.escape(word) for words in topics.values() for word in words]
    word_pattern = re.compile(r'\b(' + '|'.join(all_words) + r')\b', flags=re.IGNORECASE)
    
    # Заменяем только слова, не находящиеся внутри ссылок
    new_body = word_pattern.sub(replace_match, body)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header + '\n' + new_body)

def add_links():
    """Добавляет ссылки в сгенерированные статьи"""
    topics = load_topics("topics.json")
    articles_dir = "Articles"
    reverse_map = create_reverse_mapping(topics)
    
    for filename in os.listdir(articles_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(articles_dir, filename)
            add_links_to_md(file_path, reverse_map, topics)
            print(f"Обработан файл: {filename}")

if __name__ == '__main__':
    add_links()