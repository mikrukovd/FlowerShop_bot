from django.db import models


class Composition(models.Model):
    name = models.CharField(
        verbose_name='Цветок',
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )


    def __str__(self):
        return f"{self.name}"


class Occasion(models.Model):
    name = models.CharField(
        verbose_name='Повод',
        blank=False,
        null=False,
        max_length=100,
        unique=True,
    )


    def __str__(self):
        return f"{self.name}"
    

    class Meta:
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'


class Bouquet(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Фото букета',
        blank=False,
        null=False
    )
    discription = models.CharField(
        verbose_name="Описание",
        max_length=1000,
        blank=False,
        null=False
    )
    price = models.IntegerField(
        verbose_name='Цена',
        blank=False,
        null=False,
    )
    composition = models.ManyToManyField(
        Composition,
        verbose_name='Состав',
        related_name='bouquets',
        blank=False,
    )
    occasion = models.ForeignKey(
        Occasion,
        verbose_name='Повод',
        related_name='bouquets',
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    
    
    def __str__(self):
        return f"{self.name} {self.price}"


    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'
