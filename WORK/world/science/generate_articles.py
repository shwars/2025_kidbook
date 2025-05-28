import os
import json
from pathlib import Path

def get_project_paths():
    """Get the base paths for the project."""
    current_dir = Path(__file__).parent
    base_dir = current_dir.parent.parent.parent
    work_dir = base_dir / 'WORK' / 'world' / 'science'
    kidbook_dir = base_dir / 'KIDBOOK' / 'world' / 'science'
    return work_dir, kidbook_dir

def load_concepts(work_dir):
    """Load concepts from JSON file."""
    concepts_file = work_dir / 'concepts.json'
    try:
        with open(concepts_file, 'r', encoding='utf-8') as f:
            return json.load(f)['concepts']
    except FileNotFoundError:
        print(f"Error: concepts.json not found at {concepts_file}")
        return []
    except json.JSONDecodeError:
        print(f"Error: concepts.json is not valid JSON")
        return []

def create_article_file(kidbook_dir, term):
    """Create a new article file with proper formatting."""
    filename = kidbook_dir / f"{term}.md"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {term}\n\n(Описание пока отсутствует.)\n")
        return True
    except Exception as e:
        print(f"Error creating file {filename}: {e}")
        return False

def add_related_terms(filename, term, concepts):
    """Add related terms to an existing article."""
    try:
        with open(filename, 'r+', encoding='utf-8') as f:
            content = f.read()
            related_terms = []
            
            for linked_term in concepts:
                if linked_term != term and linked_term in content:
                    link = f"[{linked_term}](./{linked_term}.md)"
                    if link not in content:
                        related_terms.append(link)
            
            if related_terms:
                if "**Связанные понятия:**" not in content:
                    f.write("\n\n**Связанные понятия:** " + ", ".join(related_terms))
        return True
    except Exception as e:
        print(f"Error updating file {filename}: {e}")
        return False

def main():
    work_dir, kidbook_dir = get_project_paths()
    
    # Ensure directories exist
    kidbook_dir.mkdir(parents=True, exist_ok=True)
    
    # Load concepts
    concepts = load_concepts(work_dir)
    if not concepts:
        return
    
    # Process each concept
    for term in concepts:
        filename = kidbook_dir / f"{term}.md"
        if not filename.exists():
            if create_article_file(kidbook_dir, term):
                print(f"Created new article: {term}")
        
        if add_related_terms(filename, term, concepts):
            print(f"Updated article: {term}")

if __name__ == '__main__':
    main()