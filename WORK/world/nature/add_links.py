import json
import re
from pathlib import Path


with open('concept.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)['concepts']


term_to_file = {term: Path(path).stem for term, path in concepts.items()}


sorted_terms = sorted(term_to_file.keys(), key=lambda x: -len(x))

def process_file(filepath, current_concept):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = content
    
    for term in sorted_terms:
        if term != current_concept:
            file_name = term_to_file[term]
            pattern = re.compile(rf'(\b{re.escape(term)}\b)', re.IGNORECASE)
            def replace_match(match):
                original_word = match.group(1)
                # Если слово уже является ссылкой, не изменяем его
                if re.search(r'\[.*\]\(.*\)', original_word):
                    return original_word
                return f'[{original_word}]({file_name}.md)'
            
            modified_content = pattern.sub(replace_match, modified_content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        return True
    return False


for concept_name, filepath in concepts.items():
    full_path = Path(filepath)
    if full_path.exists():
        if process_file(full_path, concept_name):
            print(f"Обновлён: {filepath} (добавлены ссылки)")
        else:
            print(f"Без изменений: {filepath}")
    else:
        print(f"Файл не найден: {filepath}")

print("Обработка завершена!")