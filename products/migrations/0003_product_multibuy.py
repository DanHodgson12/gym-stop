# Generated by Django 3.2.25 on 2024-03-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20240327_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='multibuy',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
