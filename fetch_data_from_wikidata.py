import requests


def get_wikipedia_content(qid, lang="ru"):
    # 1. Получаем ссылку на Википедию по Q-ID
    wikidata_url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    response = requests.get(wikidata_url).json()
    
    sitelinks = response["entities"][qid]["sitelinks"]
    if f"{lang}wiki" not in sitelinks:
        return f"Статья на {lang} Википедии не найдена для {qid}."

    title = sitelinks[f"{lang}wiki"]["title"]
    
    # 2. Получаем содержимое статьи из Википедии
    wikipedia_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(wikipedia_url).json()

    if "extract" not in response:
        return f"Содержимое статьи '{title}' не найдено."

    return f"📄 {title}\n\n{response['extract']}"

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

    item_id = results[0]["item"]["value"].split("/")[-1]  # Извлекаем Q-идентификатор
    text = get_wikipedia_content(item_id)

    return f"🔹 ID статьи '{article_name}' в Wikidata: {item_id} \n Text:{text}"

# Пример использования
article_name = "болезнь"  # Замените на нужное название
print(get_wikidata_id(article_name))
