# Generated by Django 3.2.25 on 2024-05-11 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_subscribed_to_newsletter',
            field=models.BooleanField(default=False),
        ),
    ]
