import os
import time
from gigachat.api import Gigachat
import argparse


def read_prompts_from_file(file_path, separator='\n\n'):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        prompts = content.split(separator)
        return prompts


def send_to_gigachat(client, prompt):
    response = client.chat(
        model='giga',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    API_KEY = os.environ.get('GIGACHAT_API_KEY')
    
    if not API_KEY:
        raise ValueError("Не найден API ключ в переменной окружения GIGACHAT_API_KEY.")
        
    client = Gigachat(api_key=API_KEY)
    
    parser = argparse.ArgumentParser(description="Отправка запросов к Gigachat из файла.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Путь к файлу с запросами.")
    args = parser.parse_args()
    
    prompts = read_prompts_from_file(args.file)
    
    for i, prompt in enumerate(prompts):
        try:
            response = send_to_gigachat(client, prompt.strip())
            print(f'Запрос #{i+1}: {prompt}')
            print(f'Ответ: {response}')
            print('\n')
            
            time.sleep(0.5)
        except Exception as e:
            print(f'Ошибка при выполнении запроса: {e}')