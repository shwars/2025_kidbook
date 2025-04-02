import math
import requests
import networkx as nx
import matplotlib.pyplot as plt

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

query = """
SELECT DISTINCT 
  ?item 
  (SAMPLE(COALESCE(?itemLabelRu, ?itemLabelEn, "Без названия")) AS ?itemLabel)
  (SAMPLE(?itemDescRu) AS ?itemDescriptionRu)
  (SAMPLE(?itemDescEn) AS ?itemDescriptionEn)
WHERE {
  VALUES ?item {
    wd:Q144334   # Печатный станок
    wd:Q83405    # Фабрика (Завод)
    wd:Q11012    # Робот
    wd:Q229367   # 3D-печать
    wd:Q16338    # Персональный компьютер
    wd:Q75       # Интернет
    wd:Q11035    # Телефон
    wd:Q872      # Радио
    wd:Q1420     # Автомобиль
    wd:Q870      # Поезд
    wd:Q197      # Самолет
    wd:Q11446    # Судно
    wd:Q12725    # Электричество
    wd:Q12760    # Паровой двигатель
    wd:Q4262     # Радиоизлучение (Радиоволны)
    wd:Q14620    # Оптика
  }
  
  BIND(wd:Q11028 AS ?center)
  
  OPTIONAL { ?item rdfs:label ?itemLabelRu FILTER(LANG(?itemLabelRu) = "ru") }
  OPTIONAL { ?item rdfs:label ?itemLabelEn FILTER(LANG(?itemLabelEn) = "en") }
  
  OPTIONAL { ?item schema:description ?itemDescRu FILTER(LANG(?itemDescRu) = "ru") }
  OPTIONAL { ?item schema:description ?itemDescEn FILTER(LANG(?itemDescEn) = "en") }
}
GROUP BY ?item
ORDER BY ?itemLabel
"""

def run_sparql_query(query):
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(SPARQL_ENDPOINT, params={'query': query}, headers=headers)
    response.raise_for_status()
    return response.json()

def build_simple_graph(results):
    G = nx.DiGraph()
    
    center_label = "Технологии"
    G.add_node(center_label)

    for result in results["results"]["bindings"]:
        item_label = result["itemLabel"]["value"]
        G.add_node(item_label)
        G.add_edge(center_label, item_label)

    return G

def star_layout(G, center_label, radius=6):
    pos = {}
    pos[center_label] = (0, 0)
    
    others = [n for n in G.nodes() if n != center_label]
    angle_step = 2 * math.pi / len(others) if others else 0
    
    for i, node in enumerate(others):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pos[node] = (x, y)
    return pos

def visualize_graph(G):
    plt.figure(figsize=(10, 8))
    
    center_label = "Технологии"
    pos = star_layout(G, center_label, radius=4)
    
    nx.draw_networkx_nodes(
        G, pos,
        node_color='skyblue',
        node_size=500
    )
    
    nx.draw_networkx_edges(
        G, pos,
        arrows=True,
        arrowstyle='-|>',   
        arrowsize=20,
        width=1,
        connectionstyle='arc3,rad=0.0',
        edge_color='gray'
    )
    

    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title("Представление понятий в виде графа", fontsize=14)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    try:
        results = run_sparql_query(query)
        print("SPARQL-запрос успешно выполнен.")
    except Exception as e:
        print("Ошибка при выполнении SPARQL-запроса:", e)
        exit(1)
    
    G = build_simple_graph(results)
    visualize_graph(G)
