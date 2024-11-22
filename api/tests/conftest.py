import pytest


@pytest.fixture
def sample_articles() -> list[dict[str, str]]:
    return [
        {"title": "News 1", "published_date": "2024-11-03"},
        {"title": "News 2", "published_date": "2024-11-04"},
        {"title": "News 3", "published_date": "2024-11-05"},
    ]
