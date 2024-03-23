from django.contrib import admin

from .models.article import Article
from .models.digest import Digest


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "short_text_trimmed"]

    def short_text_trimmed(self, obj) -> str:
        words: str = obj.short_text.split()[:10]
        return " ".join(words)

    short_text_trimmed.short_description = "Сокращённый текст"  # type: ignore


class DigestAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "publication_date"]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Digest, DigestAdmin)
