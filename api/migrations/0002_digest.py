# Generated by Django 5.0.1 on 2024-03-20 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Digest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Заголовок"),
                ),
                (
                    "publication_date",
                    models.DateField(verbose_name="Дата публикации"),
                ),
                (
                    "articles",
                    models.ManyToManyField(
                        related_name="digests",
                        to="api.article",
                        verbose_name="Новости",
                    ),
                ),
            ],
        ),
    ]
