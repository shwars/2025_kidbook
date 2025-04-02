import os
import re
import pymorphy3
import json

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

# Чтение списка концептов из файла concepts.json
with open('concepts.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

concepts = json_data.get("concepts", [])

normalized_terms = {}
for concept in concepts:
    file_name = f"{concept.replace(' ', '_')}.md"
    link = f"{file_name}"
    norm = morph.parse(concept)[0].normal_form
    normalized_terms[norm] = (concept, link)

word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
# md_link_pattern – для поиска markdown-ссылок вида [текст](URL)
md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def replace_match(match):
    """
    Если слово соответствует одному из концептов (по нормальной форме), заменяем его на markdown-ссылку.
    Используется для фрагментов, которые не находятся внутри уже существующих markdown-ссылок.
    """
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form
    if lemma in normalized_terms:
        term, new_link = normalized_terms[lemma]
        return f"[{word}]({new_link})"
    return word

def update_markdown_link(link_text, old_url):
    """
    Обновляет markdown-ссылку. Если текст ссылки соответствует концепту,
    возвращает ссылку с актуальным URL (с новой директорией /concepts).
    """
    lemma = morph.parse(link_text)[0].normal_form
    if lemma in normalized_terms:
        term, new_link = normalized_terms[lemma]
        return f"[{link_text}]({new_link})"
    return f"[{link_text}]({old_url})"

def process_line(line):
    """
    Обрабатывает строку: если строка не является заголовком,
    то обновляет все найденные markdown-ссылки и заменяет слова вне ссылок.
    """
    # Если строка является заголовком, возвращаем её без изменений
    if header_pattern.match(line):
        return line

    parts = re.split(r'(\[[^\]]+\]\([^)]+\))', line)
    new_parts = []
    for part in parts:
        # Если часть соответствует markdown-ссылке, обновляем её
        md_match = md_link_pattern.fullmatch(part)
        if md_match:
            link_text = md_match.group(1)
            old_url = md_match.group(2)
            new_parts.append(update_markdown_link(link_text, old_url))
        else:
            new_parts.append(word_pattern.sub(replace_match, part))
    return "".join(new_parts)

def process_markdown_file(file_path):
    """Обрабатывает Markdown-файл, обновляя ссылки в каждой строке."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        updated_lines.append(process_line(line))

    updated_content = "".join(updated_lines)
    if updated_content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

directory = "../../../KIDBOOK/learning/knowledge_structure/concepts"
md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

# Обрабатываем все Markdown-файлы в указанной директории
for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")
