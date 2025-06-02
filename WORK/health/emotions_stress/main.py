""" Автоматическая генерация текстов """

import os
import asyncio
import json
from duck_ai import DuckAI, Models


async def generate(concept, duck, concepts):
    result = []
    chat = duck.create_new_chat(Models.GPT_4_MINI)
    
    msg = f"""
    Вот тебе список всех понятий {concepts}, связанных со стрессом. 
    Объясни максимально подробно для десятилетнего ребенка что такое {concept} на русском языке. 
    Приведи примеры ситуаций, когда десятилетний ребенок может испытать данную эмоцию.
    Пиши текст с такой структурой:
    - определение
    - примеры
    - способы решения
    - заключение

    Оформи каждый пункт выдели и добавь соответсвующие эмодзи.
    По возможности для объяснения понятия ссылайся на другие понятия из списка.
    
    Расставь ссылки на другие понятия из списка в формате гиперссылки markdown [понятие](понятие.md).
    """

    async for chunk in chat.send(msg):
        result.append(chunk)


    filename = f"{concept}.md"
    path = "../../../KIDBOOK/health/emotions_stress"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path + filename, "w") as out_file:
        out_file.write("".join(result))


async def main():
    duck = DuckAI()

    with open('concepts_with_categories.json') as file:
        json_data = file.read()

    data = json.loads(json_data)
    # for concept in data['negative_emotion']:
    #     await generate(concept, duck, data['negative_emotion'])
    #     await asyncio.sleep(5)
    for concept in data['stress']:
        await generate(concept, duck, data['stress'])
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
