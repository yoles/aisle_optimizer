from django.urls import path, include

urlpatterns = [
    path("authentication/", include("apps.authentication.urls")),
    path("accounts/", include("apps.accounts.urls")),
]
