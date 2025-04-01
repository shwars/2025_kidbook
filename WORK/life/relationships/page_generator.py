import os
from dotenv import load_dotenv
import gigachat
from gigachat.models import Chat, Messages, MessagesRole


load_dotenv()

concepts = [
    "Дружба", "Семья", "Командная работа", "Лидерство", "Конфликты",
    "Эмпатия", "Общение", "Разнообразие", "Ссоры", "Забота о других",
    "Понимание себя", "Социальные навыки", "Принятие решений", "Доброта",
    "Поддержка", "Чувство вины и прощение", "Открытость", "Уважение",
    "Взаимопомощь", "Мирное разрешение конфликтов"
]


def generate_content(concept: str) -> str:

    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    if not credentials:
        raise ValueError("GIGACHAT_CREDENTIALS не найдены в .env файле!")

    prompt = (
        f"Объясни понятие '{concept}' так, чтобы понял десятилетний ребенок. Каждое понятие должно быть расписано в 5 абзацев. "
        "В каждом абзаце по 5 длинных предложения. Каждый абзац должен иметь заголовок. Сделай в конце вывод. Не нужно писать слово заголовок при новом заголовке."
    )

    payload = Chat(
        messages=[
            Messages(role=MessagesRole.SYSTEM, content="Ты дружелюбный помощник, объясняющий понятия детям."),
            Messages(role=MessagesRole.USER, content=prompt)
        ],
        temperature=0.7,
        max_tokens=500
    )

    try:
        client = gigachat.GigaChat(credentials=credentials, verify_ssl_certs=False)
        response = client.chat(payload)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при генерации контента для {concept}: {e}")
        return ""


def save_to_md(concept: str, content: str):
    filename = f"../../../KIDBOOK/life/relationships/{concept.lower().replace(' ', '-')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {concept}\n\n{content}")


def main():
    os.makedirs("relationships", exist_ok=True)
    for concept in concepts:
        content = generate_content(concept)
        if content:
            save_to_md(concept, content)
            print(f"Сгенерирован файл для: {concept}")


if __name__ == "__main__":
    main()