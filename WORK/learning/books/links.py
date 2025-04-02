import os
import json
import pymorphy3
import re

md_directory = '../../../KIDBOOK/learning/books'

with open('conepts/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

morph = pymorphy3.MorphAnalyzer()


def get_link_for_concept(concept_name):
    return concepts.get(concept_name, {}).get('ссылка', '')


def normalize_word(word):
    return morph.parse(word)[0].normal_form


def add_links_to_md_files():
    for root, dirs, files in os.walk(md_directory):
        for file in files:
            if file == 'index.md':
                continue

            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            word_variants = {}
            words_in_text = re.findall(r'\b\w+\b', content)

            for word in words_in_text:
                norm_word = normalize_word(word)
                if norm_word not in word_variants:
                    word_variants[norm_word] = []
                word_variants[norm_word].append(word)

            print(f"Обрабатываем файл: {file}")
            print(f"Нормализованные слова в тексте: {word_variants.keys()}")

            modified = False

            for concept, data in concepts.items():
                normalized_concept = normalize_word(concept)
                link = get_link_for_concept(concept)

                if not link or os.path.basename(link) == file:
                    continue

                if normalized_concept in word_variants:
                    print(f"Найдено совпадение: {concept} -> {link}")

                    for variant in set(word_variants[normalized_concept]):
                        pattern = rf'\b{re.escape(variant)}\b'
                        replacement = f'[{variant}]({link})'
                        content, count = re.subn(pattern, replacement, content)
                        if count > 0:
                            modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Файл {file_path} изменен.")
            else:
                print(f"Файл {file_path} не был изменен.")


add_links_to_md_files()
