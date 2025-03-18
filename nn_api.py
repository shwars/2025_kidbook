import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def get_wikipedia_content(qid, lang="ru"):
    wikidata_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    wd_response = requests.get(wikidata_url).json()
    
    sitelinks = wd_response["entities"][qid].get("sitelinks", {})
    wiki_key = f"{lang}wiki"
    if wiki_key not in sitelinks:
        return f"Статья на {lang} Википедии не найдена для {qid}."
    
    title = sitelinks[wiki_key]["title"]
    
    wikipedia_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    wp_response = requests.get(wikipedia_url).json()
    
    if "extract" not in wp_response:
        return f"Содержимое статьи '{title}' не найдено."
    
    return f"📄 {title}\n\n{wp_response['extract']}"

def get_wikidata_id(article_name, lang="ru"):
    url = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT ?item WHERE {{
      ?item rdfs:label "{article_name}"@{lang}.
    }}
    """
    headers = {
        "User-Agent": "PythonWikidataClient/1.0",
        "Accept": "application/json"
    }
    response = requests.get(url, params={"query": query, "format": "json"}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.status_code}")

    data = response.json()
    results = data.get("results", {}).get("bindings", [])
    
    if not results:
        return f"Статья '{article_name}' не найдена в Wikidata."

    item_id = results[0]["item"]["value"].split("/")[-1]
    
    text = get_wikipedia_content(item_id, lang=lang)
    
    return f"🔹 ID статьи '{article_name}' в Wikidata: {item_id}\n\n{text}"

def build_yandexgpt_prompt(folder_id, user_text):
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000",
            "reasoningOptions": {
                "mode": "DISABLED"
            }
        },
        "messages": [
            {
                "role": "system",
                "text": "Объясни текст десятилетнему ребенку"
            },
            {
                "role": "user",
                "text": user_text
            }
        ]
    }
    return json.dumps(data, ensure_ascii=False)

def call_yandex_gpt(prompt_json):
    """
    Делает POST-запрос (эквивалент команды curl):
      curl \
        --request POST \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer ${IAM_TOKEN}" \
        --data "@prompt.json" \
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    prompt_json – готовая JSON-строка, которую отправим в запрос.
    """
    iam_token = os.environ.get("IAM_TOKEN")
    if not iam_token:
        raise ValueError("Не задана переменная окружения IAM_TOKEN!")

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }
    
    response = requests.post(url, headers=headers, data=prompt_json)
    response.raise_for_status()
    return response.json()

def main():
    # Можно изменить статью на любую другую
    article_name = "Альберт Эйнштейн"
    
    wiki_text = get_wikidata_id(article_name, lang="ru")
    print("==== Текст, полученный из Wikipedia ====")
    print(wiki_text)

    folder_id = os.environ.get("FOLDER_ID")
    
    prompt_json = build_yandexgpt_prompt(folder_id, wiki_text)
    
    result = call_yandex_gpt(prompt_json)
    
    print("\n==== Ответ от Yandex GPT ====")
    try:
        gpt_text = result["result"]["alternatives"][0]["message"]["text"]
        print(gpt_text)
    except (KeyError, IndexError):
        print("Не удалось найти корректный ответ в JSON:", result)

if __name__ == "__main__":
    main()
