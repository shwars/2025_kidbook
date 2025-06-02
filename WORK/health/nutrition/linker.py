import os
import re
import pymorphy2
import itertools
import json

from collections import defaultdict
from pathlib import Path
from typing import Generator


BASEDIR = Path(__file__).resolve()

TERMS_DIRPATH = Path(BASEDIR).parents[3] / 'KIDBOOK/health/nutrition'

CONCEPTS_PATH = Path(BASEDIR).parents[3] / 'WORK/health/nutrition/concepts.json'

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


PATTERNS = [
    r'\[({})\]\([^)]+\.md\)', # строка внутри md ссылки
    r'(?<![\[(])\b({})\b(?![\])(])', # строка НЕ внутри md ссылки
]


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


def add_text_links(
    filepath: str,
    terms_filepaths: dict[str, str],
    replacement_patterns: list[str]
) -> list[str]:
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    found_links = set()

    for term, term_filepath in terms_filepaths.items():

        for phrase_form in get_all_phrase_forms(term):
            str_phrase_form = ' '.join(phrase_form)
            patterns = r'|'.join(
                pattern.format(re.escape(str_phrase_form))
                for pattern in replacement_patterns
            )

            text = re.sub(
                patterns,
                lambda match: f'[{match.group(1)}]({term_filepath})',
                text,
                flags=re.IGNORECASE
            )

    linksearch_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(linksearch_pattern, text, flags=re.IGNORECASE):
        found_links.add(match.group(2))

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)

    return list(found_links)


def main(
    dirpath: str,
    terms_filenames: dict[str, str],
    replacement_patterns: list[str],
    concepts_path: str
) -> None:

    links = dict()

    for filename in os.listdir(dirpath):
        filepath = Path(dirpath) / filename

        if not os.path.isfile(filepath) or not filename.endswith('.md'):
            continue

        links[filename] = add_text_links(filepath, terms_filenames, replacement_patterns)

    concepts = dict()
    concepts['categories'] = {
        term: '../../../' + term_filename
        for term, term_filename in terms_filenames.items()
    }
    concepts['links'] = links

    with open(concepts_path, 'w', encoding='utf-8') as file:
        json.dump(concepts, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main(TERMS_DIRPATH, TERMS_FILENAMES, PATTERNS, CONCEPTS_PATH)
