# Generated by Django 4.2.16 on 2024-10-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orders',
            name='OrderNum',
            field=models.IntegerField(unique=True),
        ),
    ]
