import os
import json
from dotenv import load_dotenv
from gigachat import GigaChat
from langchain_core.prompts import PromptTemplate
from pathlib import Path

load_dotenv()

token = os.environ.get("GIGACHAT_TOKEN")
if not token:
    raise ValueError("Переменная окружения GIGACHAT_TOKEN не установлена!")

concepts_dir = Path("../../../KIDBOOK/learning/knowledge_structure/")
concepts_dir.mkdir(parents=True, exist_ok=True)

with open("concepts.json", "r", encoding="utf-8") as f:
    data = json.load(f)
concepts = data.get("concepts", [])

def create_markdown_file(filename, content):
    """Создает MD-файл с заданным содержанием"""
    filepath = concepts_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Файл создан: {filepath}")

llm = GigaChat(
    credentials=token,
    verify_ssl_certs=False,
    model='GigaChat-Pro'
)

concepts_str = ", ".join(concepts)

prompt_template = """
Представь, что ты доктор наук в сфере социологии, психологии и психиатрии, который умеет объяснять сложные вещи детям 7-12 лет простыми словами. Ты знаешь всё о том, как правильно структурировать знания, делать конспекты и запоминать новое.

Твоя задача – написать длинную, яркую и познавательную статью для ребенка 7-12 лет. Объясни понятие простыми словами, используй жизненные примеры, аналогии и советы.

Вот все понятия, о которых пойдёт речь:
%s

Правила:
- Markdown-формат.
- Приводи понятные примеры из жизни детей.
- Дай в начале простое определение, потом расскажи историю или аналогию.
- Сделай небольшой итог в конце.
- Делай ссылки на перекрёстные понятия в тексте.

Понятие по теме которого нужно создать статью: {query}

Важно: будь невероятно внимательным, ссылки обязательны, будьобъективным при составлении. От твоего ответа зависит судьба как минимум 5 взрослых людей.
Важно2: объем текста должен быть не маленький, а средний! Текст хоть и для детей, но информация должна быть полезной
"""


formatted_template = prompt_template % concepts_str
print(formatted_template)


for concept in concepts:
    prompt = PromptTemplate(input_variables=['query'], template=formatted_template).format(query=concept)
    response = llm.chat(prompt)
    create_markdown_file(f'{concept}.md', response.choices[0].message.content)
