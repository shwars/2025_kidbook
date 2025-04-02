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
        "max_tokens": 1024,  # Максимальное количество токенов в ответе
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

        file_name = f"{concept.replace(' ', '_')}.md"
        file_path = os.path.join(path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
           f.write(md_content)

        print(f"Markdown-страница '{concept}' создана: {file_path}")

        # Обновление concepts.json
        concepts_json_path = os.path.join(os.path.dirname(__file__), "concepts.json")
        concept_key = concept.lower()  # Ключ в нижнем регистре

        # Загрузка или создание данных
        if os.path.exists(concepts_json_path):
            with open(concepts_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"concepts": {}}

        # Добавление новой записи
        data["concepts"][concept_key] = file_name

        # Сохранение обновлённых данных
        with open(concepts_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Не удалось создать файл для понятия '{concept}'")


def capitalize_first_letter(s):
    return s[0].upper() + s[1:] if s else s

def extract_concepts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return [capitalize_first_letter(item.get('itemLabel', '')) 
            for item in data 
            if item.get('itemLabel')]


if __name__ == "__main__":
    concepts = extract_concepts('data_j.json')
    print(concepts)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    target_dir = os.path.join(base_dir, "KIDBOOK", "world", "technology")

    for concept in concepts:
       create_md_file(target_dir, concept)