import json
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.offline import plot

from pyvis.network import Network
import os
import tempfile

def load_concepts(json_file):
    """Загружает соответствие названий статей и их файлов из concepts.json"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['concepts']

def find_links(md_content):
    """Находит все ссылки на другие статьи в формате (filename.md)"""
    return re.findall(r'\((.*?\.md)\)', md_content)

def build_ontology(concepts, md_dir="..\\..\\..\\KIDBOOK\\health\\professional_sport\\"):
    """Строит граф связей между статьями"""
    # Создаем граф
    G = nx.DiGraph()
    
    # Добавляем узлы (статьи)
    for title, filename in concepts.items():
        G.add_node(title, filename=filename)
    
    # Создаем обратное отображение: имя файла -> название статьи
    filename_to_title = {v: k for k, v in concepts.items()}
    
    # Анализируем связи между статьями
    for title, filename in concepts.items():
        filepath = os.path.join(md_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = find_links(content)
        for link in links:
            if link in filename_to_title:
                linked_title = filename_to_title[link]
                G.add_edge(title, linked_title)
    
    return G

def visualize_ontology(G, output_file='ontology.png'):
    """Визуализирует граф связей и сохраняет в файл"""
    plt.figure(figsize=(12, 12))
    
    # Позиционирование узлов
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Рисуем граф
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue', alpha=0.9)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    
    plt.title('Онтология профессионального спорта', fontsize=15)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Визуализация сохранена в файл {output_file}")

def visualize_interactive(G, output_file='interactive_ontology.html'):
    """Интерактивная визуализация с Plotly"""
    pos = nx.spring_layout(G, k=0.3, iterations=50)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[],
            line_width=2))
    
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    fig.write_html(output_file)
    print(f"Интерактивная визуализация сохранена в {output_file}")

def pyvis_draggable(G, output_file='pyvis_graph.html'):
    # Создаем временный файл для обхода ошибки
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
        temp_path = tmp.name
    
    net = Network(height="750px", width="100%", directed=True, notebook=False)
    net.from_nx(G)
    
    # Настройки для перетаскивания
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "springLength": 150,
          "springConstant": 0.05
        }
      },
      "interaction": {
        "dragNodes": true,
        "dragView": true
      }
    }
    """)
    
    try:
        net.save_graph(temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            html = f.read()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    finally:
        os.unlink(temp_path)
    
    print(f"Граф сохранен в {output_file}")


def main():
    # Загрузка концептов
    concepts = load_concepts('concepts.json')
    
    # Построение онтологии
    ontology_graph = build_ontology(concepts)
    
    # Визуализация
    # visualize_ontology(ontology_graph)
    # visualize_interactive(ontology_graph)
    pyvis_draggable(ontology_graph)
    
    # Дополнительная информация о графе
    print(f"Всего статей: {len(concepts)}")
    print(f"Всего связей: {ontology_graph.number_of_edges()}")

if __name__ == "__main__":
    main()