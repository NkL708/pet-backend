import time
from datetime import datetime, timezone

import pytest
import requests

from ..services.digest import fetch_rss_feed, get_articles_for_date


@pytest.mark.unit
def test_fetch_rss_feed(mock_requests_get, rss_content):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 3
    expected_articles = [
        {
            "title": "News 1",
            "link": "https://example.com/article1",
            "published_date": datetime.strptime(
                "Wed, 27 Nov 2024 13:11:36 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
        {
            "title": "News 2",
            "link": "https://example.com/article2",
            "published_date": datetime.strptime(
                "Tue, 26 Nov 2024 13:11:36 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
        {
            "title": "News 3",
            "link": "https://example.com/article3",
            "published_date": datetime.strptime(
                "Wed, 27 Nov 2024 13:11:36 +0300", "%a, %d %b %Y %H:%M:%S %z"
            ),
        },
    ]

    for article, expected in zip(articles, expected_articles):
        assert article["title"] == expected["title"]
        assert article["link"] == expected["link"]
        assert article["published_date"] == expected["published_date"]


@pytest.mark.unit
def test_fetch_rss_feed_empty_feed(mock_requests_get, empty_rss_content):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = empty_rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


@pytest.mark.unit
def test_fetch_rss_feed_missing_fields(
    mock_requests_get, rss_content_with_missing_fields
):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = rss_content_with_missing_fields

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 2
    assert articles[0]["title"] == ""
    assert articles[0]["link"] == "https://example.com/article1"
    assert articles[0]["published_date"] is None
    assert articles[1]["title"] == "Sample Title 2"
    assert articles[1]["link"] == ""
    assert articles[1]["published_date"] is None


@pytest.mark.unit
def test_fetch_rss_feed_invalid_format(mock_requests_get, invalid_rss_content):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = invalid_rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


@pytest.mark.unit
def test_fetch_rss_feed_empty_response(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = ""

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 0


@pytest.mark.unit
def test_fetch_rss_feed_http_error(mock_requests_get):
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_rss_feed("https://example.com/rss")


@pytest.mark.unit
def test_fetch_rss_feed_mixed_content(mock_requests_get, mixed_rss_content):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = mixed_rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 1
    assert articles[0]["title"] == "Valid Title"
    assert articles[0]["link"] == "https://example.com/article1"
    assert articles[0]["published_date"] == datetime.strptime(
        "Tue, 12 Nov 2024 13:11:36 +0300", "%a, %d %b %Y %H:%M:%S %z"
    )


@pytest.mark.unit
def test_fetch_rss_feed_invalid_date_format(
    mock_requests_get, invalid_date_rss_content
):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = invalid_date_rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    assert len(articles) == 1
    assert articles[0]["published_date"] is None


@pytest.mark.unit
def test_get_articles_for_date(articles):
    filtered_articles = get_articles_for_date(articles, "2024-11-03")

    assert len(filtered_articles) == 1
    assert filtered_articles[0]["title"] == "News 1"


@pytest.mark.unit
def test_get_articles_for_date_no_matches(articles):

    filtered_articles = get_articles_for_date(articles, "2024-11-02")
    assert len(filtered_articles) == 0


@pytest.mark.unit
def test_get_articles_for_date_multiple_matches(articles):
    articles.extend(
        [
            {
                "title": "News 4",
                "published_date": datetime.strptime(
                    "Sun, 03 Nov 2024 13:11:36 +0300",
                    "%a, %d %b %Y %H:%M:%S %z",
                ),
            },
            {
                "title": "News 5",
                "published_date": datetime.strptime(
                    "Sun, 03 Nov 2024 18:24:11 +0300",
                    "%a, %d %b %Y %H:%M:%S %z",
                ),
            },
        ]
    )
    filtered_articles = get_articles_for_date(articles, "2024-11-03")
    assert len(filtered_articles) == 3


@pytest.mark.performance
def test_get_articles_for_date_large_dataset():
    articles = [
        {
            "title": f"News {i}",
            "published_date": datetime(
                2024, 11, 3, 10, 0, tzinfo=timezone.utc
            ),
        }
        for i in range(10_000)
    ]

    start_time = time.time()
    filtered_articles = get_articles_for_date(articles, "2024-11-03")
    duration = time.time() - start_time

    assert len(filtered_articles) == 10_000
    assert (
        duration < 1.0
    ), f"Performance test failed, duration: {duration:.2f} seconds"


@pytest.mark.integration
def test_fetch_and_filter_articles(mock_requests_get, rss_content):

    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = rss_content

    articles = fetch_rss_feed("https://example.com/rss")

    filtered_articles = get_articles_for_date(articles, "2024-11-27")

    assert len(filtered_articles) == 2
    assert filtered_articles[0]["title"] == "News 1"
    assert filtered_articles[1]["title"] == "News 3"
