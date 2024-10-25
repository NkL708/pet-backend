from django.db import models
from django.db.models import ManyToManyField
from django.db.models.fields import CharField, DateField, TextField, URLField


class Digest(models.Model):
    title: CharField = CharField(max_length=300, verbose_name="Заголовок")
    publication_date: DateField = DateField(verbose_name="Дата публикации")
    articles: ManyToManyField = ManyToManyField(
        "Article", verbose_name="Новости", related_name="digests"
    )


class Article(models.Model):
    source_url: URLField = URLField(max_length=255, verbose_name="Источник")
    short_text: TextField = TextField(verbose_name="Сокращённый текст")
    full_text: TextField = TextField(verbose_name="Полный текст")
