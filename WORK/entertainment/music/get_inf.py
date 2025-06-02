from gigachat import GigaChat
from langchain_core.prompts import PromptTemplate
import os
from getpass import getpass
from pathlib import Path

# Переменная с директорией для сохранения файлов
concepts_dir = Path("")

# Список тем для генерации
concepts = [
    "темы" 
]


def create_markdown_file(filename, content):
    """Создает MD-файл с заданным содержанием"""
    filepath = concepts_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Файл создан: {filepath}")


# Подключаемся к GigaChat
llm = GigaChat(credentials=('your_access_key'), verify_ssl_certs=False, model='GigaChat-Pro')

template = """
    Ваш промпт
    Понятие: {query}
"""

# Проходим по списку тем и создаем MD-файлы
for concept_name in concepts:
    prompt = PromptTemplate(input_variables=['query'], template=template).format(query=concept_name)

    # Отправляем запрос в GigaChat
    response = llm.chat(prompt)

    # Создаем MD-файл с сгенерированным контентом
    create_markdown_file(f'{concept_name}.md', response.choices[0].message.content)


#другой вариант 
def generate_md_file(prompt, filename):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "prompt": prompt,
        "max_tokens": 150,  # Максимальное количество токенов в ответе
        "temperature": 0.7,  # Температура для генерации текста
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result.get('text', 'No response text found.')

        # Сохранение ответа в файл .md
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Файл '{filename}' успешно создан.")
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
