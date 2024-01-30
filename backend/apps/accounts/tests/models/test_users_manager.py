import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_create_with_no_email():
    assert User.objects.count() == 0

    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password="test")

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_with_no_password():
    assert User.objects.count() == 0

    with pytest.raises(ValueError):
        User.objects.create_user(email="test@exemple.fr", password=None)

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_user():
    assert User.objects.count() == 0

    user = User.objects.create_user(email="test@exemple.fr", password="test")

    assert User.objects.count() == 1
    assert user.email == "test@exemple.fr"
    assert user.password != "test"
    assert user.is_confirm is False


@pytest.mark.django_db
def test_create_superuser_with_no_email():
    assert User.objects.count() == 0

    with pytest.raises(ValueError):
        User.objects.create_superuser(email=None, password="test")

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_superuser_with_no_password():
    assert User.objects.count() == 0

    with pytest.raises(ValueError):
        User.objects.create_superuser(email="test@exemple.fr", password=None)

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_create_super_user():
    assert User.objects.count() == 0

    user = User.objects.create_superuser(
        email="test@exemple.fr", password="test"
    )

    assert User.objects.count() == 1
    assert user.email == "test@exemple.fr"
    assert user.password != "test"
    assert user.is_confirm is False
