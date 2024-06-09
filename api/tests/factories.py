import factory
from factory.django import DjangoModelFactory

from ..models.article import Article
from ..models.digest import Digest
from .mocks import MockArticle
from .utils import random_past_datetime


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    source_url = factory.Faker("url")
    short_text = factory.Faker("sentence")
    full_text = factory.Faker("text")


class DigestFactory(DjangoModelFactory):
    class Meta:
        model = Digest

    publication_date = factory.Faker("date")
    title = factory.Faker("sentence")

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for article in extracted:
                self.articles.add(article)


class MockFeedArticleFactory(factory.Factory):
    class Meta:
        model = MockArticle

    link = factory.Faker("url")
    published = factory.LazyFunction(random_past_datetime)
