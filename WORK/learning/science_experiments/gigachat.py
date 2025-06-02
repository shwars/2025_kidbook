import requests
import certifi
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def get_token(api_key):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': 'a86a1121-efe1-4b51-b12d-6c91a4d79145',
        'Authorization': f'Basic {api_key}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            token_data = response.json()

            with open('token_data.json', 'w', encoding='utf-8') as f:
                json.dump(token_data, f, ensure_ascii=False, indent=0)

            return token_data
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None

def llm_request(access_token, request):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
      "model": "GigaChat-Max",
      "messages": [
        {
          "role": "system",
          "content": "Объясняй для 10летних детей."
        },
        {
          "role": "user",
          "content": request
        }
      ],
      "stream": False,
      "update_interval": 0,
      "max_tokens": 10000
    })

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            llm_data = response.json()
            return llm_data["choices"][0]["message"]["content"]
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None


def main():
    load_dotenv()

    if not os.path.exists("token_data.json"):
        get_token(os.getenv("API_KEY"))

    with open('token_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    expires_date = datetime.fromtimestamp(data["expires_at"] / 1000)

    print(expires_date - datetime.now() > timedelta(minutes=30))

    if (expires_date - datetime.now() < timedelta(minutes=30)):
        get_token(os.getenv("API_KEY"))
        with open('token_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

    input_prompt = input("Введите промпт: ")

    print(llm_request(data["access_token"], input_prompt))

if __name__ == "__main__":
    main()