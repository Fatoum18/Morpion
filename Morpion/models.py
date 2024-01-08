from django.db import models
from datetime import datetime
from Morpion.utils import generate_winning_combinations


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
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    config = models.ForeignKey(GameConfig, on_delete=models.CASCADE)
    board = models.JSONField(default=list, blank=True)
    current_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_player', null=True, blank=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_games',null=True, blank=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_games',null=True, blank=True)
    symbol = models.JSONField(blank=True,null=True)
    symbol = models.JSONField(blank=True,null=True)
    status = models.CharField(max_length=20, default="NOT_STARTED")
    
    
    
class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True) 
    score = models.PositiveIntegerField() 
    config = models.ForeignKey(GameConfig, on_delete=models.CASCADE) 
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.now, blank=True)
    
class Notification(models.Model):
    id =  models.AutoField(primary_key=True)
    content =  models.TextField()
    title =  models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =  models.DateTimeField(auto_now_add=True) 
    
class Invitation(models.Model):
    id =  models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, related_name='sender_invitation', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_invitation', on_delete=models.CASCADE)
    game =  models.ForeignKey(Game, on_delete=models.CASCADE)
    message = models.TextField(blank=True) 
    created_at =  models.DateTimeField(auto_now_add=True) 
    accepted =  models.BooleanField(default=False) 


def create_or_inc_score(game):
    player_lb = Leaderboard.objects.filter(player=game.current_player,config=game.config).first()
    if player_lb:
       player_lb.score = player_lb.score + 1
    else:
        player_lb = Leaderboard(player=game.current_player,score=1,config=game.config)
    player_lb.save()
 
            
 
def get_game_config_or_create (size,alignment):  
    game_config = GameConfig.objects.filter(grid_size=size,alignment=alignment).first()
    if not game_config:
        game_config = GameConfig(grid_size=size,alignment=alignment)
        game_config.save()
    return game_config

def send_invitation(sender_id,game_id, friend_id, title,message):
    invitation =  Invitation(sender=User(sender_id),recipient=User(friend_id),game=Game(game_id),message=message)
    invitation.save()
    create_notification(friend_id,title,message)
    
def create_notification(user_id,title,content):
    notification =  Notification(user=User(user_id),title=title,content=content)
    notification.save()