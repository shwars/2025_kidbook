import os
import re
from pathlib import Path
import pymorphy3
from typing import Dict, Tuple

morph = pymorphy3.MorphAnalyzer()

JSON_DATA = {
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

WORD_PATTERN = re.compile(r'\b[А-Яа-яЁё-]+\b')
HEADER_PATTERN = re.compile(r'^\s{0,3}#{1,6}\s')
LINKED_TEXT_PATTERN = re.compile(r'\[.*?\]\(.*?\)')

SINGLE_WORD_TERMS: Dict[str, Tuple[str, str]] = {}
MULTI_WORD_TERMS: Dict[str, Tuple[str, str]] = {}

for term, path in JSON_DATA["categories"].items():
    normalized = morph.parse(term)[0].normal_form
    if ' ' in term:
        MULTI_WORD_TERMS[normalized] = (term, path)
    else:
        SINGLE_WORD_TERMS[normalized] = (term, path)

def replace_match(match: re.Match, current_file_stem: str) -> str:
    original_text = match.group(0)
    
    for normalized_term, (original_term, path) in MULTI_WORD_TERMS.items():
        if original_text.lower() == original_term.lower():
            target_stem = Path(path).stem
            if target_stem != current_file_stem:
                return f"[{original_text}]({path})"
            return original_text

    term = morph.parse(original_text)[0].normal_form
    if term in SINGLE_WORD_TERMS:
        _, link = SINGLE_WORD_TERMS[term]
        target_stem = Path(link).stem
        if target_stem != current_file_stem:
            return f"[{original_text}]({link})"
    
    return original_text

def process_markdown_file(file_path: Path) -> None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return

    current_file_stem = file_path.stem
    updated_content = content
    for _, (original_term, path) in MULTI_WORD_TERMS.items():
        target_stem = Path(path).stem
        if target_stem == current_file_stem:
            continue
        pattern = re.compile(r'(?<!\()\b' + re.escape(original_term) + r'\b(?!\))', re.IGNORECASE)
        updated_content = pattern.sub(f"[{original_term}]({path})", updated_content)
    
    lines = updated_content.split('\n')
    updated_lines = []
    
    for line in lines:
        if HEADER_PATTERN.match(line) or LINKED_TEXT_PATTERN.search(line):
            updated_lines.append(line)
        else:
            updated_line = WORD_PATTERN.sub(lambda m: replace_match(m, current_file_stem), line)
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
    if not CONCEPTS_DIR:
        raise ValueError("The directory for processing markdown files is not set.")

    md_files = list(CONCEPTS_DIR.glob("*.md"))
    
    if not md_files:
        print("No .md files found for processing.")
        return
    
    for md_file in md_files:
        try:
            process_markdown_file(md_file)
        except Exception as e:
            print(f"Error processing file {md_file}: {str(e)}")

    print(f"Processing completed. Files processed: {len(md_files)}")

if __name__ == "__main__":
    main()
