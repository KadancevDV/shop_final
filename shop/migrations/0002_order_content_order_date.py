# Generated by Django 4.1 on 2022-09-05 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='content',
            field=models.TextField(max_length=4096, null=True, verbose_name='Состав заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
