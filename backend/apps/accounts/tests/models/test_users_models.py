import pytest

from apps.accounts.factories import UserFactory
from apps.accounts.models import User


@pytest.mark.django_db
def test_user_email_with_email_instead_of_username():
    assert User.objects.count() == 0
    user = User.objects.create(email="test@exemple.fr")

    assert User.objects.count() == 1
    assert user.username is None


@pytest.mark.django_db
def test_user_email_with_username_raise_error():
    assert User.objects.count() == 0

    with pytest.raises(TypeError):
        User.objects.create(username="test")

    assert User.objects.count() == 0


@pytest.mark.django_db
def test_user__str__print_email():
    user = UserFactory(email="test@example.com")
    assert user.__str__() == "test@example.com"
