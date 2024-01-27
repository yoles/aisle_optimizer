from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str, group=None, **extra_fields
    ):
        """Create, save and return a new user (email and password required)"""
        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_confirm = False
        user.set_password(password)
        user.save(using=self._db)

        if group is not None:
            group.user_set.add(user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("first_name", "admin")
        extra_fields.setdefault("last_name", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


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
    is_confirm = models.BooleanField(
        _("Email Confirmation"),
        default=False,
        help_text=_("Indicates whether this user has confirmed his email. "),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
