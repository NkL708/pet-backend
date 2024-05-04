import feedparser
import requests
from bs4 import BeautifulSoup


def fetch_article_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all("p", class_="box-paragraph__text")
    return "".join(paragraph.get_text() for paragraph in paragraphs)


def get_feed(url: str):
    return feedparser.parse(url)
