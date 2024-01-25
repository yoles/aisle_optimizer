from django.urls import path

from apps.authentication.views import get_csrf_view

app_name = "authentication"

urlpatterns = [
    path("get_csrf", get_csrf_view, name="get_csrf"),
]
