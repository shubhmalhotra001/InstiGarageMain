# Generated by Django 4.1.2 on 2022-11-21 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='highestBid',
            field=models.IntegerField(default=0, verbose_name='owner_id'),
        ),
    ]
