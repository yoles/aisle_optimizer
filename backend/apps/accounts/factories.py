import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ("password",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall(
        "set_password", "default_password"
    )
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name[0]}.{obj.last_name}@example.com"
    )
