import os
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

ITALICS_SYMBOL = '*'
BOLD_SYMBOL = '**'
BOLD_ITALICS_SYMBOL = '***'

WORD_LINKS = {
    "праздник": "traditional_holidays.md",
    "традиция": "folk_rituals.md",
    "обычай": "local_customs.md",
    "наследие": "cultural_heritage.md",
    "религия": "religious_practices.md",
    "одежда": "traditional_clothing.md",
    "кухня": "traditional_cuisine.md",
    "искусство": "art_and_crafts.md",
    "ремесло": "art_and_crafts.md",
    "музыка": "music_and_dances.md",
    "танец": "music_and_dances.md",
    "язык": "language_and_folklore.md",
    "фольклер": "language_and_folklore.md",
    "архитектура": "architecture.md",
    "семья": "family_values.md",
    "предок": "ancestor_rituals.md",
    "игра": "traditional_games.md",
    "природа": "natural_symbols.md"
}


def save_updated_file(file_path: str, updated_lines: list) -> None:
    updated_text = "\n".join([" ".join(line) for line in updated_lines])
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_text)


def process_single_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    lines = [line.split() for line in content.split("\n") if line.strip()]
    updated_lines = []

    for line in lines:
        updated_line = []
        for word in line:
            clean_word = word.replace(ITALICS_SYMBOL, "") \
                             .replace(BOLD_SYMBOL, "") \
                             .replace(BOLD_ITALICS_SYMBOL, "") \
                             .strip(".,!?:")
            normal_form = morph.parse(clean_word)[0].normal_form

            if normal_form in WORD_LINKS and os.path.basename(file_path) != WORD_LINKS[normal_form]:
                link_path = f"../{WORD_LINKS[normal_form][:-3]}/{WORD_LINKS[normal_form]}"
                updated_line.append(f"[{word}]({link_path})")
            else:
                updated_line.append(word)

        updated_lines.append(updated_line)

    save_updated_file(file_path, updated_lines)

def traverse_directory(directory_path: str) -> None:
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith("index.md"):
                continue
            elif file.endswith(".md"):
                print(f"Обрабатываю файл: {file}")
                process_single_file(os.path.join(root, file))


if __name__ == "__main__":
    print("Начинаем добавление ссылок...")
    project_directory = '../../../KIDBOOK/world/culture_traditions/concepts/'
    try:
        traverse_directory(project_directory)
    except Exception as error:
        print(f"Произошла ошибка: {error}")
        exit(1)

    print("Ссылки успешно добавлены!")
