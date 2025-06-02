import os
from pymorphy3 import MorphAnalyzer
from razdel import tokenize
from typing import List

morph = MorphAnalyzer()

concepts = [
    "Дружба", "Семья", "Командная работа", "Лидерство", "Конфликты",
    "Эмпатия", "Общение", "Разнообразие", "Ссоры", "Забота о других",
    "Понимание себя", "Социальные навыки", "Принятие решений", "Доброта",
    "Поддержка", "Чувство вины и прощение", "Открытость", "Уважение",
    "Взаимопомощь", "Мирное разрешение конфликтов"
]

concept_lemmas = {}
file_to_concept = {}

for term in concepts:
    tokens = [t.text for t in tokenize(term.lower())]
    lemmas = [morph.parse(w)[0].normal_form for w in tokens]
    concept_lemmas[" ".join(lemmas)] = term
    file_to_concept[term.lower().replace(" ", "-")] = term


def process_text(text: str, current_concept: str) -> str:
    tokens = list(tokenize(text))
    result = []
    i = 0
    n = len(tokens)

    while i < n:
        best_length = 0
        best_match = None

        if i == 0 and tokens:
            result.append(text[:tokens[0].start])

        for length in [3, 2, 1]:
            if i + length > n:
                continue

            candidate_tokens = tokens[i:i + length]
            words = [t.text for t in candidate_tokens if t.text.strip()]

            if not words:
                continue

            lemmas = [morph.parse(w)[0].normal_form for w in words]
            lemma_key = " ".join(lemmas)

            if lemma_key in concept_lemmas:
                original_term = concept_lemmas[lemma_key]
                if original_term != current_concept:
                    best_length = length
                    best_match = original_term
                    break

        if best_length and best_match:
            if i > 0:
                prev_token = tokens[i - 1]
                result.append(text[prev_token.stop:tokens[i].start])

            start = tokens[i].start
            end = tokens[i + best_length - 1].stop
            phrase_text = text[start:end]
            md_file = best_match.lower().replace(" ", "-")
            result.append(f"[{phrase_text}](./{md_file}.md)")

            i += best_length
        else:
            if i > 0:
                prev_token = tokens[i - 1]
                result.append(text[prev_token.stop:tokens[i].start])

            result.append(tokens[i].text)
            i += 1

    if tokens:
        last_token = tokens[-1]
        result.append(text[last_token.stop:])

    return "".join(result)

def process_files():
    base_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "../../../KIDBOOK/life/relationships"
    ))

    for filename in os.listdir(base_dir):
        if not filename.endswith(".md"):
            continue

        file_key = filename[:-3]
        current_concept = file_to_concept.get(file_key)

        if not current_concept:
            print(f"Файл {filename} не найден в словаре понятий")
            continue

        filepath = os.path.join(base_dir, filename)
        try:
            with open(filepath, "r+", encoding="utf-8") as f:
                content = f.read()
                updated = process_text(content, current_concept)
                f.seek(0)
                f.write(updated)
                f.truncate()
            print(f"Обработан: {filename}")
        except Exception as e:
            print(f"Ошибка в файле {filename}: {str(e)}")


if __name__ == "__main__":
    process_files()