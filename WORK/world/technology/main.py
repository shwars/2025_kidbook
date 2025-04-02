import requests
import json
import os

from config import settings

def generate_text(concept):
    prompt = f"""
    Напиши подробное описание понятия "{concept}" в формате Markdown и объясни его для десятилетнего ребенка.
    Включи:
    - Введение: краткое определение
    - Историю появления
    - Как работает (технические аспекты)
    - Влияние на общество
    - Преимущества и недостатки
    - Будущее развития
    Добавь заголовки, списки, ссылки и изображения.
    """

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {"role": "system", "content": "Ты эксперт в написании статей."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {settings.ACCESS_TOKEN}'  # Токен авторизации
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def create_md_file(path, concept):
    md_content = generate_text(concept)

    if md_content:
        if path == 'md_files': os.makedirs("md_files", exist_ok=True)

        file_path = f"{path}/{concept.replace(' ', '_')}.md"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Markdown-страница '{concept}' создана: {file_path}")


if __name__ == "__main__":
    concepts = ['Азбука', 'Интернет', 'Электричество', 'Поезда']

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    target_dir = os.path.join(base_dir, "KIDBOOK", "world", "technology")

    for concept in concepts:
        create_md_file(target_dir, concept)