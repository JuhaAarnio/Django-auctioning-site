# Generated by Django 2.2.5 on 2019-11-06 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20191103_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='auction_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='bidder',
            field=models.IntegerField(),
        ),
    ]
