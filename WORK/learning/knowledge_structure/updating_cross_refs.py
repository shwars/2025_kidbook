import os
import re
import pymorphy3
import json

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Чтение списка концептов из файла concepts.json
with open('concepts.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Получаем список концептов из ключа "concepts"
concepts = json_data.get("concepts", [])

# Формируем словарь: ключ – нормальная форма понятия, значение – (оригинальное название, ссылка)
# Ссылка формируется как "KIDBOOK/learning/knowledge_structure/<название_без_пробелов>.md"
normalized_terms = {}
for concept in concepts:
    # Замена пробелов на подчеркивания для формирования имени файла
    file_name = f"{concept.replace(' ', '_')}.md"
    link = f"KIDBOOK/learning/knowledge_structure/{file_name}"
    norm = morph.parse(concept)[0].normal_form
    normalized_terms[norm] = (concept, link)

# Регулярные выражения:
# word_pattern – находит отдельные слова
# header_pattern – определяет заголовки (начинающиеся с #)
# linked_text_pattern – определяет уже существующие markdown-ссылки
word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
linked_text_pattern = re.compile(r'\[.*?\]\(.*?\)')

def replace_match(match):
    """Если слово соответствует одному из концептов (по нормальной форме), заменяем его на markdown-ссылку."""
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form
    if lemma in normalized_terms:
        term, link = normalized_terms[lemma]
        return f"[{word}]({link})"
    return word

def process_markdown_file(file_path):
    """Обрабатывает Markdown-файл, заменяя все встречающиеся понятия на ссылки, за исключением заголовков и уже связанных фрагментов."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        # Если строка – заголовок или уже содержит ссылку, оставляем её без изменений
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

# Обрабатываем все файлы в указанной директории
for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")
