# Generated by Django 4.2.8 on 2024-01-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Morpion', '0008_alter_game_created_at_notification_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]