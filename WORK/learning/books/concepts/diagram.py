import json


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_mermaid(data):
    lines = ["graph LR;"]

    for entity, relations in data.items():
        for relation, targets in relations.items():
            if relation == "ссылка":
                continue
            for target in targets:
                f_entity = set_format(entity)
                f_relation: str = set_format(relation)
                f_target = set_format(target)
                lines.append(f"  {f_entity} -->|{f_relation}| {f_target};")

    return "\n".join(lines)


def set_format(s: str):
    return "_".join(s.split())


def main():
    input_file = "concepts.json"
    output_file = "diagram.mmd"

    try:
        data = load_json(input_file)
        mermaid_code = generate_mermaid(data)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(mermaid_code)

        print(f"Mermaid-диаграмма сохранена в файл {output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
