# Generated by Django 4.1.2 on 2022-11-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet',
            field=models.IntegerField(default=10000),
        ),
    ]