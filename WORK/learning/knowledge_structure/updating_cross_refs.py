import os
import re
import json
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

MAPPING_FILE = 'mapping.json'
TARGET_DIRECTORY = "../../../KIDBOOK/learning/knowledge_structure/concepts"


with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
    mapping = json.load(f)


normalized_mapping = {}
for russian_name, new_file in mapping.items():
    norm = morph.parse(russian_name)[0].normal_form
    normalized_mapping[norm] = new_file


print("Новый маппинг для ссылок:")
print(normalized_mapping)

def rename_files_in_directory(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".md"):
            base_name, ext = os.path.splitext(file_name)
            norm = morph.parse(base_name)[0].normal_form
            if norm in normalized_mapping:
                new_file_name = normalized_mapping[norm]
                old_path = os.path.join(directory, file_name)
                new_path = os.path.join(directory, new_file_name)
                os.rename(old_path, new_path)
                print(f"Переименован: '{file_name}' -> '{new_file_name}'")
            else:
                print(f"Файл '{file_name}' не найден в маппинге, пропускаем.")


word_pattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
header_pattern = re.compile(r'^\s{0,3}#{1,6}\s')
# 3. Markdown-ссылки вида [текст](URL)
md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def replace_word(match):
    """
    Если слово соответствует одному из концептов (по нормальной форме),
    заменяем его на ссылку с новым именем файла.
    """
    word = match.group(0)
    lemma = morph.parse(word)[0].normal_form
    if lemma in normalized_mapping:
        new_file = normalized_mapping[lemma]
        return f"[{word}]({new_file})"
    return word

def update_md_link(link_text, old_url):
    """
    Если текст ссылки соответствует концепту, обновляем URL ссылки.
    """
    lemma = morph.parse(link_text)[0].normal_form
    if lemma in normalized_mapping:
        new_file = normalized_mapping[lemma]
        return f"[{link_text}]({new_file})"
    return f"[{link_text}]({old_url})"

def process_line(line):
    """
    Обрабатывает строку:
    - Если строка – заголовок, возвращаем без изменений.
    - Иначе разбиваем строку на части (markdown-ссылки и обычный текст)
      и обрабатываем каждую часть.
    """
    if header_pattern.match(line):
        return line

    parts = re.split(r'(\[[^\]]+\]\([^)]+\))', line)
    new_parts = []
    for part in parts:
        md_match = md_link_pattern.fullmatch(part)
        if md_match:
            link_text = md_match.group(1)
            old_url = md_match.group(2)
            new_parts.append(update_md_link(link_text, old_url))
        else:
            new_parts.append(word_pattern.sub(replace_word, part))
    return "".join(new_parts)

def process_markdown_file(file_path):
    """
    Обрабатывает файл: обновляет все строки и перезаписывает файл,
    если были изменения.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = [process_line(line) for line in lines]
    updated_content = "".join(updated_lines)
    if updated_content != "".join(lines):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

rename_files_in_directory(TARGET_DIRECTORY)

md_files = [f for f in os.listdir(TARGET_DIRECTORY) if f.endswith(".md")]
for md_file in md_files:
    process_markdown_file(os.path.join(TARGET_DIRECTORY, md_file))

print("Переименование файлов и обновление ссылок завершено.")
