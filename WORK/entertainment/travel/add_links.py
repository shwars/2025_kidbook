import os
import re
import json

# Загрузка словаря определений из JSON-файла
with open('WORK/entertainment/travel/definitions.json',
          'r', encoding='utf-8') as file:
    definitions_dict = json.load(file)

base_dir = 'KIDBOOK/entertainment/travel/concepts'


# Функция для обработки одного файла
def process_file(file_name):
    file_path = os.path.join(base_dir, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().lower()

    # Ищем все слова, которые присутствуют в словаре определений
    for word, link in definitions_dict.items():
        word = word.lower()
        word_regex = r'\b' + re.escape(word) + r'\b'

        # Если слово найдено в тексте, заменяем его на ссылку
        content = re.sub(word_regex, f'[{word}]({link})', content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Файл '{file_name}' обновлен.")


for file_name in os.listdir(base_dir):
    if file_name.endswith('.md'):
        process_file(file_name)
