import pytest

from apps.accounts.factories import UserFactory
from apps.accounts.serializers import UserSerializer


@pytest.mark.django_db
def test_user():
    user = UserFactory(id=1, email="test@example.fr", password="test")
    user_serializer = UserSerializer(user)

    assert len(user_serializer.data.keys()) == 3
    assert user_serializer.data.get("id") == 1
    assert user_serializer.data.get("email") == "test@example.fr"
    assert user_serializer.data.get("is_confirm") is False
