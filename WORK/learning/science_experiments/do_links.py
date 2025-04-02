import os
import re
import json
import pymorphy3
from itertools import product

def load_keywords_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_all_md_files(root_directory):
    md_files = []
    for dirpath, _, filenames in os.walk(root_directory):
        for file in filenames:
            if file.endswith(".md"):
                md_files.append(os.path.join(dirpath, file))
    return md_files

def generate_word_forms(word, morph):
    parsed = morph.parse(word)[0]
    return set(word_form.word for word_form in parsed.lexeme)

def generate_phrase_forms(phrase, morph):
    words = phrase.split()
    word_forms = [generate_word_forms(word, morph) for word in words]
    phrase_forms = {" ".join(combo) for combo in product(*word_forms)}
    return phrase_forms

def add_links_to_markdown(root_directory, keywords_map):
    morph = pymorphy3.MorphAnalyzer()
    
    all_md_files = get_all_md_files(root_directory)
    
    for target_file, keywords in keywords_map.items():
        relative_target_path = "../" + os.path.relpath(target_file, root_directory) 
        
        for filepath in all_md_files:
            if filepath == target_file:
                continue 
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            for keyword in keywords:
                word_forms = generate_phrase_forms(keyword, morph)
                for form in word_forms:
                    pattern = rf"(?<!\[)\b({re.escape(form)})\b(?!\])"
                    replacement = rf"[\1]({relative_target_path})"
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            
            print(f"Обновлен файл: {filepath}")

concepts_path = "concepts.json"
root_directory = "../../../KIDBOOK/learning/science_experiments"

keywords = load_keywords_from_json(concepts_path)

add_links_to_markdown(root_directory, keywords)
