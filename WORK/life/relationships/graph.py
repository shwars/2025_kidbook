import os
import json
import re
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
MD_DIR = SCRIPT_DIR / "../../../KIDBOOK/life/relationships"
MD_DIR = MD_DIR.resolve()
GRAPH_FILE = SCRIPT_DIR / "concept_graph.json"
IMAGE_FILE = SCRIPT_DIR / "concept_graph.png"


def debug_paths():
    print("\n[DEBUG] Пути:")
    print(f"Директория скрипта: {SCRIPT_DIR}")
    print(f"Директория с MD-файлами: {MD_DIR}")
    print(f"Существует MD_DIR: {MD_DIR.exists()}")
    if MD_DIR.exists():
        print(f"Файлы в MD_DIR: {len(list(MD_DIR.glob('*.md')))} .md файлов")


def extract_links(md_content: str) -> list:
    links = []
    pattern = r'\[.*?\]\((?!http)(.*?\.md)\)'
    for match in re.finditer(pattern, md_content):
        link = match.group(1)
        link = Path(link).stem.replace('-', ' ')
        links.append(link)
    return links


def build_concept_graph():
    debug_paths()

    if not MD_DIR.exists():
        print(f"\nОШИБКА: Директория {MD_DIR} не найдена!")
        return None

    md_files = list(MD_DIR.glob("*.md"))
    if not md_files:
        print("\nОШИБКА: Нет .md файлов в директории!")
        return None

    print(f"\nНайдено .md файлов: {len(md_files)}")

    graph = {"nodes": [], "links": []}
    concepts = [f.stem.replace('-', ' ') for f in md_files]

    for concept in concepts:
        graph["nodes"].append({"id": concept})
        print(f"Добавлен узел: {concept}")

    link_counter = 0
    for md_file in md_files:
        concept = md_file.stem.replace('-', ' ')
        try:
            content = md_file.read_text(encoding='utf-8')
            links = extract_links(content)

            print(f"\nФайл: {md_file.name}")
            print(f"Найдены ссылки: {links}")

            for target in links:
                if target in concepts and target != concept:
                    graph["links"].append({
                        "source": concept,
                        "target": target
                    })
                    link_counter += 1

        except Exception as e:
            print(f"ОШИБКА при обработке {md_file.name}: {str(e)}")
            continue

    connected_nodes = set()
    for link in graph["links"]:
        connected_nodes.add(link["source"])
        connected_nodes.add(link["target"])

    initial_nodes = len(graph["nodes"])
    graph["nodes"] = [node for node in graph["nodes"] if node["id"] in connected_nodes]

    print(f"\nУдалено изолированных узлов: {initial_nodes - len(graph["nodes"])}")
    print(f"Всего связей найдено: {link_counter}")

    with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    return graph


def visualize_graph(graph):
    if not graph or not graph["nodes"]:
        print("\nНевозможно визуализировать: граф пуст")
        return

    G = nx.DiGraph()

    G.add_nodes_from(n["id"] for n in graph["nodes"])
    G.add_edges_from((l["source"], l["target"]) for l in graph["links"])

    plt.figure(figsize=(25, 25))
    pos = nx.spring_layout(G, k=1.5, seed=42, iterations=100)

    nx.draw_networkx_nodes(
        G, pos,
        node_size=4000,
        node_color='#00b894',
        alpha=0.9
    )

    nx.draw_networkx_edges(
        G, pos,
        edge_color='#636e72',
        width=2,
        arrows=True,
        arrowsize=30
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_family='Arial',
        font_weight='bold'
    )

    plt.title("Граф связей между понятиями", fontsize=25, pad=20)
    plt.axis('off')
    plt.savefig(IMAGE_FILE, bbox_inches='tight', dpi=150)
    plt.close()

    print(f"\nГраф сохранен как: {IMAGE_FILE}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("ГЕНЕРАТОР ГРАФА СВЯЗЕЙ v2.0")
    print("=" * 50)

    graph = build_concept_graph()

    if graph:
        visualize_graph(graph)
        print("\nГотово! Проверьте файлы:")
        print(f"- JSON: {GRAPH_FILE}")
        print(f"- Изображение: {IMAGE_FILE}")
    else:
        print("\nЗавершено с ошибками. Граф не построен!")