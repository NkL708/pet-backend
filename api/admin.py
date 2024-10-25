from django.contrib import admin

from .admin_custom.admin_config import ArticleAdmin, DigestAdmin
from .models import Article, Digest

admin.site.register(Article, ArticleAdmin)
admin.site.register(Digest, DigestAdmin)
