# Generated by Django 5.0 on 2023-12-23 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_destination_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='headers',
            field=models.CharField(max_length=100),
        ),
    ]
