import requests

url = "https://gigachat.devices.sberbank.ru/api/v1/models"

access_token = ""

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {access_token}'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)