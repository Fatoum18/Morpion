# Generated by Django 4.2.8 on 2023-12-25 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Morpion', '0003_game_board_game_current_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1_games', to='Morpion.user'),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2_games', to='Morpion.user'),
        ),
    ]
