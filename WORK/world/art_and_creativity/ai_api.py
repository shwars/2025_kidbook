import requests
import uuid
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        return response.json().get('access_token', '')
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


auth_token = "YzE5MDA0MjEtYmEwYi00ZDc0LWIxMDItNjdhMDA2MmU2YzQ3OjNkOGNkMmU4LWEzMTAtNDMyYy04MzE2LTcxMGZmNTBmMjAzMg=="  
response = get_token(auth_token)

def send_message(access_token, prompt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    prompt = prompt
    payload = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}],  
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Ответ не найден")
        else:
            return f"Ошибка {response.status_code}: {response.text}"
    except requests.RequestException as e:
        return f"Ошибка запроса: {str(e)}"
    
def generate_prompt(title, text, titles):
    return f'Напиши статью о понятии \"{title}\", за основу возьми данный текст на английском: \n\"{text}\"\n перескажи его на русском так, чтобы понял десятилетний ребенок, но определение должно быть строгим, без сюсюканья, в ответе не пиши ничего лишнего, никаких приветствий, вопросов \"Что такое\" и прочего, в статье не должно быть заголовков, по возможности используй в статье какие-то из этих понятий: {', '.join(map(lambda x: f'"{x}"', titles))}'
