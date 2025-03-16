import os
import re

# Папка с Markdown файлами
FOLDER_PATH = "pages"  # Укажи свою папку

# Регулярное выражение для поиска Markdown-ссылок
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")

# Функция для обработки текста
def remove_markdown_links(content):
    return re.sub(LINK_PATTERN, r"\1", content)

# Функция для обработки всех файлов в папке
def process_markdown_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            new_content = remove_markdown_links(content)

            with open(path, "w", encoding="utf-8") as file:
                file.write(new_content)

# Запускаем обработку
process_markdown_files(FOLDER_PATH)

print("✅ Все ссылки удалены, оставлен только текст!")
