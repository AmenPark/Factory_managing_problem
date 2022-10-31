from django.db import models

class problem(models.Model):
    senarioNum=models.IntegerField()
    today=models.IntegerField()
    data=models.JSONField(default='{}')