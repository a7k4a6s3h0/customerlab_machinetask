# Generated by Django 5.0 on 2023-12-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_account_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]