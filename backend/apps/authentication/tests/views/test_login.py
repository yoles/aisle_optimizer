import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.factories import UserFactory


def test_login_get_method_must_fail():
    client = APIClient()
    response = client.get(reverse("authentication:login"))

    assert response.status_code == 405


def test_login_put_method_must_fail():
    client = APIClient()
    response = client.put(reverse("authentication:login"))

    assert response.status_code == 405


def test_login_patch_method_must_fail():
    client = APIClient()
    response = client.patch(reverse("authentication:login"))

    assert response.status_code == 405


def test_login_delete_method_must_fail():
    client = APIClient()
    response = client.delete(reverse("authentication:login"))

    assert response.status_code == 405


def test_login_without_password():
    client = APIClient()

    credentials = {"email": "test@exemple.fr", "password": ""}
    response = client.post(reverse("authentication:login"), data=credentials)

    assert response.status_code == 403
    assert response.json() == {"detail": "Email and password is required."}


def test_login_without_email():
    client = APIClient()

    credentials = {"email": "", "password": "T3st!123"}
    response = client.post(reverse("authentication:login"), data=credentials)

    assert response.status_code == 403
    assert response.json() == {"detail": "Email and password is required."}


@pytest.mark.django_db
def test_login_with_invalid_credentials():
    client = APIClient()

    credentials = {"email": "test@exemple.fr", "password": "T3st!123"}
    response = client.post(reverse("authentication:login"), data=credentials)

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credentials."}


@pytest.mark.django_db
def test_login_with_valid_credentials():
    client = APIClient()
    credentials = {"email": "test@exemple.fr", "password": "T3st!123"}
    UserFactory(**credentials)

    response = client.post(reverse("authentication:login"), data=credentials)

    assert response.status_code == 200
    assert response.json() == {"detail": "Successfully logged in."}
    assert "_auth_user_id" in client.session
