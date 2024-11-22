def get_articles_for_date(
    articles: list[dict[str, str]], target_date: str
) -> list[dict[str, str]]:
    return [
        article
        for article in articles
        if article["published_date"] == target_date
    ]

