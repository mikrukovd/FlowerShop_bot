from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    id_tg = models.BigIntegerField(
        verbose_name='Id аккаунта',
        primary_key=True,
        unique=True
    )
    name = models.CharField(
        verbose_name='Логин',
        max_length=100,
    )
    registered_at = models.DateTimeField(
        verbose_name='Дата и время регистрации',
        auto_now_add=True,
    )
    
    
    def __str__(self):
        return f"{self.name}"
