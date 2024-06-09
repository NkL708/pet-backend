import pytest

from ..models.article import Article
from ..models.digest import Digest
from ..services.digest import generate_daily_digest
from .utils import count_yesterday_articles


@pytest.mark.django_db
def test_generate_daily_digest(
    frozen_time,
    mock_get_feed_fixture: dict,
    mock_fetch_article_text_fixture: str,
    mock_generate_summary_fixture: str,
    mock_generate_title_fixture: str,
    mock_feed_articles: list,
):
    generate_daily_digest("https://example.com/feed")

    expected_articles_count = count_yesterday_articles(mock_feed_articles)

    assert Article.objects.count() == expected_articles_count
    assert Digest.objects.count() == 1
    digest = Digest.objects.first()
    assert digest is not None, "Digest is None, but expected a Digest object."
    assert digest.articles.count() == expected_articles_count
