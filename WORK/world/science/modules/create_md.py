import os
from modules.links import science_terms

def get_files_to_create() -> list:
    return [term.lower().replace(' ', '_') for term in science_terms]

def is_md_file_exists(directory: str, filename: str) -> bool:
    if not filename.endswith('.md'):
        filename += '.md'
    filepath = os.path.join(directory, filename)
    return os.path.exists(filepath)

def create_md_file(directory: str, filename: str, content: str) -> str | None:
    if not filename.endswith('.md'):
        filename += '.md'
    
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'x', encoding='utf-8') as f:
            f.write(content)
        return filepath
    except OSError as e:
        print(f"Error: {e}")
        return None