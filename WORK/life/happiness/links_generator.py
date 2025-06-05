import os
import re
from pathlib import Path
import pymorphy3
from typing import Dict, Tuple

morph = pymorphy3.MorphAnalyzer()

CATEGORY_TO_FILE = {
    "счастье": "Счастье.md",
    "радость": "Радость.md",
    "восторг": "Радость.md",
    "удовольствие": "Счастье.md",
    "наслаждение": "Счастье.md",
    "блаженство": "Счастье.md",
    "улыбка": "Улыбка.md",
    "смех": "Радость.md",
    "светлые чувства": "Счастье.md",
    "дружба": "Дружба.md",
    "приятели": "Дружба.md",
    "товарищи": "Дружба.md",
    "общение": "Дружба.md",
    "поддержка": "Помощь_другим.md",
    "любовь": "Любовь.md",
    "привязанность": "Любовь.md",
    "романтика": "Любовь.md",
    "сердце": "Любовь.md",
    "чувства": "Любовь.md",
    "забота": "Семья.md",
    "семья": "Семья.md",
    "родители": "Семья.md",
    "дети": "Семья.md",
    "родные": "Семья.md",
    "родственники": "Семья.md",
    "тепло": "Семья.md",
    "игры": "Игры.md",
    "развлечения": "Игры.md",
    "настолки": "Игры.md",
    "видеоигры": "Игры.md",
    "веселье": "Игры.md",
    "конкурсы": "Игры.md",
    "азарт": "Игры.md",
    "хобби": "Хобби.md",
    "увлечения": "Хобби.md",
    "интересы": "Хобби.md",
    "творчество": "Хобби.md",
    "мастерство": "Хобби.md",
    "времяпрепровождение": "Хобби.md",
    "отдых": "Отдых.md",
    "релаксация": "Отдых.md",
    "спокойствие": "Отдых.md",
    "расслабление": "Отдых.md",
    "каникулы": "Отдых.md",
    "отпуск": "Отдых.md",
    "путешествия": "Путешествия.md",
    "поездки": "Путешествия.md",
    "приключения": "Путешествия.md",
    "туризм": "Путешествия.md",
    "поход": "Путешествия.md",
    "новые места": "Путешествия.md",
    "экскурсии": "Путешествия.md",
    "улыбка": "Улыбка.md",
    "смех": "Улыбка.md",
    "добро": "Улыбка.md",
    "радость": "Улыбка.md",
    "светлые эмоции": "Улыбка.md",
    "оптимизм": "Улыбка.md",
    "помощь другим": "Помощь_другим.md",
    "волонтерство": "Помощь_другим.md",
    "благотворительность": "Помощь_другим.md",
    "поддержка": "Помощь_другим.md",
    "добрые дела": "Помощь_другим.md",
    "милосердие": "Помощь_другим.md",
    "природа": "Природа.md",
    "экология": "Природа.md",
    "растения": "Природа.md",
    "животные": "Природа.md",
    "лес": "Природа.md",
    "океан": "Природа.md",
    "воздух": "Природа.md",
    "солнце": "Природа.md",
    "музыка": "Музыка.md",
    "мелодия": "Музыка.md",
    "песня": "Музыка.md",
    "гармония": "Музыка.md",
    "ритм": "Музыка.md",
    "звук": "Музыка.md",
    "спорт": "Спорт.md",
    "тренировки": "Спорт.md",
    "физическая активность": "Спорт.md",
    "здоровье": "Спорт.md",
    "соревнования": "Спорт.md",
    "командные игры": "Спорт.md",
    "еда": "Еда.md",
    "кулинария": "Еда.md",
    "блюда": "Еда.md",
    "рецепты": "Еда.md",
    "вкусности": "Еда.md",
    "десерты": "Еда.md",
    "кухня": "Еда.md"
}

WORD_RE = re.compile(r'\b[А-Яа-яЁё-]+\b')
MULTIWORD_RE = re.compile(r'\b[А-Яа-яЁё-]+(?:\s+[А-Яа-яЁё-]+)*\b')
HEADER_RE = re.compile(r'^\s{0,3}#{1,6}\s')
LINK_RE = re.compile(r'\[.*?\]\(.*?\)')

single_term_mapping: Dict[str, Tuple[str, str]] = {}
multi_term_mapping: Dict[str, Tuple[str, str]] = {}

for term, path in CATEGORY_TO_FILE.items():
    normalized_term = morph.parse(term)[0].normal_form
    if ' ' in term:
        multi_term_mapping[normalized_term] = (term, path)
    else:
        single_term_mapping[normalized_term] = (term, path)


def update_match(match: re.Match, current_file_name: str) -> str:
    matched_text = match.group(0)

    for norm_term, (original_term, path) in multi_term_mapping.items():
        if matched_text.lower() == original_term.lower():
            target_name = Path(path).stem
            if target_name != current_file_name:
                return f"[{matched_text}]({path})"
            return matched_text

    word = matched_text
    normalized = morph.parse(word)[0].normal_form
    if normalized in single_term_mapping:
        _, link_path = single_term_mapping[normalized]
        target_name = Path(link_path).stem
        if target_name != current_file_name:
            return f"[{word}]({link_path})"

    return matched_text


def modify_markdown(file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    file_name_stem = file_path.stem
    updated_content = content
    for _, (term, path) in multi_term_mapping.items():
        target_name = Path(path).stem
        if target_name == file_name_stem:
            continue

        pattern = re.compile(r'(?<!\()\b' + re.escape(term) + r'\b(?!\))', re.IGNORECASE)
        updated_content = pattern.sub(f"[{term}]({path})", updated_content)

    lines = updated_content.split('\n')
    modified_lines = []

    for line in lines:
        if HEADER_RE.match(line) or LINK_RE.search(line):
            modified_lines.append(line)
        else:
            modified_line = WORD_RE.sub(
                lambda match: update_match(match, file_name_stem), line
            )
            modified_lines.append(modified_line)

    updated_content = '\n'.join(modified_lines)

    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)
        print(f"Файл изменён: {file_path}")


def process_files():
    target_dir = Path("../../../KIDBOOK/life/happiness/concepts")
    if not target_dir.exists():
        raise ValueError("Указанная директория для обработки markdown файлов не существует.")

    markdown_files = list(target_dir.glob("*.md"))
    if not markdown_files:
        print("Нет файлов .md для обработки.")
        return

    for markdown_file in markdown_files:
        try:
            modify_markdown(markdown_file)
        except Exception as error:
            print(f"Ошибка при обработке файла {markdown_file}: {error}")

    print(f"Обработка завершена. Обработано файлов: {len(markdown_files)}")


if __name__ == "__main__":
    process_files()
