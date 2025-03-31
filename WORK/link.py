import os
import json
import re
import time
from pathlib import Path
import argparse
import chardet

try:
    import pymorphy3
    morph = pymorphy3.MorphAnalyzer()
    PYMORPHY_AVAILABLE = True
    print("pymorphy3 найден и инициализирован.")
except ImportError:
    morph = None
    PYMORPHY_AVAILABLE = False
    print("ПРЕДУПРЕЖДЕНИЕ: Библиотека pymorphy3 не найдена.")
    print("Установите ее: pip install pymorphy3 pymorphy3-dicts-ru")
    print("Скрипт будет работать в режиме простого поиска точных совпадений (регистронезависимо).")

# --- Конфигурация ---
DEFAULT_KIDBOOK_ROOT = Path("./KIDBOOK")
DEFAULT_WORK_ROOT = Path("./WORK")
CONCEPTS_FILENAME = "concepts.json"
SKIP_DIRS = {"venv", ".git", "__pycache__", "node_modules"}
# Regex для токенизации: (\b[\w-]+\b) - слово (с дефисами), ([^\w-]+) - все остальное (не-слова)
TOKENIZE_REGEX = re.compile(r'(\b[\w-]+\b)|([^\w-]+)')

# --- Функции ---

def find_concepts_files(work_root):
    """Находит все файлы concepts.json в поддиректориях work_root."""
    concept_files = []
    if not work_root.is_dir():
        print(f"Ошибка: Директория WORK '{work_root}' не найдена.")
        return []
    for item in work_root.rglob(f"**/{CONCEPTS_FILENAME}"):
        if item.is_file():
            if not any(part in SKIP_DIRS for part in item.parts):
                concept_files.append(item)
                print(f"  Найден файл концептов: {item}")
            else:
                print(f"  Пропущен файл концептов в '{item}' (внутри SKIP_DIRS).")
    return concept_files

def load_all_concepts(work_root):
    """Загружает все концепты из найденных файлов concepts.json."""
    all_concepts = {}
    concept_files = find_concepts_files(work_root)
    project_root = work_root.parent

    for f_path in concept_files:
        try:
            # Пытаемся определить кодировку concepts.json, по умолчанию utf-8
            try:
                with open(f_path, 'rb') as fb:
                    raw = fb.read(5000)
                    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
            except Exception:
                encoding = 'utf-8'

            with open(f_path, 'r', encoding=encoding) as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "topic" in item and "file" in item:
                            topic = item["topic"].strip()
                            raw_file_path = Path(item["file"])
                            if raw_file_path.is_absolute():
                                print(f"Предупреждение: Абсолютный путь в {f_path} для '{topic}': {raw_file_path}. Попытка сделать относительным.")
                                try:
                                    file_path_rel = raw_file_path.relative_to(project_root)
                                except ValueError:
                                    print(f"  Не удалось сделать путь относительным к {project_root}. Пропуск.")
                                    continue
                            else:
                                file_path_rel = raw_file_path

                            # Проверяем и корректируем путь относительно корня проекта
                            if file_path_rel.parts and file_path_rel.parts[0] != DEFAULT_KIDBOOK_ROOT.name:
                                likely_correct_path = project_root / file_path_rel
                                # Проверяем, что путь существует и это файл
                                if likely_correct_path.exists() and likely_correct_path.is_file():
                                     file_path_rel = likely_correct_path.relative_to(project_root)
                                     # print(f"  Скорректирован путь для '{topic}': {file_path_rel}")
                                elif file_path_rel.parts[0] != DEFAULT_KIDBOOK_ROOT.name:
                                      # Выводим предупреждение только если путь все еще не начинается с KIDBOOK
                                      print(f"  Предупреждение: Путь '{file_path_rel}' для '{topic}' из {f_path} не начинается с '{DEFAULT_KIDBOOK_ROOT.name}' или файл не найден. Ссылка может быть некорректной.")

                            if topic and file_path_rel:
                                path_str = str(file_path_rel).replace('\\', '/')
                                if topic in all_concepts and all_concepts[topic] != path_str:
                                    print(f"Предупреждение: Дубликат темы '{topic}' с разным путем!")
                                    print(f"  Старый путь: {all_concepts[topic]}")
                                    print(f"  Новый путь: {path_str} (из {f_path})")
                                    print(f"  Используется новый путь.")
                                all_concepts[topic] = path_str
                        else:
                            print(f"Предупреждение: Неверный формат элемента в {f_path}: {item}")
                else:
                    print(f"Предупреждение: Файл {f_path} не содержит список JSON.")
        except json.JSONDecodeError:
            print(f"Ошибка: Не удалось прочитать JSON из файла: {f_path}")
        except Exception as e:
            print(f"Ошибка при обработке файла {f_path}: {e}")

    print(f"\nЗагружено {len(all_concepts)} уникальных концептов.")
    # Сортируем по длине ключа (темы) в обратном порядке - важно для многословных
    sorted_concepts = dict(sorted(all_concepts.items(), key=lambda item: len(item[0]), reverse=True))
    return sorted_concepts

