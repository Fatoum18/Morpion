# Generated by Django 4.1.5 on 2023-12-15 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Morpion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='access_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]