import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User


def test_register_with_get_request_should_raise_error():
    client = APIClient()
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 405


def test_register_with_put_request_should_raise_error():
    client = APIClient()
    response = client.put(reverse("accounts:register"))
    assert response.status_code == 405


def test_register_with_patch_request_should_raise_error():
    client = APIClient()
    response = client.patch(reverse("accounts:register"))
    assert response.status_code == 405


def test_register_with_delete_request_should_raise_error():
    client = APIClient()
    response = client.delete(reverse("accounts:register"))
    assert response.status_code == 405


@pytest.mark.django_db
def test_register_fail_with_empty_credentials():
    assert User.objects.count() == 0

    client = APIClient()
    response = client.post(reverse("accounts:register"), data={})

    assert response.status_code == 403
    assert response.json().get("detail") == "Email and password are required."
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_fail_with_empty_email():
    assert User.objects.count() == 0
    data = {"password": "test"}
    client = APIClient()
    response = client.post(reverse("accounts:register"), data=data)

    assert response.status_code == 403
    assert response.json().get("detail") == "Email and password are required."
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_fail_with_empty_password():
    assert User.objects.count() == 0

    data = {"email": "test@example.fr"}
    client = APIClient()
    response = client.post(reverse("accounts:register"), data=data)

    assert response.status_code == 403
    assert response.json().get("detail") == "Email and password are required."
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_fail_with_weak_password():
    assert User.objects.count() == 0

    data = {"email": "test@example.fr", "password": "azerty123"}
    client = APIClient()
    with pytest.raises(ValidationError):
        client.post(reverse("accounts:register"), data=data)

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_fail_with_too_short_password():
    assert User.objects.count() == 0

    data = {"email": "test@example.fr", "password": "T3St!"}
    client = APIClient()

    with pytest.raises(ValidationError):
        client.post(reverse("accounts:register"), data=data)

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_successful():
    assert User.objects.count() == 0

    data = {"email": "test@example.fr", "password": "T3st!S3CuR3"}
    client = APIClient()
    response = client.post(reverse("accounts:register"), data=data)

    assert response.status_code == 200

    user = response.json()
    assert user.get("email") == "test@example.fr"
    assert user.get("is_confirm") is False
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_password_is_encrypted():
    data = {"email": "test@example.fr", "password": "T3st!S3CuR3"}
    client = APIClient()
    client.post(reverse("accounts:register"), data=data)

    user = User.objects.get(email="test@example.fr")
    assert user.password is not None
    assert user.password != data.get("password")
