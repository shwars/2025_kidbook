import json
import os
import re
import pymorphy2


with open("concepts.json", "r", encoding="utf-8") as f:
    concepts = json.load(f)["categories"]


morph = pymorphy2.MorphAnalyzer()

def get_word_forms(word):
    """Генерирует возможные формы слова для поиска в тексте."""
    parsed_word = morph.parse(word)[0]
    word_forms = {parsed_word.normal_form}  
    word_forms.update({form.word for form in parsed_word.lexeme})  
    return word_forms

def add_links(text, concepts):
    """Добавляет ссылки к понятиям в тексте, учитывая их формы."""
    for term, url in concepts.items():
        word_forms = get_word_forms(term)
        for form in sorted(word_forms, key=len, reverse=True):  
            pattern = rf"(?<!\[)\b{re.escape(form)}\b(?!\])"
            replacement = f"[{form}]({url})"
            text = re.sub(pattern, replacement, text)
    return text

def process_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                updated_text = add_links(text, concepts)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_text)


directory = "../../../KIDBOOK/entertainment/active_games/concepts"
process_files(directory)
