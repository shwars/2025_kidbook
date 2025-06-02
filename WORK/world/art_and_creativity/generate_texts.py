import ai_api
import json

def generate_aricle(title, text, titles):
    return ai_api.send_message(ai_api.get_token(ai_api.auth_token), ai_api.generate_prompt(title, text, titles))

def save_string_to_file(string, filename):
    try:
        with open(filename, 'w') as file:
            file.write(string)
        print(f"Содержимое успешно сохранено в файл '{filename}'.")
    except Exception as e:
        print(f"Произошла ошибка при сохранении в файл: {e}")

def parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON из файла '{file_path}'.")

data = parse_json('articles.json')
titles = [item['title'] for item in data]
concepts = []

for item in data:
    save_string_to_file(generate_aricle(item['title'], item['text'], titles), f'../../KIDBOOK/{item['title']}.md')
    concepts.append({'name': item['title'], 'file': f'{item['title']}.md'})

result = {'concepts': concepts}

with open("concepts.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4) 