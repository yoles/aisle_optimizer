from django.urls import reverse
from rest_framework.test import APIClient


def test_get_csrf_without_authentication():
    client = APIClient()

    response = client.get(reverse("authentication:get_csrf"))

    assert response.status_code == 200
    assert response.has_header("X-CSRFToken") is True
    data = response.json()
    assert data["detail"] == "CSRF cookie set"
