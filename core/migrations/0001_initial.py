
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Цветок')),
            ],
            options={
                'verbose_name': 'Цветок',
                'verbose_name_plural': 'Цветы',
            },
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Повод')),
            ],
            options={
                'verbose_name': 'Повод',
                'verbose_name_plural': 'Поводы',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id_tg', models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Id аккаунта')),
                ('name', models.CharField(max_length=100, verbose_name='Логин')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^(7|8)\\d{10}$')], verbose_name='Номер телефона')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время регистрации')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Bouquet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото букета')),
                ('discription', models.CharField(max_length=1000, verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('composition', models.ManyToManyField(related_name='bouquets', to='bot.composition', verbose_name='Состав')),
                ('occasion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bouquets', to='bot.occasion', verbose_name='Повод')),
            ],
            options={
                'verbose_name': 'Букет',
                'verbose_name_plural': 'Букеты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя заказчика')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^(7|8)\\d{10}$')], verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=300, verbose_name='Адрес')),
                ('is_deliverd', models.BooleanField(default=False, verbose_name='Доставлен')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('delivery_date', models.DateTimeField(verbose_name='Дата доставки')),
                ('bouquet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='bot.bouquet', verbose_name='Букет')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='bot.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-order_date'],
            },
        ),
    ]
