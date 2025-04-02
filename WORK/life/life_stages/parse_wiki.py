import requests
import sys
import pymorphy3.analyzer


def sparql_request(name):
    sparql_url = "https://query.wikidata.org/sparql"

    query = f"""
        SELECT ?item WHERE {{
          ?item rdfs:label "{name}"@ru.
        }}
        """

    headers = {"Accept": "application/sparql-results+json"}

    sparql_response = requests.get(sparql_url, params={"query": query}, headers=headers)

    if sparql_response.status_code != 200:
        raise Exception(f"Failed wikidata request: {sparql_response.status_code}")

    return sparql_response.json()


def get_title_from_wikidata(name):
    results = sparql_request(name).get("results", {}).get("bindings", [])

    if not results:
        return

    qid = results[0]["item"]["value"].split("/")[-1]

    wikidata_url = "https://www.wikidata.org/w/api.php"

    params = {
        "action": "wbgetentities",
        "format": "json",
        "ids": qid,
        "languages": "ru",
        "sitefilter": "ruwiki",
        "formatversion": 2
    }

    wikidata_response = requests.get(wikidata_url, params=params)

    if wikidata_response.status_code != 200:
        raise Exception(f"Failed wikidata request: {wikidata_response.status_code}")

    title = wikidata_response.json().get('entities', {}).get(qid, {}).get('sitelinks', {}).get('ruwiki',
                                                                                               {}).get(
        'title',
        None)

    return title


def wikipedia_request(name):
    wikipedia_url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{name}"

    wikipedia_response = requests.get(wikipedia_url)

    if wikipedia_response.status_code != 200:
        raise Exception(f"Failed wikipedia request: {wikipedia_response.status_code}")

    return wikipedia_response.json()


def get_wikipedia_summary(name):
    ru_wiki_title = get_title_from_wikidata(name)

    wikipedia_data = wikipedia_request(name)

    result = "1. Info without wikidata:\n" + wikipedia_data['extract']

    if ru_wiki_title:
        wikipedia_data = wikipedia_request(ru_wiki_title)

        result += "\n\n2. Info with wikidata:\n" + wikipedia_data['extract']

    return result


def main():
    args = sys.argv

    if len(args) == 1:
        print("No concept given.\nUsage: python parse_wiki.py [concept]")
        return

    morph = pymorphy3.MorphAnalyzer()

    article_name = morph.parse(args[1].lower())[0].normal_form

    print(article_name, '\n')

    wikipedia_summary = get_wikipedia_summary(article_name)

    print(wikipedia_summary)


if __name__ == "__main__":
    main()
