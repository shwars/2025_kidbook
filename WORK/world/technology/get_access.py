import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

auth_token = ""

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': '706df06a-4973-4746-a97e-400e3cfc4004',
  'Authorization': f'Basic {auth_token}'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)