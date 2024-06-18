from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USER_ROLE_CHOICES = [
        ("customer", "Customer"),
        ("member", "Member"),
        ("admin", "Admin")
    ]
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='customer')

    class Meta:
        ordering = ['id']