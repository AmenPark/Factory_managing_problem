from django.db import models


'''             
                시나리오 1번.
                data = {
                        "max_time" : 120,
                        "part_timer" : 5,
                        "items": 6,
                        "customer_capacity" : 10,
                        "max_item" : 8}
                #2
                data = {
                        "max_time" : 1200,
                        "part_timer" : 20,
                        "items": 50,
                        "customer_capacity" : 25,
                        "max_item" : 50}
                #3
                data = {
                        "max_time" : 1200,
                        "part_timer" : 30,
                        "items": 200,
                        "customer_capacity" : 50,
                        "max_item" : 500}
'''
class senarioInfo(models.Model):
    max_time=models.IntegerField()
    part_timer=models.IntegerField()
    items=models.IntegerField()
    customer_capacity=models.IntegerField()
    max_item=models.IntegerField()

class problem(models.Model):
    senarioNum=models.IntegerField()
    today=models.IntegerField()
    JSONdata=models.JSONField(default='{}')
    Customers=models.CharField(max_length=200,default="")

class customerModel(models.Model):
    today=models.IntegerField()
    needs=models.CharField(max_length=200,default="")