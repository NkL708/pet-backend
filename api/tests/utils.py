from datetime import datetime, timedelta

from ..services.date_utils import (
    DATE_FORMAT,
    SERVER_TIMEZONE,
    get_current_datetime,
)
from .faker_setup import fake
from .mocks import MockArticle


def random_past_datetime() -> str:
    days_ago = fake.random_int(min=0, max=2)
    time_ago = timedelta(
        hours=fake.random_int(min=0, max=23),
        minutes=fake.random_int(min=0, max=59),
        seconds=fake.random_int(min=0, max=59),
    )
    past_datetime = (
        get_current_datetime("Europe/Moscow")
        - timedelta(days=days_ago)
        - time_ago
    )

    return past_datetime.strftime(DATE_FORMAT)


def count_yesterday_articles(articles: list[MockArticle]) -> int:
    current_datetime = datetime.now()
    yesterday_date = (current_datetime - timedelta(days=1)).date()
    yesterday_articles_count = sum(
        1
        for article in articles
        if datetime.strptime(article.published, DATE_FORMAT)
        .astimezone(SERVER_TIMEZONE)
        .date()
        == yesterday_date
    )

    return yesterday_articles_count
