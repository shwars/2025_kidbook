import os
from modules.config import settings

files_to_create = [
    # ===== Formal science =====
    "formal_science.md",
    # Math
    "math.md",
    "algebra.md",
    "statistics.md",
    
    # Logic
    "logic.md",
    
    # Computer science
    "computer_science.md",
    "information_technology.md",
    "artificial_intelligence.md",
    
    # ===== Natural science =====
    "natural_science.md",
    "physics.md",
    "chemistry.md",
    "biology.md",
    
    # ===== Science of life =====
    "science_of_life.md",
    "medicine.md",
    "genetics.md",
    "botanics.md",
    "ecology.md",
    
    # ===== Social science =====
    "social_science.md",
    "psychology.md",
    "sociology.md",
    "economics.md",
    "history.md",
    
    # ===== Earth and space science =====
    "earth_and_space_science.md",
    "astronomy.md",
    "geology.md",
    "geography.md",
]


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