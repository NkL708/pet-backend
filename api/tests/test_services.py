from ..services.digest import get_articles_for_date


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

