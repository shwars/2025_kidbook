import requests
import os

# Укажи свой API-ключ GigaChat
access_token = ""

# Определение понятия
concept = "Интернет"

# Функция для генерации текста через GigaChat API
def generate_text_gigachat(concept):
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

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": "Ты эксперт в написании статей."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7
    }

    response = requests.post("https://gigachat.devices.sberbank.ru/api/v1/chat/completions", json=payload, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Ошибка:", response.json())
        return None

# Генерируем текст
md_content = generate_text_gigachat(concept)

if md_content:
    # Создаём папку и сохраняем файл
    os.makedirs("md_files", exist_ok=True)
    file_path = f"md_files/{concept.replace(' ', '_')}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Markdown-страница '{concept}' создана: {file_path}")
