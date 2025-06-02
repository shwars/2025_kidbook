import os
import re
from pymorphy3 import MorphAnalyzer

# Папка с Markdown файлами
FOLDER_PATH = "pages"  # Укажи свою папку

# Инициализация морфологического анализатора
morph = MorphAnalyzer()

# Функция для чтения всех файлов в папке
def read_markdown_files(folder):
    articles = {}
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                articles[filename] = content
    return articles

# Функция для извлечения ключевых слов (заголовков) из статей
def extract_keywords(articles):
    keywords = {}
    for filename, content in articles.items():
        # Берем заголовок из первой строки
        match = re.search(r"^# (.+)", content, re.MULTILINE)
        if match:
            keyword = match.group(1).strip().lower()  # Ключевое слово — это заголовок статьи в нижнем регистре
            keywords[keyword] = filename
    return keywords

# Функция для лемматизации слова с использованием pymorphy2
def lemmatize_word(word):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form

# Функция для замены ключевых слов на ссылки с учетом падежей и заглавных букв
def insert_links(articles, keywords):
    updated_articles = {}
    for filename, content in articles.items():
        # Разбиваем текст на слова, сохраняя их оригинальный вид для дальнейшей замены
        words = re.findall(r'\b\w+\b', content)
        for word in words:
            lemma_word = lemmatize_word(word.lower())  # Лемматизируем слово для учета падежей и чисел
            if lemma_word in keywords and keywords[lemma_word] != filename:
                # Если слово найдено в ключевых словах, заменяем его на ссылку
                content = re.sub(rf'\b{re.escape(word)}\b', f"[{word}]({keywords[lemma_word]})", content)
        updated_articles[filename] = content
    return updated_articles

# Функция для сохранения обновленных файлов
def save_updated_files(folder, updated_articles):
    for filename, content in updated_articles.items():
        path = os.path.join(folder, filename)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

# Основная логика
articles = read_markdown_files(FOLDER_PATH)
keywords = extract_keywords(articles)
updated_articles = insert_links(articles, keywords)
save_updated_files(FOLDER_PATH, updated_articles)

print("Success!")
