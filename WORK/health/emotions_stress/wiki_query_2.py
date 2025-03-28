""" Группировка понятий с фильтрацией """

from SPARQLWrapper import SPARQLWrapper, JSON
import re
import json

# Определяем SPARQL-запрос
sparql_query = """
SELECT DISTINCT ?i ?iLabel ?iSub ?iSubLabel
WHERE {
  {
    ?iSub wdt:P279 ?i.
    ?i wdt:P279 wd:Q9415.  # Q9415 - идентификатор понятия эмоции
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,ru". }
  }
}
"""

# Настройка SPARQLWrapper для работы с Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)

# Выполнение запроса и получение результатов
try:
    results = sparql.query().convert()
except Exception as e:
    print(f"Ошибка при выполнении запроса: {e}")
    results = None

# Проверяем, что результаты получены
if results and "results" in results and "bindings" in results["results"]:
    data = results["results"]["bindings"]
else:
    print("Нет данных для обработки.")
    data = []

# Функция для фильтрации данных по шаблону
def filter_by_emotion_keywords(data):
    # Регулярное выражение для поиска однокоренных слов на русском и английском
    pattern = r"(эмоц|emotion)"
    filtered_data = []
    for item in data:
        iLabel = item.get("iLabel", {}).get("value", "")
        if re.search(pattern, iLabel, re.IGNORECASE):  # Используем re.IGNORECASE для игнорирования регистра
            filtered_data.append(item)
    return filtered_data

# Фильтруем данные
filtered_data = filter_by_emotion_keywords(data)

# Группируем данные по iLabel
grouped_data = {}
for item in filtered_data:
    iLabel = item.get("iLabel", {}).get("value", "")
    iSubLabel = item.get("iSubLabel", {}).get("value", "")

    if iLabel not in grouped_data:
        grouped_data[iLabel] = []
    if iSubLabel:  # Добавляем только непустые iSubLabel
        grouped_data[iLabel].append(iSubLabel)

# Сохраняем данные в JSON-файл
output_file = "grouped_data.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(grouped_data, json_file, ensure_ascii=False, indent=4)

print(f"\nДанные успешно сохранены в файл: {output_file}")
