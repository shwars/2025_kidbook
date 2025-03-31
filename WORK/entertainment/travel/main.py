import os
import re

definitions_dict = {
    'автопутешествие': 'autotravel.md',
    'авиация': 'avia.md',
    'бэкпекинг': 'backpacking.md',
    'велосипед': 'bicycle.md',
    'судно': 'boat.md',
    'бомж-тур': 'bomj.md',
    'Автомобиль': 'car.md',
    'Чемодан': 'chemod.md',
    'Круиз': 'cruise.md',
    'Снаряжение': 'gear.md',
    'Рюкзак': 'knapsack.md',
    'Багаж': 'luggage.md',
    'Свадебное путешествие': 'merriage.md',
    'Поезд': 'train.md',
    'Транспорт': 'transport.md',
    'Путешествия': 'travel.md',
    'Виды путешествий': 'types.md',
    'Велосипедный отпуск': 'velotravel.md',
    'Кругосветное путешествие': 'world.md'

}

base_dir = '2025_kidbook/KIDBOOK/entertainment/travel'


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
