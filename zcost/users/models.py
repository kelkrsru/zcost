from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс переопределенного пользователя."""
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True
    )

    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20,
        unique=True
    )
