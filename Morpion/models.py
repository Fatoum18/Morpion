from django.db import models
from datetime import datetime


class User(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, default="")

class GameConfig(models.Model):
    id =  models.AutoField(primary_key=True)
    grid_size = models.IntegerField(default=3)
    alignment = models.IntegerField(default=3)
    created_at =  models.DateField(default=datetime.now, blank=True) 
    
      
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    visibility = models.CharField(max_length=20, default="PUBLIC")
    access_code = models.CharField(max_length=20,blank=True)
    created_at = models.DateField(default=datetime.now, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    config = models.ForeignKey(GameConfig, on_delete=models.CASCADE)
    board = models.JSONField(default=list, blank=True)
    current_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_player', null=True, blank=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_games',null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_games',null=True, blank=True)

    def check_winner(self):
        # Define winning combinations
        size = self.config.grid_size  # Assuming the board is square
        winning_combinations = []

        # Rows and Columns
        for i in range(size):
            row = [i * size + j for j in range(size)]
            col = [j * size + i for j in range(size)]
            winning_combinations.append(row)
            winning_combinations.append(col)

        # Diagonals
        diagonal1 = [i * (size + 1) for i in range(size)]
        diagonal2 = [i * (size - 1) + (size - 1) for i in range(size)]
        winning_combinations.append(diagonal1)
        winning_combinations.append(diagonal2)

        # Check for a winner
        for combo in winning_combinations:
            if all(self.board[combo[i]] == self.board[combo[i + 1]] != ' ' for i in range(len(combo) - 1)):
                return True  # We have a winner!

        return False  # No winner yet
       
def get_game_config_or_create (size,alignment):  
    game_config = GameConfig.objects.filter(grid_size=size,alignment=alignment).first()
    if not game_config:
        game_config = GameConfig(grid_size=size,alignment=alignment)
        game_config.save()
    return game_config
