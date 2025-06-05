import json
from pathlib import Path

concepts_path = Path(r"C:\Users\miron\Downloads\concepts.json")
output_dir = Path(r"C:\Users\miron\Downloads\articles")

def get_template(term):
    return f"""# {term}

👶 *Объяснение для детей:*

Здесь будет понятное и интересное объяснение, чтобы даже десятилетний ребёнок понял, что такое **{term}**.

---

📚 **Что это такое?**  
(Описание понятия, как оно работает, зачем нужно.)

🌍 **Где это встречается?**  
(Примеры из реального мира.)

🧠 **Интересные факты:**  
- Факт 1  
- Факт 2  
- Факт 3

✏️ **Связанные понятия:**  
(Появятся автоматически позже.)
"""

def load_concepts(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get("concepts", [])

def create_article(term, output_dir):
    filename = output_dir / f"{term}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(get_template(term))

def main():
    concepts = load_concepts(concepts_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    for term in concepts:
        create_article(term, output_dir)

if __name__ == '__main__':
    main()
