import os
import re
import pymorphy3
import json

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Чтение файла категорий (графовая сущность зависимостей)
with open('categories.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Формирование словаря: ключ — нормальная форма термина, значение — кортеж (оригинальный термин, ссылка)
normalized_terms = {}
for term, data in json_data["categories"].items():
    if isinstance(data, dict):
        link = data.get("link", "")
    else:
        link = data
    normalized_terms[morph.parse(term)[0].normal_form] = (term, link)

# Регулярные выражения для поиска слов, заголовков и уже связанных участков
word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
linked_text_pattern = re.compile(r'\[.*?\]\(.*?\)')

def replace_match(match):
    """Заменяет найденное слово на markdown-ссылку, если оно присутствует в normalized_terms."""
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form
    if lemma in normalized_terms:
        term, link = normalized_terms[lemma]
        return f"[{word}]({link})"
    return word

def process_markdown_file(file_path):
    """Обрабатывает Markdown-файл, добавляя ссылки, за исключением заголовков и уже связанных частей."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        # Если строка является заголовком или содержит уже существующую ссылку, оставляем её без изменений
        if header_pattern.match(line) or linked_text_pattern.search(line):
            updated_lines.append(line)
        else:
            updated_line = word_pattern.sub(replace_match, line)
            updated_lines.append(updated_line)

    updated_content = "".join(updated_lines)
    if updated_content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

# Задаем директорию, где находятся Markdown-файлы для темы "структурирование знаний"
directory = "../../../KIDBOOK/learning/knowledge_structure/concepts"
md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

# Обрабатываем все Markdown-файлы в указанной директории
for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")
