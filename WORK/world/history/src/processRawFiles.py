import os
from preprocessHtml import preprocessHtml

IN_DIR = "./rawHtml/"
OUT_DIR = "./processedFiles/"

def main():
    for directory, _, files in os.walk(IN_DIR):
        for fileName in files:
            outText = ""
            with open(str(os.path.join(directory, fileName)), "r") as file:
                html = file.read()
                outText = preprocessHtml(html)

            with open(str(os.path.join(OUT_DIR, fileName.replace(".html", ".md"))), "w") as file:
                file.write(outText)

if __name__ == "__main__":
    main()
