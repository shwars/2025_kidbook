import os
import re
from pathlib import Path
import pymorphy2
from collections import defaultdict, OrderedDict

morph = pymorphy2.MorphAnalyzer()

STOP_WORDS = {
    'без', 'близ', 'в', 'во', 'вместо', 'вне', 'для', 'до', 'за', 'из', 'изо', 'из-за',
    'из-под', 'к', 'ко', 'кроме', 'между', 'на', 'над', 'о', 'об', 'от', 'перед', 'по',
    'под', 'при', 'про', 'ради', 'с', 'со', 'сквозь', 'среди', 'у', 'через', 'и', 'или',
    'а', 'но', 'да', 'либо', 'ни', 'то', 'ли', 'же', 'бы', 'ведь', 'вон', 'вот', 'всё',
    'все', 'всё-таки', 'всегда', 'всего', 'всех', 'вы', 'где', 'даже', 'для', 'до', 'его',
    'ее', 'если', 'есть', 'ещё', 'же', 'за', 'зачем', 'здесь', 'и', 'из', 'или', 'им',
    'иногда', 'их', 'к', 'как', 'какая', 'какой', 'когда', 'кто', 'куда', 'ли', 'лучше',
    'между', 'меня', 'мне', 'много', 'может', 'можно', 'мой', 'моя', 'мы', 'на', 'над',
    'надо', 'наш', 'не', 'него', 'нее', 'нет', 'ни', 'них', 'но', 'ну', 'о', 'об', 'один',
    'он', 'она', 'они', 'оно', 'от', 'перед', 'по', 'под', 'после', 'потом', 'потому',
    'почему', 'при', 'про', 'раз', 'разве', 'с', 'сам', 'свою', 'себе', 'себя', 'сейчас',
    'со', 'совсем', 'так', 'такой', 'там', 'тебя', 'тем', 'теперь', 'то', 'тогда', 'того',
    'тоже', 'той', 'только', 'том', 'ты', 'у', 'уже', 'хотя', 'чего', 'чем', 'через',
    'что', 'чтоб', 'чтобы', 'это', 'этого', 'этой', 'этом', 'этот', 'я'
}

def is_significant_word(word):
    return (len(word) >= 3 and
            word.lower() not in STOP_WORDS and
            any(c.isalpha() for c in word))

def get_base_form(word):
    """Получаем нормальную форму слова"""
    try:
        return morph.parse(word)[0].normal_form
    except:
        return word.lower()

def get_all_forms(word):
    """Получаем все формы слова"""
    try:
        parsed = morph.parse(word)[0]
        return {f.word for f in parsed.lexeme} | {word}
    except:
        return {word}

def process_directory(directory):
    """Создаем индексы для слов и словосочетаний"""
    # Словарь для отдельных слов (базовая форма -> файл)
    word_index = OrderedDict()
    
    # Словарь для словосочетаний (нормальная форма -> (файл, оригинальное словосочетание))
    phrase_index = OrderedDict()
    
    # Собираем все md-файлы и сортируем лексикографически
    md_files = sorted(Path(directory).glob('*.md'), key=lambda x: x.name.lower())
    
    for file in md_files:
        filename = file.stem
        # Заменяем подчеркивания на пробелы для анализа
        phrase = filename.replace('_', ' ')
        words = re.findall(r'[а-яёА-ЯЁ]+', phrase)
        
        # Разделяем обработку для отдельных слов и словосочетаний
        if len(words) == 1:  # Отдельное слово
            word = words[0]
            if is_significant_word(word):
                base = get_base_form(word)
                if base not in word_index:
                    word_index[base] = file.name
        else:  # Словосочетание
            # Получаем все формы для каждого слова в словосочетании
            phrase_forms = []
            for word in words:
                if is_significant_word(word):
                    phrase_forms.append(get_all_forms(word))
                else:
                    phrase_forms.append({word})
            
            # Генерируем все возможные комбинации форм слов
            from itertools import product
            for form_combination in product(*phrase_forms):
                phrase_variant = ' '.join(form_combination).lower()
                if phrase_variant not in phrase_index:
                    phrase_index[phrase_variant] = (file.name, phrase)
    
    return word_index, phrase_index

def add_links_to_files(directory, word_index, phrase_index):
    """Добавляем ссылки с учетом всех требований"""
    for file in sorted(Path(directory).glob('*.md'), key=lambda x: x.name.lower()):
        with open(file, 'r+', encoding='utf-8') as f:
            content = f.read()
            new_content = content
            
            # Сначала обрабатываем словосочетания (более длинные совпадения)
            for phrase_variant, (target_file, original_phrase) in phrase_index.items():
                if target_file == file.name:  # Пропускаем ссылки на себя
                    continue
                
                # Ищем точное совпадение словосочетания (с учетом регистра)
                pattern = re.compile(r'(?<!\[)\b(' + re.escape(phrase_variant) + r')\b(?!\])', re.IGNORECASE)
                
                def make_phrase_link(match):
                    matched_phrase = match.group(1)
                    # Сохраняем оригинальный регистр
                    if matched_phrase.lower() == phrase_variant:
                        return f'[{matched_phrase}]({target_file})'
                    return matched_phrase
                
                new_content = pattern.sub(make_phrase_link, new_content)
            
            # Затем обрабатываем отдельные слова
            for base_word, target_file in word_index.items():
                if target_file == file.name:  # Пропускаем ссылки на себя
                    continue
                
                # Получаем все формы слова
                all_forms = get_all_forms(base_word)
                
                # Ищем только слова, которые не являются частью ссылок
                pattern = re.compile(r'(?<!\[)\b(' + '|'.join(map(re.escape, all_forms)) + r')\b(?!\])', re.IGNORECASE)
                
                def make_word_link(match):
                    matched_word = match.group(1)
                    return f'[{matched_word}]({target_file})'
                
                new_content = pattern.sub(make_word_link, new_content)
            
            if new_content != content:
                f.seek(0)
                f.write(new_content)
                f.truncate()

if __name__ == '__main__':
    current_dir = Path(__file__).parent
    
    print("Создаем индексы слов и словосочетаний...")
    word_index, phrase_index = process_directory(current_dir)
    print(f"Найдено {len(word_index)} отдельных слов и {len(phrase_index)} вариантов словосочетаний")
    
    print("Добавляем ссылки с учетом приоритетов...")
    add_links_to_files(current_dir, word_index, phrase_index)
    
    print("Готово! Ссылки добавлены с сохранением форм и падежей")