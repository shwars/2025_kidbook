import os
import json
import requests

GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
GIGACHAT_API_KEY = input()


def generate_markdown(concept):
    prompt = (
        f"Объясни понятие '{concept}' для десятилетнего ребенка. "
        "Напиши текст в формате Markdown, который включает заголовок и доступное объяснение."
    )
    headers = {
        "Authorization": f"Bearer {GIGACHAT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "GigaChat-Plus",
        "messages": [
            {"role": "system", "content": "Ты – эксперт по созданию образовательных текстов для детей."},
            {"role": "system", "content": "Ты весёлый помощник поэтому используешь эмоджи."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    response = requests.post(GIGACHAT_API_URL, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"# {concept}\n\nОшибка генерации текста."


def main():
    input_json_path = "concepts.json"
    with open(input_json_path, "r", encoding="utf-8") as f:
        concepts_data = json.load(f)

    output_dir = "concepts"
    os.makedirs(output_dir, exist_ok=True)

    generated_concepts = {}

    for concept in concepts_data.keys():
        print(f"Генерация описания для понятия: {concept}")
        markdown_text = generate_markdown(concept)
        file_name = concept.lower().replace(" ", "_") + ".md"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        generated_concepts[concept] = {
            "файл": file_path,
            "отношения": concepts_data[concept]
        }

    # Сохраняем обновленный файл concepts.json в папке WORK
    work_dir = "WORK"
    os.makedirs(work_dir, exist_ok=True)
    output_json_path = os.path.join(work_dir, "concepts.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(generated_concepts, f, ensure_ascii=False, indent=4)

    print("Генерация завершена! Markdown-странички сохранены в папке KIDBOOK, обновленный concepts.json в WORK.")


if __name__ == "__main__":
    main()
