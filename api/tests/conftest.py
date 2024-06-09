import pytest
from freezegun import freeze_time

from .factories import MockFeedArticleFactory
from .mocks import MockFeed


@pytest.fixture(scope="function")
def frozen_time():
    with freeze_time("2024-05-21 00:00:00") as frozen:
        yield frozen


@pytest.fixture
def mock_feed_articles(frozen_time) -> list:
    return MockFeedArticleFactory.create_batch(20)


@pytest.fixture
def mock_get_feed_fixture(mocker, mock_feed_articles: list) -> None:

    def mock_get_feed(url) -> MockFeed:
        return MockFeed(mock_feed_articles)

    mocker.patch("api.services.digest.get_feed", mock_get_feed)


@pytest.fixture
def mock_fetch_article_text_fixture(mocker) -> None:

    def mock_fetch_article_text(url) -> str:
        return "Полный текст статьи"

    mocker.patch(
        "api.services.digest.fetch_article_text", mock_fetch_article_text
    )


@pytest.fixture
def mock_generate_summary_fixture(mocker) -> None:
    def mock_generate_summary(text) -> str:
        return "Краткий текст статьи"

    mocker.patch("api.services.digest.generate_summary", mock_generate_summary)


@pytest.fixture
def mock_generate_title_fixture(mocker) -> None:
    def mock_generate_title(articles) -> str:
        return "Ежедневный дайджест"

    mocker.patch("api.services.digest.generate_title", mock_generate_title)
