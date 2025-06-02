import os
import pymorphy3


morph = pymorphy3.MorphAnalyzer()

ITALICS_TEXT_SYMBOL = '*'
BOLD_TEXT_SYMBOL = '**'
ITALICS_BOLD_TEXT_SYMBOL = '***'

PHRASE_LINK_DICT = {
    "рука": "hygiena_hands_and_nails.md",
    "одежда": "hygiene_clothes_shoes.md",
    "обувь": "hygiene_clothes_shoes.md",
    "ноготь": "hygiena_hands_and_nails.md",
    "рот": "hygiena_mouse.md",
    "зуб": "hygiena_mouse.md",
    "стоматолог": "hygiena_mouse.md",
    "тело": "hygiene_body_face.md",
    "лицо": "hygiene_body_face.md",
    "волосы": "hygiene_body_face.md",
    "кожа": "hygiene_body_face.md",
    "сон": "hygiene_sleep.md",
    "нос": "hygiene_nose_and_ear.md",
    "ухо": "hygiene_nose_and_ear.md",
    "игрушка": "hygiene_of_toys_and_personal%20_Items.md",
    "вещь": "hygiene_of_toys_and_personal%20_Items.md",
    "предмет": "hygiene_of_toys_and_personal%20_Items.md",
    "питание": "hygiene_food.md",
    "фрукт": "hygiene_food.md",
    "овощ": "hygiene_food.md",
    "пища": "hygiene_food.md",
    "посуда": "hygiene_food.md",
    "школа": "hygiene_at_the_public_places.md",
    "улица": "hygiene_at_the_public_places.md",
    "транспорт": "hygiene_at_the_public_places.md",
    "пространство": "hygiene_at_your_place.md",
    "комната": "hygiene_at_your_place.md",
    "уборка": "hygiene_at_your_place.md",
    "проветривание": "hygiene_at_your_place.md",
    "микроб": "microbs.md",
    "профилактика": "Personal-protection-and-prevention.md",
    "иммунитет": "Personal-protection-and-prevention.md",
    "болезнь": "Hygiene-during-illness.md",
    "зима": "Seasonal-hygiene.md",
    "весна": "Seasonal-hygiene.md",
    "лето": "Seasonal-hygiene.md",
    "осень": "Seasonal-hygiene.md"
}


def write_to_file(file_path: str, new_file_data_list: list[list[str]]) -> None:
    text = ""

    for string in new_file_data_list:
        text += ' '.join(string)
        text += "\n"

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def process_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    file_data_list = [s.split() for s in text.split(sep='\n') if s.strip()]
    new_file_data_list = []

    for string in file_data_list:
        new_string = []
        for word in string:
            normal_form = morph.parse(word)[0].normal_form
            normal_word = (normal_form
                           .replace(ITALICS_BOLD_TEXT_SYMBOL, "")
                           .replace(BOLD_TEXT_SYMBOL, "")
                           .replace(ITALICS_TEXT_SYMBOL, "")
                           .replace('.', "")
                           .replace(',', "")
                           .replace('?', "")
                           .replace('!', "")
                           .replace(':', "")
                           )

            if (normal_word in PHRASE_LINK_DICT) and (os.path.basename(file_path) != PHRASE_LINK_DICT[normal_word]):
                relation_path = '../' + PHRASE_LINK_DICT[normal_word][:-3] + '/' + PHRASE_LINK_DICT[normal_word]
                new_word = f'[{word}]({relation_path})'

                new_string.append(new_word)
            else:
                new_string.append(word)

        new_file_data_list.append(new_string)

    write_to_file(file_path=file_path, new_file_data_list=new_file_data_list)


def directory_bypass(directory_path: str) -> None:
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith("index.md"):
                continue
            elif file.endswith(".md"):
                print(f'Processing {file}')
                process_file(file_path=os.path.join(root, file))


if __name__ == "__main__":
    print("INFO: Links placing starts")
    kid_book_directory_path = '../../../KIDBOOK/health/hygiene/concepts/'

    try:
        directory_bypass(directory_path=kid_book_directory_path)
    except Exception as error:
        print(f"ERROR: {error}")
        exit(1)

    print("INFO: Links were placed successfully")

