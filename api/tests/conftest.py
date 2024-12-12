from datetime import datetime
from typing import Any
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from api.models import Article


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def articles() -> list[dict[str, Any]]:
    return [
        {
            "title": "News 1",
            "published_date": datetime.strptime(
                "Sun, 03 Nov 2024 09:45:01 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
        {
            "title": "News 2",
            "published_date": datetime.strptime(
                "Mon, 04 Nov 2024 15:53:42 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
        {
            "title": "News 3",
            "published_date": datetime.strptime(
                "Tue, 05 Nov 2024 21:39:06 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
    ]


@pytest.fixture
def article() -> Article:
    return Article.objects.create(
        source_url="https://example.com/article1",
        short_text="Short description",
        full_text="Full description of the article.",
    )


@pytest.fixture
def rss_content():
    return """
    <rss version="2.0">
        <channel>
            <item>
                <title>News 1</title>
                <link>https://example.com/article1</link>
                <pubDate>Wed, 27 Nov 2024 13:11:36 +0300</pubDate>
            </item>
            <item>
                <title>News 2</title>
                <link>https://example.com/article2</link>
                <pubDate>Tue, 26 Nov 2024 13:11:36 +0300</pubDate>
            </item>
            <item>
                <title>News 3</title>
                <link>https://example.com/article3</link>
                <pubDate>Wed, 27 Nov 2024 13:11:36 +0300</pubDate>
            </item>
        </channel>
    </rss>
    """


@pytest.fixture
def empty_rss_content():
    return """
    <rss version="2.0">
        <channel>
            <title>Empty Feed</title>
        </channel>
    </rss>
    """


@pytest.fixture
def rss_content_with_missing_fields():
    return """
    <rss version="2.0">
        <channel>
            <item>
                <link>https://example.com/article1</link>
            </item>
            <item>
                <title>Sample Title 2</title>
            </item>
        </channel>
    </rss>
    """


@pytest.fixture
def invalid_rss_content():
    return """
    <html>
        <body>Not an RSS feed</body>
    </html>
    """


@pytest.fixture
def mixed_rss_content():
    return """
    <rss version="2.0">
        <channel>
            <item>
                <title>Valid Title</title>
                <link>https://example.com/article1</link>
                <pubDate>Tue, 12 Nov 2024 13:11:36 +0300</pubDate>
            </item>
            <item>
                <invalid>Not a valid item</invalid>
            </item>
        </channel>
    </rss>
    """


@pytest.fixture
def invalid_date_rss_content():
    return """
    <rss version="2.0">
        <channel>
            <item>
                <title>Title with invalid date</title>
                <link>https://example.com/article</link>
                <pubDate>Invalid Date Format</pubDate>
            </item>
        </channel>
    </rss>
    """
