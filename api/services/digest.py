from datetime import date, datetime

from django.db import transaction

from ..models.article import Article
from ..models.digest import Digest
from .gpt import generate_summary, generate_title
from .parser import fetch_article_text, get_feed

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


def generate_daily_digest(url: str) -> None:
    articles = []
    for feed_article in get_feed(url).entries:
        if published_today(feed_article.published):
            article_text = fetch_article_text(feed_article.link)
            short_text = generate_summary(article_text)
            article = save_article(feed_article.link, short_text, article_text)
            articles.append(article)
    if articles:
        save_digest(articles)


def published_today(published_date: str) -> bool:
    article_date = datetime.strptime(published_date, DATE_FORMAT)
    current_date = datetime.now(tz=article_date.tzinfo)
    return (
        article_date.day == current_date.day
        and article_date.month == current_date.month
        and article_date.year == current_date.year
    )


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
