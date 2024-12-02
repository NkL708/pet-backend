from datetime import datetime

import feedparser
import requests


def fetch_rss_feed(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    feed = feedparser.parse(response.text)

    articles = []
    for entry in feed.entries:
        published_date_str = entry.get("published")
        published_date = None
        if published_date_str:
            try:
                published_date = datetime.strptime(
                    published_date_str, "%a, %d %b %Y %H:%M:%S %z"
                )
            except ValueError:
                pass

        if any(
            (entry.get("title"), entry.get("link"), entry.get("published"))
        ):
            articles.append(
                {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published_date": published_date,
                }
            )

    return articles


def get_articles_for_date(
    articles: list[dict[str, str]], target_date: str
) -> list[dict[str, str]]:
    target_date_as_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    return [
        article
        for article in articles
        if isinstance(article["published_date"], datetime)
        and article["published_date"].date() == target_date_as_date
    ]
