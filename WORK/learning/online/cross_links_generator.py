import os
from pathlib import Path
from typing import Dict, Tuple
import pymorphy3
import re

morph = pymorphy3.MorphAnalyzer()

singleTerms: Dict[str, Tuple[str, str]] = {}
multiTerms: Dict[str, Tuple[str, str]] = {}

data = {
    "categories": {
        "Массовые открытые онлайн-курсы (MOOC)": "Массовые_открытые_онлайн-курсы_(MOOC).md",
        "Онлайн-курсы с сертификатами": "Онлайн-курсы_с_сертификатами.md",
        "Геймифицированные платформы": "Геймифицированные_платформы.md",
        "Образовательные мобильные приложения": "Образовательные_мобильные_приложения.md",
        "Подкасты": "Подкасты.md",
        "Обучение через YouTube": "Обучение_через_YouTube.md",
        "Электронные книги и статьи": "Электронные_книги_и_статьи.md",
        "Образовательные блоги": "Образовательные_блоги.md",
        "Интерактивные симуляции": "Интерактивные_симуляции.md",
        "Совместное обучение": "Совместное_обучение.md",
        "Онлайн-наставничество и коучинг": "Онлайн-наставничество_и_коучинг.md",
        "Вебинары": "Вебинары.md",
        "Форумы и сообщества": "Форумы_и_сообщества.md",
        "Социальные сети": "Социальные_сети.md",
        "Виртуальные конференции и саммиты": "Виртуальные_конференции_и_саммиты.md"
    }
}

for term, path in data["categories"].items():
    normalized = morph.parse(term)[0].normal_form
    if ' ' in term:
        multiTerms[normalized] = (term, path)
    else:
        singleTerms[normalized] = (term, path)

def change_match(match: re.Match, current_file_stem: str):
    original_text = match.group(0)
    for normalized_term, (original_term, path) in multiTerms.items():
        if original_text.lower() == original_term.lower():
            target_stem = Path(path).stem
            if target_stem != current_file_stem:
                return f"[{original_text}]({path})"
            return original_text
    term = morph.parse(original_text)[0].normal_form
    if term in singleTerms:
        _, link = singleTerms[term]
        target_stem = Path(link).stem
        if target_stem != current_file_stem:
            return f"[{original_text}]({link})"
    return original_text

wordPattern = re.compile(r'\b[А-Яа-яЁё-]+\b')
headerPattern = re.compile(r'^\s{0,3}#{1,6}\s')
textPattern = re.compile(r'\[.*?\]\(.*?\)')

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    current_file_stem = file_path.stem
    updated_content = content
    for _, (original_term, path) in multiTerms.items():
        target_stem = Path(path).stem
        if target_stem == current_file_stem:
            continue
        pattern = re.compile(r'(?<!\()\b' + re.escape(original_term) + r'\b(?!\))', re.IGNORECASE)
        updated_content = pattern.sub(f"[{original_term}]({path})", updated_content)
    lines = updated_content.split('\n')
    updated_lines = []
    for line in lines:
        if headerPattern.match(line) or textPattern.search(line):
            updated_lines.append(line)
        else:
            updated_line = wordPattern.sub(lambda m: change_match(m, current_file_stem), line)
            updated_lines.append(updated_line)
    updated_content = '\n'.join(updated_lines)  
    if updated_content != content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"File updated: {file_path}")
        except Exception as e:
            print(f"Error writing to file {file_path}: {str(e)}")

def main():
    CONCEPTS_DIR = Path(os.getenv("CONCEPTS_DIR"))
    files = list(CONCEPTS_DIR.glob("*.md"))
    for file in files:
        parse_file(file)
        

if __name__ == "__main__":
    main()
