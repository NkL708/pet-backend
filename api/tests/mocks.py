class MockArticle:
    def __init__(self, link, published):
        self.link = link
        self.published = published


class MockFeed:
    def __init__(self, entries):
        self.entries = entries