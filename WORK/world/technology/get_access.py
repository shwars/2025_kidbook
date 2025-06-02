import requests
from config import settings

def get_access_token(auth_token):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
    'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '706df06a-4973-4746-a97e-400e3cfc4004',
    'Authorization': f'Basic {auth_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response.json()['access_token']
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return None
    
def update_env_file(access_token):
    env_file = settings.model_config['env_file']

    try:
        with open(env_file, 'r') as file:
            lines = file.readlines()
        
        updated = False
        new_lines = []
        for line in lines:
            if line.startswith('ACCESS_TOKEN='):
                new_lines.append(f'ACCESS_TOKEN={access_token}\n')
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            new_lines.append(f'\nACCESS_TOKEN={access_token}\n')
        
        with open(env_file, 'w') as file:
            file.writelines(new_lines)
        
        print("ACCESS_TOKEN успешно обновлён!")

    except Exception as e:
        print(f"Ошибка при обновлении .env файла: {str(e)}")


if __name__ == "__main__":
    access_token = get_access_token(settings.AUTH_TOKEN)
    if access_token:
        update_env_file(access_token)

    