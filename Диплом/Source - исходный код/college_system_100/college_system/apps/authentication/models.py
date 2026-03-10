from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Администратор"
        ACCOUNTANT = "accountant", "Бухгалтер"
        CURATOR = "curator", "Куратор"
        TEACHER = "teacher", "Преподаватель"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TEACHER,
        verbose_name="Роль",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"


