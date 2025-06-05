import os
import re
import json
import pymorphy3
from pathlib import Path

# Инициализация
morph = pymorphy3.MorphAnalyzer()

# Пути
BASE_DIR = Path(__file__).parent
MD_DIR = BASE_DIR / "path_to_directory"
OUTPUT_DIR = BASE_DIR / "KIDBOOK_LINKED"
CONCEPTS_PATH = BASE_DIR / "concepts.json"

# Создаем выходную директорию
OUTPUT_DIR.mkdir(exist_ok=True)

# Загрузка concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts_data = json.load(f)

# Создаем словарь для поиска терминов
term_map = {}
for concept in concepts_data['concepts']:
    term = concept['name']
    file = concept['file']
    term_map[term.lower()] = file
    for alias in concept.get('aliases', []):
        term_map[alias.lower()] = file

# Генерация всех словоформ
all_forms = {}
for term in term_map.keys():
    try:
        parsed = morph.parse(term)[0]
        forms = {term}
        cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
        for case in cases:
            try:
                forms.add(parsed.inflect({case}).word.lower())
            except:
                pass
        try:
            plural = parsed.make_plural()
            forms.add(plural.word.lower())
            for case in cases:
                try:
                    forms.add(plural.inflect({case}).word.lower())
                except:
                    pass
        except:
            pass
        for form in forms:
            all_forms[form] = term_map[term]
    except:
        continue

# Функция для замены терминов на ссылки
def add_links(text):
    tokens = re.split(r'(\W+)', text)
    for i in range(len(tokens)):
        token = tokens[i]
        if token.isalpha():
            lower_token = token.lower()
            if lower_token in all_forms:
                linked = f"[{token}]({all_forms[lower_token]})"
                tokens[i] = linked
    return ''.join(tokens)

# Обработка всех .md файлов
for md_file in MD_DIR.glob('*.md'):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if not re.search(r'\[.*?\]\(.*?\)', content):
            linked_content = add_links(content)
            output_path = OUTPUT_DIR / md_file.name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(linked_content)
    except:
        continue