import pymorphy3
import os

# Путь к директории
PATH = 'pages'
# Если есть такой файл, то имена берутся оттуда, иначе берутся имена файлов
# Это нужно для создания приоритетов названий файлвв, если одно является частью другого
LINKS = 'names.md'

# Алгоритм Ахо-Корасик
class TrieNode:
    def __init__(self):
        self.children = {}
        self.output = []
        self.fail = None

def build_automaton(keywords):
    root = TrieNode()

    for keyword in keywords:
        node = root
        for char in keyword:
            node = node.children.setdefault(char, TrieNode())
        node.output.append(keyword)

    queue = []
    for node in root.children.values():
        queue.append(node)
        node.fail = root

    while queue:
        current_node = queue.pop(0)
        for key, next_node in current_node.children.items():
            queue.append(next_node)
            fail_node = current_node.fail
            while fail_node and key not in fail_node.children:
                fail_node = fail_node.fail
            next_node.fail = fail_node.children[key] if fail_node else root
            next_node.output += next_node.fail.output

    return root


def search_text(text, keywords, patterns):
    root = build_automaton(keywords)
    result = {keywords[i]: [patterns[i]] for i in range(len(keywords))}

    current_node = root
    for i, char in enumerate(text):
        while current_node and char not in current_node.children:
            current_node = current_node.fail

        if not current_node:
            current_node = root
            continue

        current_node = current_node.children[char]
        for keyword in current_node.output:
            result[keyword].append(i - len(keyword) + 1)

    return result

def get_pages(folder):
    pages = {}
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            path = os.path.join(folder, filename)
            with open(path, "r") as f:
                text = f.read()
                pages[filename] = text
    return pages

def get_names(pages):
    names = []
    for name, body in pages.items():
        names.append(name)
    return names

def add_links(pages, patterns):
    new_pages = {}

    morph = pymorphy3.MorphAnalyzer()

    parsed_patterns = []
    for pattern in patterns:
        parsed_patterns.append(' '.join([morph.parse(word)[0].normal_form for word in pattern.split(' ')]))

    for filename, text in pages.items():
        parsed_text = [morph.parse(word.strip('(),.-#:" '))[0].normal_form for word in text.split(' ')]

        new_text = ' '.join(parsed_text)

        # Первае значение это паттерн в изначальной форме
        result = search_text(new_text, parsed_patterns, patterns)

        found = {}

        for key, pos in result.items():
            found[key] = [pos[0]]
            for i in range(1, len(pos)):
                cnt = 0
                for i in range(pos[i]):
                    if new_text[i] == ' ':
                        cnt += 1
                found[key].append(cnt)

        words = [word for word in text.split()]

        for key, pos in found.items():
            word_cnt = len(key.split())
            for j in range(1, len(pos)):
                if morph.parse(words[pos[j]].strip('(),.-#:" '))[0].normal_form == key.split()[0]:
                    for i in range(word_cnt):
                        if i == 0:
                            words[pos[j]] = '[[' + ' '.join([words[pos[j] + i] for i in range(word_cnt)]) + '|' + pos[0] + ']]'
                        else:
                            words[pos[j] + i] = ' '


        words = list(filter(lambda x: x != ' ', words))

        res_text = ' '.join(words)
        new_pages[filename] = res_text

    return new_pages

def update_pages(folder, new_pages):
    for filename, text in new_pages.items():
        path = os.path.join(folder, filename)
        with open(path, "w") as file:
            file.write(text)

if __name__ == '__main__':
    patterns = []
    pages = get_pages(PATH)
    if os.path.isfile(LINKS):
        with open(LINKS, 'r') as f:
            for line in f:
                patterns.append(line.rstrip())
    else:
        patterns = get_names(pages)

    new_pages = add_links(pages, patterns)

    update_pages(PATH, new_pages)
