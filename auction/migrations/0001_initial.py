# Generated by Django 2.2.5 on 2019-10-12 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('minimum_price', models.FloatField()),
                ('deadline_date', models.DateTimeField()),
                ('creator_id', models.IntegerField()),
            ],
        ),
    ]