import os
import json
import re

# Загружаем список понятий
with open("WORK/concepts.json", "r", encoding="utf-8") as f:
    concepts = json.load(f)

# Функция для добавления ссылок в текст
def add_links(text, concepts):
    for concept in concepts:
        term = concept["name"]
        link = f"[{term}]({concept['file']})"
        text = re.sub(rf"\b{term}\b", link, text)
    return text

# Обрабатываем все markdown-файлы
for filename in os.listdir("pages"):
    if filename.endswith(".md"):
        filepath = os.path.join("pages", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = add_links(content, concepts)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

print("Ссылки успешно расставлены!")
