from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AlterField(
            model_name='bouquet',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Цветок'),
        ),
        migrations.AlterField(
            model_name='occasion',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Повод'),
        ),
    ]
