import pytest
from rest_framework import status

from api.models import Article, Digest


@pytest.mark.integration
@pytest.mark.django_db
def test_article_viewset_get(client, article):
    response = client.get(f"/api/articles/{article.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["source_url"] == article.source_url


@pytest.mark.integration
@pytest.mark.django_db
def test_article_viewset_post(client):
    data = {
        "source_url": "https://example.com/article1",
        "short_text": "Short description",
        "full_text": "Full description of the article.",
    }

    response = client.post("/api/articles/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.count() == 1
    assert Article.objects.first().source_url == data["source_url"]


@pytest.mark.integration
@pytest.mark.django_db
def test_article_viewset_put(client, article):
    updated_data = {
        "source_url": "https://example.com/updated-article",
        "short_text": "Updated description",
        "full_text": "Updated full description.",
    }

    response = client.put(f"/api/articles/{article.id}/", updated_data)

    assert response.status_code == status.HTTP_200_OK
    article.refresh_from_db()
    assert article.source_url == updated_data["source_url"]
    assert article.short_text == updated_data["short_text"]
    assert article.full_text == updated_data["full_text"]


@pytest.mark.integration
@pytest.mark.django_db
def test_article_viewset_patch(client, article):
    partial_data = {"short_text": "Partially updated description"}

    response = client.patch(f"/api/articles/{article.id}/", partial_data)

    assert response.status_code == status.HTTP_200_OK
    article.refresh_from_db()
    assert article.short_text == partial_data["short_text"]


@pytest.mark.integration
@pytest.mark.django_db
def test_article_viewset_delete(client, article):
    response = client.delete(f"/api/articles/{article.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Article.objects.count() == 0


@pytest.mark.integration
@pytest.mark.django_db
def test_digest_viewset_get(client, article):
    digest = Digest.objects.create(
        title="Digest Title", publication_date="2024-12-04"
    )
    digest.articles.add(article)

    response = client.get(f"/api/digests/{digest.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == digest.title
    assert len(response.data["articles"]) == 1
    assert response.data["articles"][0]["source_url"] == article.source_url
