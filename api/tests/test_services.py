from unittest.mock import patch

import pytest
import requests

from ..services.digest import fetch_rss_feed, get_articles_for_date


def test_get_articles_for_date(sample_articles):
    filtered_articles = get_articles_for_date(sample_articles, "2024-11-03")

    assert len(filtered_articles) == 1
    assert filtered_articles[0]["title"] == "News 1"


def test_get_articles_for_date_no_matches(sample_articles):

    filtered_articles = get_articles_for_date(sample_articles, "2024-11-02")
    assert len(filtered_articles) == 0


def test_get_articles_for_date_multiple_matches(sample_articles):
    sample_articles.extend(
        [
            {"title": "News 4", "published_date": "2024-11-03"},
            {"title": "News 5", "published_date": "2024-11-03"},
        ]
    )
    filtered_articles = get_articles_for_date(sample_articles, "2024-11-03")
    assert len(filtered_articles) == 3


def test_fetch_rss_feed():
    rss_content = """
    <rss version="2.0">
        <channel>
            <item>
                <title>Sample Title 1</title>
                <link>https://example.com/article1</link>
                <pubDate>Tue, 12 Nov 2024 13:11:36 +0300</pubDate>
            </item>
            <item>
                <title>Sample Title 2</title>
                <link>https://example.com/article2</link>
                <pubDate>Tue, 12 Nov 2024 09:36:27 +0300</pubDate>
            </item>
        </channel>
    </rss>
    """

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = rss_content

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 2

    assert articles[0]["title"] == "Sample Title 1"
    assert articles[0]["link"] == "https://example.com/article1"
    assert articles[0]["published_date"] == "Tue, 12 Nov 2024 13:11:36 +0300"

    assert articles[1]["title"] == "Sample Title 2"
    assert articles[1]["link"] == "https://example.com/article2"
    assert articles[1]["published_date"] == "Tue, 12 Nov 2024 09:36:27 +0300"


def test_fetch_rss_feed_empty_feed():
    empty_rss_content = """
    <rss version="2.0">
        <channel>
            <title>Empty Feed</title>
        </channel>
    </rss>
    """

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = empty_rss_content

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


def test_fetch_rss_feed_missing_fields():
    rss_content_with_missing_fields = """
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

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = rss_content_with_missing_fields

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 2

    assert articles[0]["title"] == ""
    assert articles[0]["link"] == "https://example.com/article1"
    assert articles[0]["published_date"] == ""

    assert articles[1]["title"] == "Sample Title 2"
    assert articles[1]["link"] == ""
    assert articles[1]["published_date"] == ""


def test_fetch_rss_feed_invalid_format():
    invalid_rss_content = """
    <html>
        <body>Not an RSS feed</body>
    </html>
    """

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = invalid_rss_content

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


def test_fetch_rss_feed_empty_response():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = ""

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


def test_fetch_rss_feed_http_error():
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError
        )

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_rss_feed("https://example.com/rss")


def test_fetch_rss_feed_mixed_content():
    mixed_rss_content = """
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
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mixed_rss_content

        articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 1

    assert articles[0]["title"] == "Valid Title"
    assert articles[0]["link"] == "https://example.com/article1"
    assert articles[0]["published_date"] == "Tue, 12 Nov 2024 13:11:36 +0300"
