from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]
