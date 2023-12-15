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
    access_code = models.CharField(max_length=20)
    created_at = models.DateField(default=datetime.now, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    config = models.ForeignKey(GameConfig, on_delete=models.CASCADE)

