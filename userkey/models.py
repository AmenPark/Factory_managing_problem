from django.db import models

class userKey(models.Model):
    uniqueKey = models.CharField(max_length=64, unique=True)
    userEmail = models.EmailField(unique = True)
    bestScore = models.DecimalField(default = 0)

class userScore(models.Model):
    problemkey = models.ForeignKey(userProgress, on_delete=True)
    sellScore = models.IntegerField(default=0)
    speedScore = models.IntegerField(default=0)
    penaltyScore = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

class userProgress(models.Model):
    user=models.ForeignKey(userKey, on_delete=True)
    problemKey=models.CharField(max_length=16)
    senarioNumber = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    end=models.BooleanField(default=False)



# Create your models here.
