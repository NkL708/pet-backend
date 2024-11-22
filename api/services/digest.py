import feedparser
import requests


def get_articles_for_date(
    articles: list[dict[str, str]], target_date: str
) -> list[dict[str, str]]:
    return [
        article
        for article in articles
        if article["published_date"] == target_date
    ]


def fetch_rss_feed(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    feed = feedparser.parse(response.text)

    articles = []
    for entry in feed.entries:
        if any(
            (entry.get("title"), entry.get("link"), entry.get("published"))
        ):
            articles.append(
                {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published_date": entry.get("published", ""),
                }
            )

    return articles
