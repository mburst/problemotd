from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("", include("social_django.urls", namespace="social")),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("admin/", admin.site.urls),
]
