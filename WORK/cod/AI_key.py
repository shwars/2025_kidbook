import requests
import uuid
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Функция для получения токена авторизации
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
auth_token = "тут должен быть токен"  
response = get_token(auth_token)

if response != -1 and response.status_code == 200:
    token = response.json().get('access_token', '')

    if token:
        print(f"Токен: {token}")

        # Записываем токен в файл token.txt
        file_path = os.path.join(os.path.dirname(__file__), "token.txt")
        with open(file_path, "w") as file:
            file.write(token)

        print(f"Токен сохранён в файл: {file_path}")
    else:
        print("Ошибка: токен не найден в ответе сервера.")
else:
    print(f"Ошибка {response.status_code}: {response.text}")
