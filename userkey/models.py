from django.db import models

class userKey(models.Model):
    uniqueKey = models.CharField(max_length=64, unique=True)
    userEmail = models.EmailField(unique = True)
    bestScore = models.DecimalField(max_digits=6, decimal_places=2, default=0)

class userProgress(models.Model):
    user=models.ForeignKey(userKey, on_delete=models.CASCADE)
    problemKey=models.CharField(max_length=16)
    senarioNumber = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    end=models.BooleanField(default=False)
    itemstatus = models.CharField(max_length=200,default="")
    waitings=models.CharField(max_length=200, default="")
    soldNum=models.IntegerField(default=0)
    waitingTimeSquare=models.IntegerField(default=0)
    rejectedNum=models.IntegerField(default=0)
    failedNum=models.IntegerField(default=0)




# Create your models here.