def preprocess_concepts(concepts_dict, use_lemma=True):
    """Разделяет концепты на однословные (с леммами) и многословные."""
    single_word_lemma_map = {} # { лемма: путь }
    multi_word_concepts = {}   # { оригинал: путь }

    # Используем pymorphy для лемматизации однословных, если доступно и включено
    can_lemmatize = PYMORPHY_AVAILABLE and use_lemma

    print("\nПредобработка концептов...")
    single_count = 0
    multi_count = 0

    for topic, path in concepts_dict.items():
        # Считаем количество "слов" в теме (простая проверка по пробелам)
        # Игнорируем текст в скобках при подсчете слов для лемматизации
        topic_for_check = re.sub(r'\(.*?\)', '', topic).strip()
        words_in_topic = topic_for_check.split()

        # Считаем тему однословной, только если ОДНО слово ВНЕ скобок
        if len(words_in_topic) == 1:
            word = words_in_topic[0]
            # Убираем пунктуацию по краям для ключа леммы
            cleaned_word = re.sub(r'^\W+|\W+$', '', word)
            if can_lemmatize and cleaned_word:
                parsed_word = morph.parse(cleaned_word)
                if parsed_word:
                    lemma = parsed_word[0].normal_form
                    # Для тем типа "Свидетель" лемма будет "свидетель"
                    if lemma in single_word_lemma_map and single_word_lemma_map[lemma] != path:
                         print(f"  Предупреждение: Лемма '{lemma}' для '{topic}' уже связана с '{single_word_lemma_map[lemma]}'. Перезапись на '{path}'.")
                    single_word_lemma_map[lemma] = path
                    single_count +=1
                else:
                    # Если не удалось лемматизировать, считаем многословным для точного поиска
                    multi_word_concepts[topic] = path
                    multi_count += 1
            elif cleaned_word: # Если лемматизация недоступна/отключена, ищем точно
                multi_word_concepts[topic] = path
                multi_count += 1
            # Игнорируем пустые темы или темы только из пунктуации/скобок
        else:
             # Все темы с >1 словом или со скобками (даже если одно слово) идут в точный поиск
             multi_word_concepts[topic] = path
             multi_count += 1

    # Сортируем многословные еще раз по длине
    multi_word_concepts = dict(sorted(multi_word_concepts.items(), key=lambda item: len(item[0]), reverse=True))

    print(f"Обработано концептов: {single_count} однословных (для лемматизации), {multi_count} многословных/сложных (для точного совпадения).")
    if single_count > 0:
         print("  Леммы для поиска:", list(single_word_lemma_map.keys()))
    return single_word_lemma_map, multi_word_concepts


def find_md_files(kidbook_root):
    """Находит все .md файлы в директории kidbook_root, исключая SKIP_DIRS."""
    md_files = []
    if not kidbook_root.is_dir():
        print(f"Ошибка: Директория KIDBOOK '{kidbook_root}' не найдена.")
        return []
    for item in kidbook_root.rglob("*.md"):
         if item.is_file():
            if not any(part in SKIP_DIRS for part in item.parts):
                md_files.append(item)
            else:
                print(f"  Пропущен файл '{item}' (внутри SKIP_DIRS).")
    return md_files

