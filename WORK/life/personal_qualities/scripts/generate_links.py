import re
import os
from pathlib import Path
from pymorphy3 import MorphAnalyzer
import warnings

warnings.filterwarnings("ignore")

CONCEPTS = [
    "Доброта", "Смелость", "Честность", "Щедрость", "Эмпатия",
    "Лень", "Лицемерие", "Жадность", "Вспыльчивость", "Высокомерие",
    "Сдержанность", "Любопытство", "Замкнутость", "Терпение", "Ответственность"
]

BASE_DIR = Path(__file__).resolve().parent
KIDBOOK_DIR = BASE_DIR / "../../../../KIDBOOK/life/personal_qualities"

morph = MorphAnalyzer()

def normalize_concept(concept):
    parsed = morph.parse(concept)[0]
    return parsed.normal_form

def process_text(text, concepts_map, current_concept):
    pattern = re.compile(
        r'(?<!\()[А-Яа-яЁё]+(?![\w\s]*?\]\([^\)]+\))',
        flags=re.IGNORECASE
    )
    
    def replace_match(match):
        word = match.group(0)
        parsed_word = morph.parse(word.lower())[0]
        base_form = parsed_word.normal_form
        
        if base_form in concepts_map:
            original_concept = concepts_map[base_form]
            if original_concept != current_concept:
                return f"[{word}]({original_concept}.md)"
        return word
    
    processed_text = text
    for match in reversed(list(pattern.finditer(text))):
        start, end = match.start(), match.end()
        replacement = replace_match(match)
        processed_text = processed_text[:start] + replacement + processed_text[end:]
        
    return processed_text

def main():
    concepts_map = {normalize_concept(concept): concept for concept in CONCEPTS}
    
    for concept in CONCEPTS:
        md_file = f"{concept}.md"
        file_path = KIDBOOK_DIR / md_file
        
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                content = f.read()
                processed_content = process_text(content, concepts_map, concept)
                
                if processed_content != content:
                    f.seek(0)
                    f.write(processed_content)
                    f.truncate()
                    print(f"✅ {concept}: добавлены новые ссылки")
                else:
                    print(f"🔵 {concept}: изменений не требуется")
                
        except FileNotFoundError:
            print(f"⚠️ Файл {file_path} не найден")
            continue
    
    print("\n🎉 Все файлы успешно обработаны!")

if __name__ == "__main__":
    main()