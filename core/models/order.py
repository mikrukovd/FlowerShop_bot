from django.db import models
from .user import User
from .bouquet import Bouquet
from django.core.validators import RegexValidator


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='orders',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    name = models.CharField(
        verbose_name='Имя заказчика',
        max_length=100,
        blank=False,
        null=False
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
        validators=[RegexValidator(r'^(7|8)\d{10}$')],
        blank=False,
        null=False
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=300,
        blank=False,
        null=False
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.SET_NULL,
        verbose_name='Букет',
        related_name='orders',
        blank=False,
        null=True
    )
    removed_flower = models.CharField(
        verbose_name='Удаленный цветок',
        max_length=100,
        blank=True,
        null=True
    )
    is_deliverd = models.BooleanField(
        verbose_name='Доставлен',
        blank=False,
        null=False,
        default=False
    )
    order_date = models.DateTimeField(
        verbose_name='Дата заказа',
        blank=False,
        null=False,
        auto_now_add=True,
    )
    delivery_date = models.DateTimeField(
        verbose_name='Дата доставки',
        blank=False,
        null=False,
    )


    def __str__(self):
        return f"{self.id} {self.user.name} {self.is_deliverd}"


    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
