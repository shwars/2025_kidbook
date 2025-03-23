from gigachat import GigaChat
from langchain_core.prompts import PromptTemplate
import os 
from getpass import getpass

from pathlib import Path

script_dir = Path(__file__).resolve().parent

destination_folder = script_dir.parents[3] / "KIDBOOK" / "life" / "personal_qualities"

def create_markdown_file(filename, content):
    destination_folder.mkdir(parents=True, exist_ok=True)  
    filepath = destination_folder / filename  
    filepath.write_text(content, encoding="utf-8")
    print(f"Файл создан: {filepath}")
        
llm = GigaChat(credentials=getpass('Insert_api:'), verify_ssl_certs=False)
template = """
    Твоя задача по заданному понятию сгенерировать статью-обьяснение этого понятия так, как будто ты обьясняешь 5 летнему ребенку. 
    
    Понятие: {query}
"""

with open("concepts.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    prompt = PromptTemplate(input_variables=['query'], template=template).format(query=line)
    response = llm.chat(prompt)
    create_markdown_file(f'{line.split()[0]}.md', response.choices[0].message.content)

    