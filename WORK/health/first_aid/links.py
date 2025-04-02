import os
import re
import pymorphy2
from typing import Dict, List, Tuple

# --- Словарь понятий и шаблоны ссылок ---
CONCEPTS = {
    ("первая", "помощь"): "[[Основы первой помощи|{phrase}]]",
    ("сердечно", "легочная", "реанимация"): "[[Сердечно-легочная реанимация (СЛР)|{phrase}]]",
    ("тепловой",): "[[Тепловой и солнечный удар|{phrase}]]",
    ("солнечный",): "[[Тепловой и солнечный удар|{phrase}]]",
    "ожог": "[[Ожоги|{word}]]",
    "кровотечение": "[[Кровотечения|{word}]]",
    "кровь": "[[Кровотечения|{word}]]",
    "обморожение": "[[Обморожение|{word}]]",
    "обморок": "[[Потеря сознания|{word}]]",
    "шок": "[[Шоковое состояние|{word}]]",
    "эпилепсия": "[[Эпилептический припадок|{word}]]",
    "перелом": "[[Переломы|{word}]]",
    "аптечка": "[[Аптечка первой помощи|{word}]]",
    "отравление": "[[Отравления|{word}]]",
    "укус": "[[Укусы животных и насекомых|{word}]]",
    "травма": "[[Переломы|{word}]]",
    "слр": "[[Сердечно-легочная реанимация (СЛР)|СЛР]]"
}

morph = pymorphy2.MorphAnalyzer()

def prepare_concepts() -> Dict[Tuple[str, ...], Tuple[List[str], str]]:
    prepared = {}
    for key, value in CONCEPTS.items():
        if isinstance(key, tuple):
            lemmas = tuple(morph.parse(word.lower())[0].normal_form for word in key)
            prepared[lemmas] = (list(key), value)
        else:
            lemma = morph.parse(key.lower())[0].normal_form
            prepared[(lemma,)] = ([key], value)
    return dict(sorted(prepared.items(), key=lambda x: -len(x[0])))

prepared_concepts = prepare_concepts()

def tokenize(text: str) -> List[dict]:
    tokens = []
    for match in re.finditer(r'\b[\w-]+\b|[^\w\s]', text, re.UNICODE):
        token = match.group()
        start, end = match.span()
        lemma = None
        if token.isalnum():
            parsed = morph.parse(token.lower())
            lemma = parsed[0].normal_form if parsed else token.lower()
        tokens.append({'text': token, 'start': start, 'end': end, 'lemma': lemma})
    return tokens

def find_matches(tokens: List[dict]) -> List[dict]:
    matches = []
    i = 0
    while i < len(tokens):
        max_length = 0
        best_match = None
        best_template = None
        for concept_lemmas, (original_words, template) in prepared_concepts.items():
            length = len(concept_lemmas)
            if i + length > len(tokens):
                continue
            current_lemmas = [t['lemma'] for t in tokens[i:i + length]]
            if current_lemmas == list(concept_lemmas):
                if length > max_length:
                    max_length = length
                    best_match = original_words
                    best_template = template
        if best_match:
            phrase = ' '.join(t['text'] for t in tokens[i:i + max_length])
            matches.append({
                'start': tokens[i]['start'],
                'end': tokens[i + max_length - 1]['end'],
                'replacement': best_template.format(
                    phrase=phrase,
                    word=tokens[i]['text']
                )
            })
            i += max_length
        else:
            i += 1
    return matches

def apply_replacements(text: str, matches: List[dict]) -> str:
    offset = 0
    for match in sorted(matches, key=lambda x: x['start']):
        original = text[match['start'] + offset:match['end'] + offset]
        replacement = match['replacement']
        text = text[:match['start'] + offset] + replacement + text[match['end'] + offset:]
        offset += len(replacement) - len(original)
    return text

def process_text(text: str) -> str:
    tokens = tokenize(text)
    matches = find_matches(tokens)
    return apply_replacements(text, matches)
def process_markdown_files(source_dir: str, destination_dir: str):
    os.makedirs(destination_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(source_dir, filename)
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
            processed = process_text(content)
            output_path = os.path.join(destination_dir, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(processed)
            print(f" Обработан файл: {filename}")

if name == "__main__":
    source_folder = "md_files"      
    destination_folder = "processed" 
    process_markdown_files(source_folder, destination_folder)