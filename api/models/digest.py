from django.db import models
from django.db.models import ManyToManyField
from django.db.models.fields import CharField, DateField


class Digest(models.Model):
    title: CharField = CharField(max_length=300, verbose_name="Заголовок")
    publication_date: DateField = DateField(verbose_name="Дата публикации")
    articles: ManyToManyField = ManyToManyField(
        "Article", verbose_name="Новости", related_name="digests"
    )
