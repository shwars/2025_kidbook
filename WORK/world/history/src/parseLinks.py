import os
import re

DIRECTORY = "./processedFiles/"


def main():
    links = {}
    for _, _, files in os.walk(DIRECTORY):
        for fileName in files:
            with open(str(os.path.join(DIRECTORY, fileName)), "r") as file:
                txt = file.read()
            links[fileName] = set(re.findall(r"\(\..*?\)", txt))

    for k, v in links.items():
        print(f"\"{k}\": {[x[3: -1] for x in list(v)]}")

if __name__ == "__main__":
    main()
