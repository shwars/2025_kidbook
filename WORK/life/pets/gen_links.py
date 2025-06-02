import json
import os
import re
import argparse
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

def generate_forms(phrase):
    """Генерирует грамматические формы с улучшенной обработкой составных терминов"""
    words = phrase.split()
    if len(words) > 1:
        # Для составных терминов генерируем формы для каждого слова
        forms = set()
        base_words = []
        for word in words:
            parsed = morph.parse(word)[0]
            if 'NOUN' in parsed.tag:
                cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'plur']
                word_forms = {word}
                for case in cases:
                    try:
                        form = parsed.inflect({case}).word
                        word_forms.add(form)
                    except:
                        continue
                base_words.append(list(word_forms))
            else:
                base_words.append([word])
        
        # Генерируем комбинации форм слов
        from itertools import product
        for combo in product(*base_words):
            forms.add(' '.join(combo))
        return list(forms)
    else:
        # Одиночные слова
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
    """Строит словарь терминов с улучшенной обработкой животных"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    concept_dict = {}
    for category in data.values():
        for concept in category.get('concepts', []):
            forms = generate_forms(concept['name'])
            for form in forms:
                # Нормализация ключа (регистр и пробелы)
                normalized_form = ' '.join(form.lower().split())
                concept_dict[normalized_form] = concept['file']
                
                # Добавляем варианты с "для" (например, "корм для кошек")
                if concept['name'] in ['Корм', 'Игрушки', 'Аксессуары']:
                    concept_dict[f"{normalized_form} для"] = concept['file']
                    
    return concept_dict

def replace_concepts(content, concept_map, current_file):
    """Улучшенная замена терминов с учетом специфики животных"""
    sorted_concepts = sorted(concept_map.items(),
                            key=lambda x: (-len(x[0]), x[0]))  # Сначала длинные, потом по алфавиту
    
    # Игнорируем существующие ссылки и код
    link_pattern = re.compile(r'(\[[^]]+\]\([^)]+\)|`[^`]+`|```[\s\S]+?```)')
    parts = link_pattern.split(content)
    
    # Специальные обработки для животных
    animal_terms = {'собака', 'кошка', 'попугай', 'хомяк'}
    
    for i in range(0, len(parts), 2):
        text_part = parts[i]
        for word, file in sorted_concepts:
            if file == current_file:
                continue
                
            # Особые правила для животных
            if word in animal_terms:
                pattern = rf'(?<!\w)({re.escape(word)}[\w]*)(?![\w.])'
            else:
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
    parser = argparse.ArgumentParser(description='Smart concept linking for pets articles')
    parser.add_argument('json_file', help='Path to pets concepts JSON')
    parser.add_argument('md_dir', help='Directory with markdown files about pets')
    args = parser.parse_args()
    
    print(f"Building concept map from {args.json_file}...")
    concept_map = build_concept_dict(args.json_file)
    print(f"Loaded {len(concept_map)} concept forms")
    
    processed_files = 0
    for filename in os.listdir(args.md_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(args.md_dir, filename)
        print(f"Processing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = replace_concepts(content, concept_map, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        processed_files += 1
    
    print(f"Done! Processed {processed_files} files.")

if __name__ == '__main__':
    main()
