import os
from pathlib import Path
from dotenv import load_dotenv
from gigachat import GigaChat
from langchain_core.prompts import PromptTemplate


class ConceptMarkdownGenerator:
    def __init__(self, concepts: list, base_dir: Path, llm: GigaChat):
        self.concepts = concepts
        self.base_dir = base_dir
        self.llm = llm
        self._create_directory()

    def _create_directory(self):
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True)
        print(f"Путь для сохранения: {self.base_dir.resolve()}")

    def generate_markdown_for_concept(self, concept: str) -> None:
        prompt = self._create_prompt(concept)
        content = self._get_content_from_prompt(prompt)
        self._save_markdown_file(concept, content)

    def _create_prompt(self, concept: str) -> str:
        return PromptTemplate(
            input_variables=['query'],
            template=self._get_prompt_template()
        ).format(query=concept)

    def _get_prompt_template(self) -> str:
        return """
        Ты — опытный тьютор , которай должен составить подробную, информативную и структурированную статью по заданному понятию, предназначенную для аудитории 10-летних детей. Твоя задача — сделать текст таким, чтобы он был не только познавательным, но и интересным для этой аудитории, чтобы они захотели узнать больше и применить знания в своей жизни.
        Необходимо:
        1. Включить **жирным шрифтом** все термины, относящиеся к другим понятиям из списка, которые могут помочь раскрыть тему.
        2. Обеспечить лёгкость восприятия текста, добавив яркие, современные слова, а также включить подходящие эмодзи и смайлики для более дружелюбного и интересного стиля. Например, много смайликов и эмодзи, которые делают текст веселее.
        3. Начать с чёткого определения заданного понятия.
        4. Включить примеры, ориентированные на жизнь детей, которые помогут лучше понять и раскрыть суть понятия. Примеры не должны быть связаны с "Счастьем", если оно не является основным понятием.
        5. Для всех ключевых терминов создать сноски с объяснением.
        6. Завершить статью коротким, но полезным выводом, который поможет детям запомнить основные идеи.
        7. Статья должна быть в формате Markdown.
        
        Основные понятия, которые могут быть использованы: ["Счастье", "Радость", "Дружба", "Любовь", "Семья", "Игры", "Хобби", "Отдых", "Улыбка", "Помощь_другим", "Природа", "Путешествия", "Музыка", "Кулинария", "Спорт", "Еда"].
        
        Статья должна быть ориентирована на понятность для детей 10 лет, поэтому избегай излишней сложности в языке и учитывай их восприятие.
        
        Напиши статью о понятии: {query}
        """

    def _get_content_from_prompt(self, prompt: str) -> str:
        response = self.llm.chat(prompt)
        return response.choices[0].message.content

    def _save_markdown_file(self, concept: str, content: str) -> None:
        file_path = self.base_dir / f"{concept}.md"
        file_path.write_text(content, encoding="utf-8")
        print(f"Файл создан: {file_path}")


def initialize_llm() -> GigaChat:
    giga_chat_key = os.getenv("GIGA_CHAT_KEY")
    if not giga_chat_key:
        raise ValueError("Не задан ключ авторизации.")
    return GigaChat(
        credentials=giga_chat_key,
        verify_ssl_certs=False,
        model='GigaChat-2-Max',
        timeout=60
    )


def main():
    load_dotenv()

    concepts = [
        "Счастье", "Радость", "Дружба", "Любовь", "Семья",
        "Игры", "Хобби", "Отдых", "Улыбка", "Помощь_другим",
        "Природа", "Путешествия", "Музыка", "Еда", "Спорт"
    ]

    concepts_dir = Path("../../../KIDBOOK/life/happiness/concepts")
    llm = initialize_llm()
    concept_generator = ConceptMarkdownGenerator(concepts, concepts_dir, llm)

    for concept in concepts:
        concept_generator.generate_markdown_for_concept(concept)


if __name__ == "__main__":
    main()
