import os
import re
from pathlib import Path

MD_DIRS = "A:\\PyToohon\\AI_Labs\\2025_kidbook\\KIDBOOK\\learning\\knowledge_structure\\concepts\\"

class MarkdownLinker:
    def __init__(self, terms_dir=MD_DIRS):
        self.terms_dir = terms_dir
        self.terms = self._load_terms()

    def _load_terms(self):
        """Загружает все термины из названий .md файлов"""
        terms = {}
        for file in Path(self.terms_dir).glob("*.md"):
            term = file.stem.replace("_", " ")
            terms[term.lower()] = file.name
        return terms

    def _process_text(self, text):
        """Заменяет упоминания терминов на ссылки"""
        def replace_match(match):
            # Получаем совпадение либо из первой, либо из второй группы
            term = match.group(1) or match.group(2)
            if term and term.lower() in self.terms:
                return f"[{term}]({self.terms[term.lower()]})"
            return match.group(0)

        # Ищем слова с большой буквы ИЛИ в кавычках
        pattern = r'\b([А-ЯЁA-Z][а-яёa-z]+)\b|«([^»]+)»'
        return re.sub(pattern, replace_match, text)

    def add_links(self):
        """Обрабатывает все .md файлы, добавляя ссылки"""
        for file in Path(self.terms_dir).glob("*.md"):
            try:
                with open(file, "r+", encoding='utf-8') as f:
                    content = f.read()
                    new_content = self._process_text(content)
                    f.seek(0)
                    f.write(new_content)
                    f.truncate()
            except Exception as e:
                print(f"Ошибка при обработке файла {file}: {e}")

# Использование
try:
    linker = MarkdownLinker()
    linker.add_links()
    print("Перекрёстные ссылки успешно добавлены!")
except Exception as e:
    print(f"Произошла ошибка: {e}")