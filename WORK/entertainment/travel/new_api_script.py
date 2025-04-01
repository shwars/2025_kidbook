import requests
import json
import os
import uuid

# Встроенный JSON данных
DATA = {
    "elements": [
        {
            "label": "Путешествия",
            "relations": [
                "Виды",
                "Транспорт",
                "Снаряжение"
            ]
        },
        {
            "label": "Виды",
            "relations": [
                "Бэкпекинг",
                "Свадебное путешествие",
                "Кругосветное путешествие",
                "Бомж-тур",
                "Автопутешествие",
                "Круиз",
                "Велосипедный отпуск"
            ]
        },
        {
            "label": "Транспорт",
            "relations": [
                "Авиация",
                "Поезд",
                "Автомобиль",
                "Судно",
                "Велосипед"
            ]
        },
        {
            "label": "Снаряжение",
            "relations": [
                "Багаж",
                "Чемодан",
                "Рюкзак"
            ]
        },
        {
            "label": "Бэкпекинг",
            "relations": []
        },
        {
            "label": "Свадебное путешествие",
            "relations": []
        },
        {
            "label": "Кругосветное путешествие",
            "relations": []
        },
        {
            "label": "Бомж-тур",
            "relations": []
        },
        {
            "label": "Автопутешествие",
            "relations": []
        },
        {
            "label": "Круиз",
            "relations": []
        },
        {
            "label": "Велосипедный отпуск",
            "relations": []
        },
        {
            "label": "Авиация",
            "relations": []
        },
        {
            "label": "Поезд",
            "relations": []
        },
        {
            "label": "Автомобиль",
            "relations": []
        },
        {
            "label": "Судно",
            "relations": []
        },
        {
            "label": "Велосипед",
            "relations": []
        },
        {
            "label": "Багаж",
            "relations": []
        },
        {
            "label": "Чемодан",
            "relations": []
        },
        {
            "label": "Рюкзак",
            "relations": []
        }
    ],
    "special_relations": [
        {
            "type": "implementation",
            "from": "Судно",
            "to": "Круиз"
        },
        {
            "type": "implementation",
            "from": "Автомобиль",
            "to": "Автопутешествие"
        },
        {
            "type": "implementation",
            "from": "Велосипед",
            "to": "Велосипедный отпуск"
        },
        {
            "type": "inheritance",
            "from": "Чемодан",
            "to": "Багаж"
        },
        {
            "type": "inheritance",
            "from": "Рюкзак",
            "to": "Багаж"
        }
    ]
}

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }
    payload = {'scope': scope}

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

# Получение токена авторизации
auth_token = "NzQ3YjhiNzctNjYxZC00YmRkLWIyYmUtOGViMDZjMzZiYWRmOjkzY2UzYWJhLTFmMjktNDc4My1iYzIyLWQzMjgzODI2MGExMw=="
response = get_token(auth_token)
if response != -1:
    token = response.json()['access_token']



def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 4000,
        "repetition_penalty": 1,
        "update_interval": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1

def main():
    term = input("Введите термин: ").strip()
    
    # Поиск элемента и сбор связей
    element = next((el for el in DATA['elements'] if el['label'] == term), None)
    if not element:
        print(f"Термин '{term}' не найден в базе данных")
        return

    # Собираем все связи
    relations = set(element['relations'])
    
    # Добавляем связи из special_relations
    for rel in DATA['special_relations']:
        if rel['from'] == term:
            relations.add(rel['to'])
        elif rel['to'] == term:
            relations.add(rel['from'])
    
    relations_str = ", ".join(relations) if relations else "отсутствуют"
    
    prompt = f'''Объясни термин "{term}" для десятилетнего ребенка, не забудь упомянуть про: {relations_str}. Используй большое количество эмодзи! Можешь использовать оформление текста для формата md. Ответ должен быть полностью на русском.'''
    
    answer = get_chat_completion(token, prompt)
    if answer == -1:
        print("Ошибка при обращении к ИИ")
        return
    
    try:
        output_text = answer.json()['choices'][0]['message']['content']
    except KeyError:
        print("Ошибка формата ответа от API")
        return

    # Создаем директорию, если её нет
    os.makedirs("concepts", exist_ok=True)
    
    # Записываем результат в файл
    with open(f"concepts/{term.lower().replace(' ', '_')}.md", "w", encoding="utf-8") as file:
        file.write(output_text)
    
    print(f"Результат сохранен в concepts/{term.lower().replace(' ', '_')}.md")
    return 0

if __name__ == "__main__":
    main()
