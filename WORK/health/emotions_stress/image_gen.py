
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import re
import os
import base64


auth_key = ""


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
    with open('./topics/' + path, 'r') as file:
        text = file.read()
        return markdown_to_plain_text(text)


def generate_image_for_text(text, filename):
    with GigaChat(credentials=auth_key, verify_ssl_certs=False) as giga:

        query = "Сгенерируй картинку размером 600 на 600 пикселей к этому тексту. \
            Текст объясняет ребенку понятие понятным для него языком. \
            Картинка не должна содержать много текста, максимум заголовок понятия.\n\n"

        payload = Chat(
            messages=[Messages(role=MessagesRole.USER, content=query + text)],
            temperature=0.7,
            max_tokens=100,
            function_call="auto",
        )

        response = giga.chat(payload)

        match = re.search(r'src="([^"]+)"', response.choices[0].message.content)
        if match:
            image_id = match.group(1)
            # print(image_id)
        else:
            print(f"No image in response for file: {filename}, response is {response}")
            exit()

        img = giga.get_image(image_id)
        imagename = os.path.splitext(filename)[0]

        with open('./topics/' + imagename + '.jpg', mode="wb") as fd:
            fd.write(base64.b64decode(img.content))

        print(f"For file {filename} image is saved: {imagename}")


def main():
    files = [f for f in os.listdir('./topics') if f.endswith(".md")]
    print(files)
    for file in files:
        print(f"current file is: {file}, {files.index(file)}")
        generate_image_for_text(get_text(file), file)



if __name__ == "__main__":
    main()