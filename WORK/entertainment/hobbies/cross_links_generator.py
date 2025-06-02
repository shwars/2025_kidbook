# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import pymorphy3
from typing import Dict, Tuple

morph = pymorphy3.MorphAnalyzer()

JSON_DATA = {
    "categories": {
        "хобби": "хобби.md",
        "творческие" : "творческие.md",
        "активные" : "активные.md",
        "интеллектуальные" : "интеллектуальные.md",
        "домашние" : "домашние.md",
        "спорт" : "спорт.md",
        "танцы" : "танцы.md",
        "садоводство" : "садоводство.md",
        "чтение" : "чтение.md",
        "настольные игры" : "настольные_игры.md",
        "научнве эксперименты" : "научные_эксперименты.md",
        "конструирование" : "конструирование.md",
        "видеоигры" : "видеоигры.md",
        "настолки" : "настольные_игры.md",
        "проводить эксперименты" : "научные_эксперименты.md",
        "творческие" : "творческие.md",
        "творчество" : "творческие.md",
        "рисование" : "рисование.md",
        "музыка" : "музыка.md",
        "вышивание" : "вышивание.md",
        "актерское мастерство" : "актерское_мастерство.md",
        "кулинария" : "кулинария.md",
        "физическая активность" : "активные.md",
        "увлечение" : "хобби.md",
        "мышление" : "интеллектуальные.md",
        "логика" : "интеллектуальные.md",
        "занятие" : "хобби.md",
        "искусство" : "хобби.md",
        "фантазия" : "творческие.md",
        "помидорчик" : "садоводство.md",
        "салат" : "садоводство.md",
        "собираются вместе" : "домашние.md",
        "близких" : "домашние.md",
        "дом" : "домашние.md",
        "книга" : "чтение.md",
        "тренировка" : "спорт.md",
        "спортивные" : "спорт.md",
        "создание различных моделей" : "интеллектуальные.md",
        "воображение" : "творческие.md",
        "решать задачи" : "интеллектуальные.md",
        "мозг" : "интеллектуальные.md",
        "тренироваться" : "спорт.md",
        "семья" : "домашние.md",
        "стратегия" : "видеоигры.md",
        "анализировать" : "интеллектуальные.md",
        "родители" : "домашние.md",
        "семейные" : "домашние.md",
        "исследовать" : "интеллектуальные.md",
        "природа" : "садоводство.md",
        "укрепление здоровья" : "активные.md",
        "движение" : "активные.md",
        "здоровый" : "активные.md",
        "ритм" : "музыка.md",
        "поддерживать форму" : "активные.md",
        "гибкость" : "активные.md",
        "рисунок" : "рисование.md",
        "песня" : "музыка.md",
        "кулинарное блюдо" : "кулинария.md",
        "играя музыку" : "музыка.md",
        "актерская игра" : "актерское_мастерство.md",
        "эксперименты" : "интеллектуальные.md",
        "приготовление пищи" : "кулинария.md",
        "молоко" : "кулинария.md",
        "вода" : "кулинария.md",
        "соль" : "кулинария.md",
        "сахар" : "кулинария.md",
        "вырисовка" : "рисование.md",
        "экспериментировать" : "научные_эксперименты.md",
        "футбол" : "спорт.md",
        "плаванье" : "спорт.md",
        "открытия" : "научные_эксперименты.md",
        "собирать модели" : "конструирование.md",
        "наука" : "научные_эксперименты.md",
        "изобретения" : "конструирование.md",
        "загадка" : "интеллектуальны.md",
        "игры" : "настольные_игры.md",
        "футболист" : "спорт.md",
        "планировать ходы" : "видеоигры.md",
        "семейные традиции" : "домашние.md",
        "технологии" : "конструирование.md",
        "конструкции" : "конструирование.md",
        "приложения" : "видеоигры.md",
        "механика" : "конструирование.md",
        "полезные навыки" : "хобби.md",
        "физическая форма" : "активные.md"
    }
}

WORD_PATTERN = re.compile(r'\b[А-Яа-яЁё-]+\b')
MULTIWORD_PATTERN = re.compile(r'\b[А-Яа-яЁё-]+(?:\s+[А-Яа-яЁё-]+)*\b')
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

    word = original_text
    term = morph.parse(word)[0].normal_form
    if term in SINGLE_WORD_TERMS:
        _, link = SINGLE_WORD_TERMS[term]
        target_stem = Path(link).stem
        if target_stem != current_file_stem:
            return f"[{word}]({link})"
    
    return original_text

def process_markdown_file(file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

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
            updated_line = WORD_PATTERN.sub(
                lambda m: replace_match(m, current_file_stem), line
            )
            updated_lines.append(updated_line)
    
    updated_content = '\n'.join(updated_lines)
    
    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Файл обновлен: {file_path}")

def main():
    CONCEPTS_DIR = Path(os.getenv("CONCEPTS_DIR"))
    if not CONCEPTS_DIR:
        raise ValueError("Не задана директория для обработки markdown файлов.")

    md_files = list(CONCEPTS_DIR.glob("*.md"))
    
    if not md_files:
        print("Нет .md файлов для обработки.")
        return
    
    for md_file in md_files:
        try:
            process_markdown_file(md_file)
        except Exception as e:
            print(f"Ошибка при обработке файла {md_file}: {str(e)}")

    print(f"Обработка завершена. Обработано файлов: {len(md_files)}")

if __name__ == "__main__":
    main()