import os
import re
import json
import pymorphy3

def load_concepts(concepts_path):
    with open(concepts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    morph = pymorphy3.MorphAnalyzer()
    normalized = {}
    for term, link in data.get("categories", {}).items():
        lemma = morph.parse(term)[0].normal_form
        normalized[lemma] = (term, link)
    return normalized, morph

def is_header(line):
    return bool(re.match(r'^\s{0,3}#{1,6}\s', line))

def contains_link(line):
    return bool(re.search(r'\[.*?\]\(.*?\)', line))

def link_word(word, normalized_terms, morph):
    lemma = morph.parse(word)[0].normal_form
    if lemma in normalized_terms:
        original, link = normalized_terms[lemma]
        return f'[{word}]({link})'
    return word

def process_line(line, normalized_terms, morph):
    if is_header(line) or contains_link(line):
        return line
    else:
        return re.sub(r'\b[А-Яа-яЁё-]+\b', lambda m: link_word(m.group(0), normalized_terms, morph), line)

def process_markdown_file(file_path, normalized_terms, morph):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = [process_line(line, normalized_terms, morph) for line in lines]

    if processed_lines != lines:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)

def main():
    concepts_path = '/home/sestroedinson/2025_kidbook/WORK/world/peoples_of_the_world/concepts.json'
    directory = '/home/sestroedinson/2025_kidbook/KIDBOOK/world/peoples_of_the_world/'

    normalized_terms, morph = load_concepts(concepts_path)

    md_files = [f for f in os.listdir(directory) if f.endswith('.md')]
    for md_file in md_files:
        full_path = os.path.join(directory, md_file)
        process_markdown_file(full_path, normalized_terms, morph)

    print('Обновление ссылок завершено.')

if __name__ == '__main__':
    main()