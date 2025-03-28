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
        
llm = GigaChat(
    credentials=getpass('INSERT_AUTH.KEY:'), 
    model="GigaChat-Max", 
    verify_ssl_certs=False)

template = """
    Твоя задача по заданному понятию сгенерировать красочную статью в виде markdown странички для детской энциклопедии. Заданное понятие - {query}
    Объяснение должно быть для десятилетнего ребенка. При оформлении используй обязательно смайлики!!!! Оформи странички красочно!
    Страничка должна быть довольно объемной, можно использовать метафоры (с животными, природой), примеры из различных сфер жизни (дружба, семья, работа).
    При этом важно понимать структуру энциклопедии. Представь что в ней есть набор из 15 страниц с ключевыми темами (включительно та, которую тебе нужно сейчас описать): Доброта, Смелость, Честность, Щедрость, Эмпатия, Лень, Лицемерие, Жадность, Вспыльчивость, Высокомерие, Сдержанность, Любопытство, Замкнутость, Терпение, Ответственность.
    Так вот, тебе нужно описывать заданное понятие, используя в своем повествовании упоминания вышеперечисленных качеств, например, при сопоставлении или анализе любых связей, влияний. Не надо переусердствовать и упоминать слишком много качеств.
"""

with open("concepts.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    prompt = PromptTemplate(input_variables=['query'], template=template).format(query=line)
    response = llm.chat(prompt)
    create_markdown_file(f'{line.split()[0]}.md', response.choices[0].message.content)