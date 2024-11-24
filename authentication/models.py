from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.manager import AccountManager


class Account(AbstractUser):
    first_name = None
    last_name = None

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = AccountManager()

    def __str__(self):
        return self.username
