import requests
import json
import os

from pathlib import Path
from config import settings

def capitalize_first_letter(s):
    return s[0].upper() + s[1:] if s else s

def extract_concepts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return [capitalize_first_letter(item.get('itemLabel', '')) 
            for item in data 
            if item.get('itemLabel')]

def generate_text(concept):
    prompt = f"""
Ты — талантливый детский писатель и педагог с 20-летним опытом. Напиши главу о "{concept}" для энциклопедии "Удивительный мир вокруг нас", предназначенной для любознательных 10-летних читателей

Инструкции:

1. Введение: Напишите краткое и понятное определение '{concept}', выделив самое важное, чтобы ребенок смог легко понять суть.

2. История: Расскажите увлекательную историю появления '{concept}', адаптированную для юного ума, чтобы вызвать интерес и понимание.

3. Принципы работы: Объясните, как работает '{concept}', раскрывая технические аспекты с учетом детских возможностей восприятия, избегая сложных терминов, но сохраняя важные детали.

4. Влияние: Опишите, какое влияние оказало '{concept}' на общество, делая акцент на примерах, которые ребенок может увидеть в своей повседневной жизни.

5. Интересный факт: Для закрепления интереса к теме у юного читателя приведи реальный факт, который впечатлит юный ум читателя

Правила:
- Напиши длинную главу
- Используй словарь 4-го класса.
- Добавляй эмодзи.
- Структурируй описание так, чтобы оно было понятно и интересно ребенку.
- Если будет полезно для раскрытия понятия упомянуть связь со следующими темами: [3D-печать, Интернет, Радиоизлучение, Автомобиль, Мобильный телефон, Оптика, Паровой двигатель, Персональный компьютер, Поезд, Радио, Робот, Ручной типографский станок, Самолёт, Судно, Телефон, Фабрика, Электричество]. Но не перегружай главу, если она уже достаточна сложная для понимания 10-ти летним ребенком
    """

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-2-Max",  # Используемая модель
        "messages": [
            {"role": "system", "content": "Ты эксперт в написании статей."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        #"max_tokens": 1024,  # Максимальное количество токенов в ответе
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
    
    if not md_content:
        print(f"Не удалось создать файл для понятия '{concept}'")
        return None
    
    if path == 'md_files':
        os.makedirs("md_files", exist_ok=True)
    
    file_name = f"{concept.replace(' ', '_')}.md"
    file_path = os.path.join(path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Markdown-страница '{concept}' создана: {file_path}")
    return file_name

def update_concepts_json(md_folder_path):
    concepts_data = {}
    
    try:
        md_files = list(Path(md_folder_path).glob("*.md"))
    except Exception as e:
        print(f"Ошибка при чтении директории: {str(e)}")
        return

    for md_file in md_files:
        concept_name = md_file.stem.replace('_', ' ')
        concepts_data[concept_name.lower()] = md_file.name

    concepts_json_path = Path(__file__).parent / "concepts.json"
    
    if concepts_json_path.exists():
        with open(concepts_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"concepts": {}}

    data["concepts"] = concepts_data
    
    with open(concepts_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Обновлено записей в concepts.json: {len(concepts_data)}")

if __name__ == "__main__":
    concepts = extract_concepts('data_j.json')
    print(concepts)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    target_dir = os.path.join(base_dir, "KIDBOOK", "world", "technology")

    concepts = extract_concepts('data_j.json')
    for concept in concepts:
        create_md_file(target_dir, concept)
    update_concepts_json(target_dir)