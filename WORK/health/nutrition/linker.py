import os
import re
import pymorphy2
import itertools

from typing import Generator


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

TERMS_FILENAMES = {
    'калории': 'calories.md',
    'углеводы': 'carbohydrates.md',
    'диета': 'diet.md',
    'пищеварение': 'digestion.md',
    'жиры': 'fats.md',
    'пища': 'food.md',
    'пищевые добавки': 'food_additives.md',
    'гликемический индекс': 'glycemic_index.md',
    'здоровое питание': 'healthy_eating.md',
    'голод': 'hunger.md',
    'макронутриенты': 'macronutrients.md',
    'метаболизм': 'metabolism.md',
    'микронутриенты': 'micronutients.md',
    'минералы': 'minerals.md',
    'нутриенты': 'nutrient.md',
    'питание': 'nutrition.md',
    'белки': 'protein.md',
    'рацион': 'ration.md',
    'насыщение': 'saturation.md',
    'витамины': 'vitamins.md',
}


def get_norm_word(word: str) -> str:
    return pymorphy2.MorphAnalyzer().parse(word)[0].normal_form


def get_word_forms(word: str) -> list[str]:
    morph = pymorphy2.MorphAnalyzer()
    return [form.word for form in morph.parse(word)[0].lexeme]


def remove_special_chars(word: str) -> str:
    return re.sub(r'[^\w\s]|[\d]', '', word)


def get_all_phrase_forms(phrase: str) -> Generator[tuple[str, ...], None, None]:
    words = phrase.split()
    word_forms = [
        get_word_forms(remove_special_chars(word))
        for word in words
    ]

    yield from itertools.product(*word_forms)

def add_text_links(filepath: str, terms_filenames: dict[str, str]) -> None:
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    for term in terms_filenames:
        for phrase_form in get_all_phrase_forms(term):
            str_phrase_form = ' '.join(phrase_form)
            pattern = rf'(?<!\[)\b{re.escape(str_phrase_form)}\b(?!\])'
            text = re.sub(
                pattern,
                lambda match:
                    (
                        f'[{match.group(0)}]'
                        f'({os.path.join(BASE_DIR, terms_filenames[term])})'
                    ),
                text,
                flags=re.IGNORECASE
            )

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)


def main(dirpath: str, terms_filenames: dict[str, str]) -> None:
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)

        if not os.path.isfile(filepath) or not filename.endswith('.md'):
            continue

        add_text_links(filepath, terms_filenames)


if __name__ == '__main__':
    directry = '../../../KIDBOOK/health/nutrition/'
    main(os.path.join(BASE_DIR, directry), TERMS_FILENAMES)
