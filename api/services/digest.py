from datetime import date

from django.db import transaction

from ..models import Article, Digest
from .date_utils import (
    get_current_datetime,
    get_yesterday_date,
    published_on_specific_date,
)
from .gpt import generate_summary, generate_title
from .parser import fetch_article_text, get_feed


def generate_daily_digest(url: str) -> None:
    yesterday_date = get_yesterday_date(get_current_datetime())

    articles = []
    for feed_article in get_feed(url).entries:
        if published_on_specific_date(feed_article.published, yesterday_date):
            article_text = fetch_article_text(feed_article.link)
            short_text = generate_summary(article_text)
            article = save_article(feed_article.link, short_text, article_text)
            articles.append(article)
    if articles:
        save_digest(articles)


def save_article(source_url: str, short_text: str, full_text: str) -> Article:
    with transaction.atomic():
        article, created = Article.objects.get_or_create(
            source_url=source_url,
            defaults={"short_text": short_text, "full_text": full_text},
        )
        if created:
            article.save()
    return article


def save_digest(articles: list[Article]) -> Digest:
    with transaction.atomic():
        digest, created = Digest.objects.get_or_create(
            publication_date=date.today(),
            defaults={"title": generate_title(articles)},
        )
        if created:
            for article in articles:
                digest.articles.add(article)
            digest.save()
    return digest
