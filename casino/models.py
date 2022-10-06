from django.db import models
from django.contrib.auth.models import AbstractUser
from casino.helpers import generate_random_key


class User(AbstractUser):
    """
    Custom User model
    """

    identity_key = models.CharField(max_length=256, default=generate_random_key)
    email = models.EmailField(max_length=254, unique=True)
    credit = models.IntegerField(default=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.email
