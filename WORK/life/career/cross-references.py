import os
import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

json_data = {
    "categories": {
        "профессия": "Профессия.md",
        "работа": "Профессия.md",
        "деятельность": "Профессия.md",
        "специальность": "Специальность.md",
        "профиль": "Специальность.md",
        "направление": "Специальность.md",

        "образование": "Образование.md",
        "учеба": "Образование.md",
        "обучение": "Образование.md",
        "вуз": "Образование.md",

        "навыки": "Навыки.md",
        "умения": "Навыки.md",
        "способности": "Навыки.md",

        "опыт": "Опыт работы.md",
        "практика": "Опыт работы.md",
        "стаж": "Опыт работы.md",

        "резюме": "Резюме.md",
        "анкета": "Резюме.md",
        "cv": "Резюме.md",

        "карьера": "Карьерный рост.md",
        "продвижение": "Карьерный рост.md",
        "развитие": "Карьерный рост.md",

        "зарплата": "Зарплата.md",
        "доход": "Зарплата.md",
        "заработок": "Зарплата.md",

        "предприниматель": "Предприниматель.md",
        "бизнесмен": "Предприниматель.md",
        "стартап": "Предприниматель.md",

        "работодатель": "Работодатель.md",
        "наниматель": "Работодатель.md",
        "компания": "Работодатель.md",

        "стажировка": "Стажировка.md",
        "практика": "Стажировка.md",
        "ученичество": "Стажировка.md",

        "профориентация": "Профориентация.md",
        "выбор профессии": "Профориентация.md",
        "тесты": "Профориентация.md",

        "фриланс": "Фриланс.md",
        "удаленка": "Фриланс.md",
        "свободный график": "Фриланс.md",

        "договор": "Трудовой договор.md",
        "контракт": "Трудовой договор.md",
        "трудоустройство": "Трудовой договор.md",

        "мечта": "Мечта.md",
        "цель": "Мечта.md",
        "планы": "Мечта.md"
    }
}

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


directory = "../../../KIDBOOK/life/career/concepts"
md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

for md_file in md_files:
    process_markdown_file(os.path.join(directory, md_file))

print("Обновление ссылок завершено.")
