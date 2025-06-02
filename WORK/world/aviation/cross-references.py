import os
import re
import pymorphy3
import json

morph = pymorphy3.MorphAnalyzer()

with open('concepts.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

normalized_terms = {
    morph.parse(term)[0].normal_form: (term, path)
    for term, path in json_data["categories"].items()
}

word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
linked_text_pattern = re.compile(r'\[.*?\]\(.*?\)')


def replace_match(match):
    """ Функция для замены слов на ссылки """
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form

    if lemma in normalized_terms:
        term, link = normalized_terms[lemma]
        return f"[{word}]({link})"

    return word


def process_markdown_file(file_path):
    """ Обрабатывает Markdown-файл, добавляя ссылки, кроме заголовков. """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if header_pattern.match(line) or linked_text_pattern.search(line):
            updated_lines.append(line)
        else:
            updated_line = word_pattern.sub(replace_match, line)
            updated_lines.append(updated_line)

    updated_content = "".join(updated_lines)
    if updated_content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)


directory = "c:/MAI/2025_kidbook/KIDBOOK/world/aviation"
md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")