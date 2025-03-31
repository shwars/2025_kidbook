import requests
import json
import os
import uuid


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

# Функция для отправки запроса к нейросети и получения результата
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




def main ():
    file = open("concepts/travel.md","w")
    term = input()

    prompt = f'Объясни термин "{term}" для десятилетнего ребенка. Используй большое количество эмодзи! Можешь использовать оформление текста для формата md. '


    
    answer = get_chat_completion(token, prompt)
    if answer == -1:
        print("Ошибка при обращении к ИИ")
    output_text = answer.json()['choices'][0]['message']['content']

    file.write(output_text)

    return 0


if __name__ == "__main__":
    main()