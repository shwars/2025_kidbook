import os
import json
import uuid
import requests
from dotenv import load_dotenv
from pathlib import Path
from time import sleep

# Загрузка токена
load_dotenv()

# Пути (абсолютные)
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Корень репозитория
CONCEPTS_FILE = BASE_DIR / "WORK/learning/school/concepts.json"
OUTPUT_DIR = BASE_DIR / "KIDBOOK/learning/school/api_generated"

AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")

def get_access_token() -> str:
    """Получает временный access token через OAuth"""
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),  # Генерируем уникальный ID запроса
        'Authorization': f'Basic {AUTH_KEY}'
    }
    
    payload = {'scope': 'GIGACHAT_API_PERS'}
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print(f"Ошибка получения токена: {e}")
        return ""

def generate_text_with_gigachat(prompt: str, token: str) -> str:
    """Генерирует текст через GigaChat API"""
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    data = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            verify=False,
            timeout=20
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Ошибка генерации текста: {e}")
        return ""

def generate_articles():
    """Основная функция генерации статей"""
    # Получаем access token
    access_token = get_access_token()
    if not access_token:
        print("Не удалось получить access token!")
        return

    # Загружаем концепты
    with open(CONCEPTS_FILE, 'r', encoding='utf-8') as f:
        concepts = json.load(f)["Школа"]["concepts"]
    
    # Генерируем статьи
    for concept in concepts:
        term = concept["name"]
        filename = concept["file"]
        
        # Формируем путь
        output_path = OUTPUT_DIR / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Создаем промпт
        prompt = (
            f"Напиши детскую энциклопедическую статью о '{term}' для детей 10 лет. "
            "Требования:\n"
            "- Простым языком с примерами\n"
            "- Используй подзаголовки уровня ##\n"
            "- Формат: Markdown"
        )
        
        # Генерируем текст
        print(f"Генерация статьи: {term}")
        article = generate_text_with_gigachat(prompt, access_token)
        
        # Сохраняем результат
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {term}\n\n{article}")
        
        sleep(1)  # Задержка между запросами

if __name__ == "__main__":
    generate_articles()