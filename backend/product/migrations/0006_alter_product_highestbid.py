# Generated by Django 4.1.2 on 2022-11-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_highestbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='highestBid',
            field=models.IntegerField(default=0, verbose_name='highest_bid_id'),
        ),
    ]
