from django.db import models
from django.db.models.fields import TextField, URLField


class Article(models.Model):
    source_url: URLField = URLField(max_length=255, verbose_name="Источник")
    short_text: TextField = TextField(verbose_name="Сокращённый текст")
    full_text: TextField = TextField(verbose_name="Полный текст")
