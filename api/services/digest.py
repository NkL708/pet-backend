from datetime import datetime, timezone
from typing import Optional

import feedparser
import requests


def fetch_rss_feed(url: str, timeout: int = 10) -> list:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    feed = feedparser.parse(response.text)

    articles = []
    for entry in feed.entries:
        published_date = convert_to_utc(entry.get("published"))
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


def convert_to_utc(
    date_str: str, date_format: str = "%a, %d %b %Y %H:%M:%S %z"
) -> Optional[datetime]:
    if date_str is None:
        return None
    try:
        local_date = datetime.strptime(date_str, date_format)
        return local_date.astimezone(timezone.utc)
    except ValueError:
        return None
