from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/api/", include("api.admin_custom.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
