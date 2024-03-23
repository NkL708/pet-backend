from django.urls import include, path

urlpatterns = [
    path("token/", include("api.urls.token")),
    path("user/", include("api.urls.user")),
    path("users/", include("api.urls.users")),
    path("article/", include("api.urls.article")),
    path("digest/", include("api.urls.digest")),
]
