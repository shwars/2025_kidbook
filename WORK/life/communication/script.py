import os
import json
import re

# Загрузка понятий из concepts_clean.json
def load_concepts(concepts_file):
    with open(concepts_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Поиск и замена упоминаний понятий на ссылки
def replace_with_links(text, concepts):
    for concept, file_name in concepts.items():
        # Создаем регулярное выражение для поиска слова с учетом падежей
        pattern = rf'\b{re.escape(concept)}\w*\b'
        # Заменяем все вхождения на Markdown-ссылку
        text = re.sub(pattern, rf'[{concept}]({file_name})', text, flags=re.IGNORECASE)
    return text

# Обработка всех Markdown-файлов
def process_markdown_files(directory, concepts):
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Заменяем упоминания понятий на ссылки
            updated_content = replace_with_links(content, concepts)

            # Сохраняем обновленный текст
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

# Основная функция
def main():
    # Путь к файлу concepts_clean.json
    concepts_file = 'WORK/concepts_clean.json'
    # Путь к директории с Markdown-файлами
    markdown_directory = 'KIDBOOK'

    # Загружаем понятия
    concepts = load_concepts(concepts_file)

    # Обрабатываем Markdown-файлы
    process_markdown_files(markdown_directory, concepts)

if __name__ == '__main__':
    main()