def detect_encoding(file_path):
    """Определяет кодировку файла."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(5000)
            result = chardet.detect(raw_data)
            return result['encoding'] if result['encoding'] else 'utf-8'
    except Exception:
        return 'utf-8'

def tokenize_text(text):
    """Разбивает текст на слова и не-слова."""
    tokens = []
    # Исправленный regex: (\b[\w'-]+\b) позволяет апострофы и дефисы внутри слов
    # ([^\w'-]+) - все остальное
    tokenize_regex_local = re.compile(r"(\b[\w'-]+\b)|([^\w'-]+)")
    for match in tokenize_regex_local.finditer(text):
        word = match.group(1)
        non_word = match.group(2)
        if word:
            tokens.append({'text': word, 'is_word': True})
        elif non_word:
            tokens.append({'text': non_word, 'is_word': False})
    return tokens

def create_links_in_file(md_file_path, single_lemma_map, multi_concepts, project_root, use_lemma=True, dry_run=False):
    """Ищет концепты в файле и создает Markdown ссылки (с лемматизацией)."""
    try:
        file_encoding = detect_encoding(md_file_path)
        with open(md_file_path, 'r', encoding=file_encoding) as f:
            original_content = f.read()
    except Exception as e:
        print(f"Ошибка чтения файла {md_file_path}: {e}")
        return 0

    links_added = 0
    links_added_multi = 0
    links_added_lemma = 0
    current_file_rel_path_str = str(md_file_path.relative_to(project_root)).replace('\\', '/')
    md_file_dir = md_file_path.parent

    # 1. Маскировка существующих ссылок и блоков кода
    masked_content, placeholders = mask_content(original_content)
    processed_text = masked_content # Начинаем обработку с замаскированного текста

    # 2. Обработка МНОГОСЛОВНЫХ/СЛОЖНЫХ концептов (точное совпадение, регистронезависимо)
    # Итерация от длинных к коротким
    temp_processed_text = processed_text # Копия для итераций по многословным
    for topic_original, target_file_rel_path_str in multi_concepts.items():
        # Пропускаем self-links
        if target_file_rel_path_str == current_file_rel_path_str:
            continue

        # Рассчитываем относительный путь
        try:
            target_path_abs = project_root / target_file_rel_path_str
            # Проверяем существование файла перед расчетом пути
            if not target_path_abs.is_file():
                 print(f"  Предупреждение: Целевой файл '{target_file_rel_path_str}' для темы '{topic_original}' не найден. Пропуск.")
                 continue
            relative_link_path = os.path.relpath(target_path_abs, start=md_file_dir)
            relative_link_path = relative_link_path.replace('\\', '/')
        except ValueError as e:
            print(f"  Предупреждение: Не удалось рассчитать относительный путь для '{topic_original}' из '{md_file_path}': {e}")
            continue

        # Паттерн для поиска ТОЛЬКО этой фразы (целые слова)
        pattern = r'\b(' + re.escape(topic_original) + r')\b'
        try:
            current_pass_text = "" # Собираем текст после замен в этой итерации
            last_end = 0
            matches_this_topic = 0
            # Используем finditer для контроля замен на тексте *после предыдущих замен*
            for match in re.finditer(pattern, temp_processed_text, flags=re.IGNORECASE):
                start, end = match.span()
                matched_text = match.group(1) # Текст, который совпал

                # Проверка, не внутри ли плейсхолдера (простая)
                # Ищем плейсхолдеры до и после совпадения
                has_placeholder_before = re.search(f"{PLACEHOLDER_PREFIX}\\d+{PLACEHOLDER_SUFFIX}$", temp_processed_text[last_end:start])
                has_placeholder_after = re.match(f"^{PLACEHOLDER_PREFIX}\\d+{PLACEHOLDER_SUFFIX}", temp_processed_text[end:])

                if has_placeholder_before or has_placeholder_after:
                     #print(f"    Пропуск (Multi) '{matched_text}' - рядом/внутри плейсхолдера.")
                     current_pass_text += temp_processed_text[last_end:end] # Добавляем совпадение без изменений
                else:
                     # Формируем замену
                     replacement = f"[{matched_text}]({relative_link_path})"
                     # Добавляем текст до совпадения и саму замену
                     current_pass_text += temp_processed_text[last_end:start] + replacement
                     links_added += 1
                     links_added_multi += 1
                     matches_this_topic += 1
                     print(f"    + [Multi] Добавлена ссылка: [{matched_text}]({relative_link_path})")

                last_end = end # Обновляем позицию для следующего поиска

            # Добавляем остаток текста после последнего совпадения (или весь текст, если совпадений не было)
            current_pass_text += temp_processed_text[last_end:]

            # Обновляем текст для следующей итерации по темам
            if matches_this_topic > 0:
                 temp_processed_text = current_pass_text

        except re.error as e:
            print(f"  Ошибка регулярного выражения для темы '{topic_original}': {e}")
            continue
        except Exception as e:
             print(f"  Неожиданная ошибка при обработке Multi-темы '{topic_original}': {e}")
             continue # Переходим к следующей теме

    # Фиксируем результат после всех многословных замен
    processed_text = temp_processed_text

    # 3. Обработка ОДНОСЛОВНЫХ концептов (по леммам)
    if PYMORPHY_AVAILABLE and use_lemma and single_lemma_map:
        try:
            # Токенизируем то, что получилось ПОСЛЕ обработки многословных
            tokens = tokenize_text(processed_text)
            processed_tokens = [{'text': t['text'], 'is_word': t['is_word'], 'linked': False} for t in tokens]

            for i, token in enumerate(processed_tokens):
                if token['is_word'] and not token['linked']:
                    # Очищаем слово от часто встречающихся знаков препинания по краям для лемматизации
                    cleaned_word_text = token['text'].strip('.,!?;:\'"()[]{}')
                    if not cleaned_word_text: continue # Если остались только символы

                    parsed_word = morph.parse(cleaned_word_text)
                    if parsed_word:
                        lemma = parsed_word[0].normal_form
                        if lemma in single_lemma_map:
                            target_file_rel_path_str = single_lemma_map[lemma]
                            # Пропускаем self-links
                            if target_file_rel_path_str == current_file_rel_path_str:
                                continue

                            # Рассчитываем относительный путь
                            try:
                                target_path_abs = project_root / target_file_rel_path_str
                                # Проверяем существование файла
                                if not target_path_abs.is_file():
                                     print(f"  Предупреждение: Целевой файл '{target_file_rel_path_str}' для леммы '{lemma}' не найден. Пропуск.")
                                     continue
                                relative_link_path = os.path.relpath(target_path_abs, start=md_file_dir)
                                relative_link_path = relative_link_path.replace('\\', '/')
                            except ValueError as e:
                                print(f"  Предупреждение: Не удалось рассчитать относительный путь для '{lemma}' ({target_file_rel_path_str}) из '{md_file_path}': {e}")
                                continue

                            # Создаем ссылку, ИСПОЛЬЗУЯ ОРИГИНАЛЬНЫЙ ТОКЕН
                            original_token_text = token['text']

                            # Доп. проверка: не является ли токен частью плейсхолдера?
                            # Ищем плейсхолдеры в соседних токенах (если они есть)
                            is_near_placeholder = False
                            if i > 0 and PLACEHOLDER_SUFFIX in processed_tokens[i-1]['text']:
                                is_near_placeholder = True
                            if i < len(processed_tokens) - 1 and PLACEHOLDER_PREFIX in processed_tokens[i+1]['text']:
                                is_near_placeholder = True
                            # Проверяем сам токен (хотя токенизатор должен разделять)
                            if PLACEHOLDER_PREFIX in original_token_text or PLACEHOLDER_SUFFIX in original_token_text:
                                is_near_placeholder = True

                            if is_near_placeholder:
                                # print(f"    Пропуск (Lemma) '{original_token_text}' - рядом/внутри плейсхолдера.")
                                continue

                            replacement = f"[{original_token_text}]({relative_link_path})"

                            # Обновляем токен
                            processed_tokens[i]['text'] = replacement
                            processed_tokens[i]['linked'] = True # Помечаем как связанный
                            links_added += 1
                            links_added_lemma += 1
                            print(f"    + [Lemma] Добавлена ссылка: [{original_token_text}]({relative_link_path}) (Лемма: {lemma})")

            # Собираем текст обратно из токенов, если были лемма-ссылки
            if links_added_lemma > 0:
                processed_text = "".join([t['text'] for t in processed_tokens])
        except Exception as e:
             print(f"  Неожиданная ошибка при обработке Lemma-тем: {e}")
             # Продолжаем без лемма-ссылок

    # 4. Восстанавливаем замаскированные блоки
    final_content = unmask_content(processed_text, placeholders)

    # 5. Записываем изменения, если они были
    if links_added > 0 and final_content != original_content:
        print(f"  Внесено ссылок: {links_added_multi} (Multi) + {links_added_lemma} (Lemma) = {links_added} в файл: {md_file_path.name}")
        if not dry_run:
            try:
                with open(md_file_path, 'w', encoding=file_encoding) as f:
                    f.write(final_content)
            except Exception as e:
                print(f"Ошибка записи файла {md_file_path}: {e}")
                # Не сбрасываем счетчик, т.к. ссылки были найдены
        else:
            print(f"  (Dry Run) Изменения не записаны.")
        return links_added
    else:
        # print(f"  Ссылки не добавлены в файл: {md_file_path.name}")
        return 0

# --- Функции маскировки (без изменений) ---
MASK_PATTERN = r"""
    (?P<markdown_link>\[.*?\]\(.*?\)) | # Markdown links [...] (...)
    (?P<html_link><a\s[^>]*>.*?</a>) | # HTML links <a>...</a>
    (?P<inline_code>`+[^`]+`+) |       # Inline code ``...``
    (?P<fenced_code>```[\s\S]*?```) | # Fenced code blocks ```...```
    (?P<html_code><code.*?>[\s\S]*?</code>) # HTML code blocks <code>...</code>
"""
MASK_REGEX = re.compile(MASK_PATTERN, re.VERBOSE | re.IGNORECASE)
PLACEHOLDER_PREFIX = "___MASKED_CONTENT_"
PLACEHOLDER_SUFFIX = "___"

def mask_content(text):
    """Заменяет найденные паттерны на плейсхолдеры."""
    placeholders = {}
    count = [0] # Используем список для изменения внутри replacer

    def replacer(match):
        placeholder = f"{PLACEHOLDER_PREFIX}{count[0]}{PLACEHOLDER_SUFFIX}"
        # Берем группу, которая не None
        key = next(key for key, value in match.groupdict().items() if value is not None)
        placeholders[placeholder] = match.group(key)
        count[0] += 1
        return placeholder

    masked_text = MASK_REGEX.sub(replacer, text)
    # print(f"Masked {count[0]} items. Placeholders: {list(placeholders.keys())[:5]}...")
    return masked_text, placeholders

def unmask_content(text, placeholders):
    """Восстанавливает оригинальный контент из плейсхолдеров."""
    # Итерируем в обратном порядке номеров на всякий случай
    # (хотя при уникальных плейсхолдерах порядок не так важен)
    processed_placeholders = 0
    missing_placeholders = 0
    # Сортируем ключи по номеру (на всякий случай, если генерация была нестрогой)
    sorted_keys = sorted(placeholders.keys(), key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)

    for placeholder in sorted_keys:
        # Используем count=1 для замены только одного вхождения за раз, если вдруг дубликаты
        new_text, num_replaced = re.subn(re.escape(placeholder), placeholders[placeholder], text, count=1)
        if num_replaced > 0:
            text = new_text
            processed_placeholders += 1
        else:
             # Это может случиться, если плейсхолдер оказался внутри другого при замене
             # print(f"Предупреждение: Плейсхолдер {placeholder} не найден при размаскировке.")
             missing_placeholders += 1

    if PLACEHOLDER_PREFIX in text:
        print(f"Предупреждение: В тексте остались незамененные плейсхолдеры! ({text.count(PLACEHOLDER_PREFIX)})")
    # print(f"Unmasked {processed_placeholders} items. Missing: {missing_placeholders}.")
    return text


# --- Основной блок ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Автоматически проставляет кросс-ссылки в Markdown файлах KidBook.")
    parser.add_argument(
        "--kidbook-dir", type=Path, default=DEFAULT_KIDBOOK_ROOT,
        help=f"Путь к корневой папке KIDBOOK с .md файлами (по умолчанию: {DEFAULT_KIDBOOK_ROOT})"
    )
    parser.add_argument(
        "--work-dir", type=Path, default=DEFAULT_WORK_ROOT,
        help=f"Путь к корневой папке WORK с concepts.json файлами (по умолчанию: {DEFAULT_WORK_ROOT})"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Выполнить прогон без реальной записи изменений в файлы."
    )
    parser.add_argument(
        "--no-lemma", action="store_true",
        help="Отключить использование pymorphy3 для лемматизации однословных тем."
    )

    args = parser.parse_args()

    use_lemma_flag = not args.no_lemma

    if use_lemma_flag and not PYMORPHY_AVAILABLE:
        print("Лемматизация запрошена, но pymorphy3 недоступен. Будет использоваться только точное совпадение.")
        use_lemma_flag = False
    elif not use_lemma_flag:
         print("Лемматизация отключена пользователем.")


    KIDBOOK_ROOT = args.kidbook_dir
    WORK_ROOT = args.work_dir
    # Определяем корень проекта как родителя папки WORK
    # Важно, чтобы и KIDBOOK, и WORK были внутри этого корня
    PROJECT_ROOT = WORK_ROOT.resolve().parent
    # Перепроверяем пути относительно найденного корня
    KIDBOOK_ROOT = PROJECT_ROOT / KIDBOOK_ROOT.name
    WORK_ROOT = PROJECT_ROOT / WORK_ROOT.name


    print(f"--- Запуск скрипта кросс-линковки ---")
    print(f"Корень проекта: {PROJECT_ROOT}")
    print(f"Папка KidBook: {KIDBOOK_ROOT}")
    print(f"Папка Work: {WORK_ROOT}")
    print(f"Использование лемматизации: {'Включено' if use_lemma_flag else 'Отключено'}")
    if args.dry_run:
        print("РЕЖИМ ПРОБНОГО ЗАПУСКА (Dry Run): Изменения не будут сохранены.")

    start_time = time.time()

    # 1. Загрузить все концепты
    print("\nШаг 1: Поиск и загрузка всех концептов...")
    concepts = load_all_concepts(WORK_ROOT)
    if not concepts:
        print("Концепты не найдены или не удалось загрузить. Выход.")
        exit()

    # 2. Предобработка концептов
    single_lemma_map, multi_concepts = preprocess_concepts(concepts, use_lemma=use_lemma_flag)

    # 3. Найти все .md файлы для обработки
    print("\nШаг 2: Поиск Markdown файлов для обработки...")
    md_files = find_md_files(KIDBOOK_ROOT)
    print(f"Найдено {len(md_files)} .md файлов.")
    if not md_files:
        print("Markdown файлы не найдены. Выход.")
        exit()

    # 4. Обработать каждый файл
    print("\nШаг 3: Обработка файлов и добавление ссылок...")
    total_links_added = 0
    files_processed = 0
    files_changed = 0

    for md_file in md_files:
        relative_md_path = md_file.relative_to(PROJECT_ROOT)
        print(f"\nОбработка файла: {relative_md_path}")
        try:
            links_in_file = create_links_in_file(
                md_file,
                single_lemma_map,
                multi_concepts,
                PROJECT_ROOT,
                use_lemma=use_lemma_flag,
                dry_run=args.dry_run
            )
            files_processed += 1
            if links_in_file > 0:
                total_links_added += links_in_file
                files_changed += 1
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА при обработке файла {relative_md_path}: {e}")
            # Можно добавить traceback для отладки
            # import traceback
            # traceback.print_exc()


    end_time = time.time()
    print("\n--- Обработка завершена ---")
    print(f"Обработано файлов: {files_processed}")
    print(f"Изменено файлов: {files_changed}")
    print(f"Всего добавлено ссылок: {total_links_added}")
    print(f"Затраченное время: {end_time - start_time:.2f} сек.")
    if args.dry_run:
        print("РЕЖИМ ПРОБНОГО ЗАПУСКА (Dry Run): Изменения НЕ были сохранены.")