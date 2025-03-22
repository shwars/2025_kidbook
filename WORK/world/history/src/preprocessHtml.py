import sys
from bs4 import BeautifulSoup as bs

def preprocessHtml(html: str):
    soup = bs(html, "html.parser")

    for a in soup.find_all("a"):
        a.string = f"[{a.text}]({a['href']})"

    for bold in soup.find_all("strong"):
        bold.string = f"**{bold.text}**"

    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.string = f"- {li.text}"

    return soup.text


if __name__ == "__main__":
    html = sys.stdin.read()
    print(preprocessHtml(html))

