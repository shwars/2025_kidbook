import json
import os
import re
import argparse
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

def generate_forms(phrase):
    words = phrase.split()
    if len(words) > 1:
        return [phrase]
    forms = set()
    parsed = morph.parse(phrase)[0]
    if 'NOUN' not in parsed.tag:
        return [phrase]
    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'plur']
    for case in cases:
        try:
            form = parsed.inflect({case}).word
            forms.add(form)
        except:
            continue
    return list(forms) + [phrase]

def build_concept_dict(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    concept_dict = {}
    for category in data.values():
        for concept in category.get('concepts', []):
            forms = generate_forms(concept['name'])
            for form in forms:
                concept_dict[form] = concept['file']
    return concept_dict

def replace_concepts(content, concept_map, current_file):
    sorted_concepts = sorted(concept_map.items(),
                            key=lambda x: len(x[0]),
                            reverse=True)
    link_pattern = re.compile(r'(\[[^]]+\]\([^)]+\))')
    parts = link_pattern.split(content)

    for i in range(0, len(parts), 2):
        text_part = parts[i]
        for word, file in sorted_concepts:
            if file == current_file:
                continue
            pattern = rf'(?<!\w){re.escape(word)}(?![\w.])'
            text_part = re.sub(
                pattern,
                lambda m: f'[{m.group(0)}]({file})',
                text_part,
                flags=re.IGNORECASE
            )
        parts[i] = text_part

    return ''.join(parts)

def main():
    parser = argparse.ArgumentParser(description='Smart concept linking')
    parser.add_argument('json_file', help='Path to concepts JSON')
    parser.add_argument('md_dir', help='Directory with markdown files')
    args = parser.parse_args()
    concept_map = build_concept_dict(args.json_file)

    for filename in os.listdir(args.md_dir):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(args.md_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = replace_concepts(content, concept_map, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == '__main__':
    main()
