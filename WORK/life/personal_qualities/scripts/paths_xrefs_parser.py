import os
import json
import re
from pathlib import Path

concepts = [
    "Доброта", "Смелость", "Честность", "Щедрость", "Эмпатия",
    "Лень", "Лицемерие", "Жадность", "Вспыльчивость", "Высокомерие",
    "Сдержанность", "Любопытство", "Замкнутость", "Терпение", "Ответственность"
]

script_dir = Path(__file__).resolve().parent
kid_book_directory_path = script_dir / '../../../../KIDBOOK/life/personal_qualities'
output_json_path = script_dir / '../data/concepts.json'

def find_links(content):
    normalized_concepts = {c.lower(): c for c in concepts}
    matches = re.findall(r'\[.*?\]\((?:\./)?(.*?\.md)\)', content)
    
    unique_links = set()
    
    for match in matches:
        filename = os.path.basename(match)
        base_name = os.path.splitext(filename)[0]
        
        if base_name.lower() in normalized_concepts:
            original_name = normalized_concepts[base_name.lower()] + ".md"
            unique_links.add(original_name)
    
    return list(unique_links)

def generate_concepts_json():
    md_dir = kid_book_directory_path.resolve()
    
    result = {
        "categories": {},
        "links": {}
    }

    for concept in concepts:
        md_file = f'{concept}.md'
        md_path = md_dir / md_file
        
        rel_path = os.path.relpath(md_path, output_json_path.parent)
        result["categories"][concept] = rel_path.replace('\\', '/')

        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                links = find_links(content)
                result["links"][md_file] = links
        except FileNotFoundError:
            print(f'Warning: File {md_file} not found')
            result["links"][md_file] = []

    return result

if __name__ == "__main__":
    data = generate_concepts_json()
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'Successfully generated {output_json_path}')