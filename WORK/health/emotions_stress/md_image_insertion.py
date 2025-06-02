import os
from pathlib import Path
import re 
import random
from PIL import Image

directory = Path("./topics")


def markdown_to_plain_text(md_text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', md_text)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def get_text(path):
    with open(path, 'r') as file:
        text = file.read()
        return markdown_to_plain_text(text)


def count_paragraphs(md_text):
    paragraphs = [p.strip() for p in md_text.split('\n\n') if p.strip()]
    return len(paragraphs)


def resize_images(new_width = 600, new_height = 600):
    files = [f for f in os.listdir('./topics') if f.endswith(".jpg")]

    for file in files:
        img = Image.open('./topics/' + file)
        img = img.resize((new_width, new_height))
        img.save('./topics/' + os.path.splitext(file)[0] + '.jpg')



def insert_images(md_directory = './topics'):
    
    md_files = list(Path(md_directory).glob("*.md"))
    
    for md_file in md_files:

        stem = md_file.stem
        img_path = None
        
        potential_img = Path(md_directory) / f"{stem}.jpg"
        if potential_img.exists():
            img_path = potential_img
        
        if not img_path:
            print(f"For file {md_file.name} image wasn't found")
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                  
        insert_position = random.randint(1, len(paragraphs))
        img_markdown = f"\n\n![Изображение {stem}]({img_path.name.replace(' ', '%20')})\n\n"
        paragraphs.insert(insert_position, img_markdown)
        new_content = '\n\n'.join(paragraphs)
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Image inserted in {md_file.name}")


if __name__ == "__main__":
    resize_images()
    insert_images()