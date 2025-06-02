import os
import json
import re
import pymorphy3
import generate_texts

morph = pymorphy3.MorphAnalyzer()
script_dir = os.path.dirname(os.path.abspath(__file__))
kidbook_path = os.path.join(script_dir, "..", "..", "KIDBOOK")

with open("concepts.json", "r", encoding="utf-8") as f:
    concepts = json.load(f)["concepts"]

titles = [i['name'] for i in concepts]
titles_files = {i['name']: i['file'] for i in concepts}
files = [i['file'] for i in concepts]

for path in files:
    result = ''
    with open(os.path.join(kidbook_path, path), "r") as f:
        text = f.read()
        words = re.findall(r'\w+|\W+', text)
    
        for i, word in enumerate(words):
            if word.strip() and word.isalpha():  # Проверяем, что это слово (не пунктуация/число)
                parsed = morph.parse(word)[0]
                if parsed.normal_form.capitalize() in titles:
                    if titles_files[parsed.normal_form.capitalize()] != path:
                        words[i] = f"[{word}]({titles_files[parsed.normal_form.capitalize()]})"
        result = ''.join(words)
    
    generate_texts.save_string_to_file(result, os.path.join(kidbook_path, path))
