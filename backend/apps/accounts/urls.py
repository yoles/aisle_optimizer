from django.urls import path

from apps.accounts.views import Register

app_name = "accounts"

urlpatterns = [path("register/", Register.as_view(), name="register")]
