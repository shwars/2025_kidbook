import os
from pymorphy3 import MorphAnalyzer
from razdel import tokenize

morph_analyzer = MorphAnalyzer()

science_terms = [
    "Формальные науки", "Математика", "Алгебра", "Геометрия", "Статистика",
    "Логика", "Компьютерные науки", "Информатика", "Искусственный интеллект",
    "Естественные науки", "Физика", "Химия", "Биология", "Науки о жизни",
    "Медицина", "Генетика", "Ботаника", "Экология", "Социальные науки",
    "Психология", "Социология", "Экономика", "История", "Науки о Земле и космосе",
    "Астрономия", "Геология", "География"
]

term_lemmas_map = {}
file_to_term_map = {}

for term in science_terms:
    tokenized_terms = [token.text for token in tokenize(term.lower())]
    lemmas = [morph_analyzer.parse(word)[0].normal_form for word in tokenized_terms]
    term_lemmas_map[" ".join(lemmas)] = term
    file_to_term_map[term.lower().replace(" ", "-")] = term


def update_text_with_links(text: str, current_term: str) -> str:
    tokenized_text = list(tokenize(text))
    updated_content = []
    index = 0
    total_tokens = len(tokenized_text)

    while index < total_tokens:
        max_length = 0
        matched_term = None

        if index == 0 and tokenized_text:
            updated_content.append(text[:tokenized_text[0].start])

        for length in [3, 2, 1]:
            if index + length > total_tokens:
                continue

            candidate_tokens = tokenized_text[index:index + length]
            words_in_candidate = [token.text for token in candidate_tokens if token.text.strip()]

            if not words_in_candidate:
                continue

            lemmas_of_words = [morph_analyzer.parse(word)[0].normal_form for word in words_in_candidate]
            lemma_key = " ".join(lemmas_of_words)

            if lemma_key in term_lemmas_map:
                original_term = term_lemmas_map[lemma_key]
                if original_term != current_term:
                    max_length = length
                    matched_term = original_term
                    break

        if max_length and matched_term:
            if index > 0:
                previous_token = tokenized_text[index - 1]
                updated_content.append(text[previous_token.stop:tokenized_text[index].start])

            start_index = tokenized_text[index].start
            end_index = tokenized_text[index + max_length - 1].stop
            phrase_text = text[start_index:end_index]
            markdown_file_name = matched_term.lower().replace(" ", "-")
            updated_content.append(f"[{phrase_text}](./{markdown_file_name}.md)")

            index += max_length
        else:
            if index > 0:
                previous_token = tokenized_text[index - 1]
                updated_content.append(text[previous_token.stop:tokenized_text[index].start])

            updated_content.append(tokenized_text[index].text)
            index += 1

    if tokenized_text:
        last_token = tokenized_text[-1]
        updated_content.append(text[last_token.stop:])

    return "".join(updated_content)

def process_markdown_files():
    base_directory = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "../../../../KIDBOOK/world/science"
    ))

    for file_name in os.listdir(base_directory):
        if not file_name.endswith(".md"):
            continue

        file_key_name = file_name[:-3]
        current_term_name = file_to_term_map.get(file_key_name)

        if not current_term_name:
            print(f"Файл {file_name} не найден в словаре понятий")
            continue

        full_file_path = os.path.join(base_directory, file_name)
        try:
            with open(full_file_path, "r+", encoding="utf-8") as file_handle:
                content_data = file_handle.read()
                updated_data = update_text_with_links(content_data, current_term_name)
                file_handle.seek(0)
                file_handle.write(updated_data)
                file_handle.truncate()
            print(f"Обработан: {file_name}")
        except Exception as error_message:
            print(f"Ошибка в файле {file_name}: {str(error_message)}")


if __name__ == "__main__":
    process_markdown_files()