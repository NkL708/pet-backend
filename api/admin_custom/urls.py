from django.urls import path

from .views import generate_digest_view

urlpatterns = [
    path("generate-digest/", generate_digest_view, name="generate_digest"),
]
