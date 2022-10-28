from django.db import models

class userKey(models.Model):
    uniquekey = models.CharField(max_length=32, unique=True)
    useremail = models.EmailField(unique = True)
    bestscore = models.DecimalField()

class userScore(models.Model):
    user=models.ForeignKey(userKey, on_delete=True)
    score_1 = models.DecimalField()
    score_2 = models.DecimalField()
    score_3 = models.DecimalField()
    score_4 = models.DecimalField()

class userProgress(models.Model):
    user=models.ForeignKey(userKey, on_delete=True)
    userkey=models.CharField(max_length=16)
    senarioNumber = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    end=models.BooleanField(default=False)


# Create your models here.
