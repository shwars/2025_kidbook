from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx
import matplotlib.pyplot as plt

# Функция для выполнения SPARQL запроса
def run_sparql_query(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# SPARQL запрос для получения хобби и их категорий
query = """
SELECT ?hobby ?hobbyLabel ?category ?categoryLabel WHERE {
  ?hobby wdt:P31 wd:Q47728. # категория
  ?hobby wdt:P279 ?category. # связь с категорией
  VALUES ?categoryLabel {"хобби"}
  VALUES ?hobbyLabel {"вышивание" "кулинария" "рисование" "музыка" "спорт" "садоводство" "настольные игры" "видеоигры" "актерское мастерство" "чтение" "конструирование" "научные эксперименты" "танцы"}

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ru". }
}
"""

# Выполнение запроса
results = run_sparql_query(query)

# Создание графа
G = nx.Graph()

# Словарь для категоризации
category_dict = {
    "вышивание": "творческое",
    "кулинария": "домашнее",
    "рисование": "творческое",
    "музыка": "творческое",
    "спорт": "активное",
    "садоводство": "домашнее",
    "настольные игры": "домашнее",
    "видеоигры": "интеллектуальное",
    "актерское мастерство": "творческое",
    "чтение": "интеллектуальное",
    "конструирование": "творческое",
    "научные эксперименты": "интеллектуальное",
    "танцы": "активное"
}

# Добавление вершин и рёбер в граф
for result in results["results"]["bindings"]:
    hobby = result["hobbyLabel"]["value"]
    category = result["categoryLabel"]["value"]
    
    # Добавляем вершины и связь между ними
    G.add_node(hobby)
    G.add_node(category)
    category_label = category_dict.get(hobby, "неизвестное")
    G.add_edge(hobby, category, label=category_label)

plt.figure(figsize=(12, 12))

# Позиционирование узлов с использованием Spring Layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Рисуем граф
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
plt.title("Граф хобби", fontsize=16)
plt.show()
