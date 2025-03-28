""" Получения понятий, связанных с эмоциями """

import json
from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# SPARQL-запрос для поиска только экземпляров (instances)
#Q9415 -- эмоции
#Q123414 -- стресс

query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?concept ?conceptLabel ?instance ?instanceLabel WHERE {
  # Список классов, для которых ищем экземпляры
  VALUES ?concept { wd:Q123414 wd:Q180015 }
  
  # Ищем все экземпляры для каждого класса
  ?instance wdt:P31 ?concept .
  
  # Получаем метки для классов и экземпляров
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "en". 
    ?concept rdfs:label ?conceptLabel .
    ?instance rdfs:label ?instanceLabel .
  }
}
"""

sparql.setQuery(query)
sparql.setReturnFormat(JSON)

try:
    results = sparql.query().convert()

    grouped_results = {}
    for result in results["results"]["bindings"]:
        concept_uri = result["concept"]["value"]
        concept_label = result.get("conceptLabel", {}).get("value", "No label")
        instance_uri = result["instance"]["value"]
        instance_label = result.get("instanceLabel", {}).get("value", "No label")
        
        if concept_uri not in grouped_results:
            grouped_results[concept_uri] = {
                "label": concept_label,
                "instances": []
            }
        grouped_results[concept_uri]["instances"].append((instance_uri, instance_label))

    
    with open('concepts_new.json', 'w', encoding='utf-8') as file:
        data = {}
        for concept_uri, topics in grouped_results.items():
            data['key'] = topics['label']
            
            inst = []
            for instance_uri, instance_label in topics["instances"]:
                inst.append(instance_label)

            data['emotions'] = inst
        json.dump(data, file, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")
