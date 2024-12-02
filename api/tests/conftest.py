from datetime import datetime
from typing import Any

import pytest


@pytest.fixture
def sample_articles() -> list[dict[str, Any]]:
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
