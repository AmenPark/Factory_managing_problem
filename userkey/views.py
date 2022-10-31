from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import userKey,userScore,userProgress
import hashlib
import random
import string

class startTest(APIVIEW):
    def post(self,request):
        data = request.data
        try:
            email=data["address"]
            encoded_string = email.encode()
            digest = hashlib.sha256(encoded_string).hexdigest()
            obj = userKey(uniqueKey=digest, userEmail=email)
        except:
            return(Response(data={"message":"address must be email"},status=status.HTTP_400_BAD_REQUEST))
        obj.save()
        return (Response(data={"key":digest},status=200))


class startProblem(APIVIEW):
    def post(self,request):
        data = request.data
        try:
            key = data["key"]
            user=userKey.objects.get(uniqueKey=key)
        except:
            return(Response(data={"message":"Invalid key"},status=400))
        try:
            p = data["problem"]
            problemkey = "".join(random.choices(string.digits + string.ascii_letters, k=16))
            if p==1:
                obj=userProgress(user=user,problemkey=problemkey,senarioNumber=1)
                data = {"key" : problemkey,
                        "max_time" : 120,
                        "part_timer" : 3,
                        "items": ["chocolate", "milk", "cake", "ramen", "kimchi", "kimbab", "coffee","hotdog"]
                        "customer_capacity" : 10,
                        "max_item" : 5}
                obj.save()
                scoreObj=userScore(problemkey=obj)
                scoreObj.save()
                return (Response(data=data,status=200))

            return(Response(data={"message":"Bad Request"},status=400))
        except:
            return(Response(data={"message":"Bad Request"},status=400))

# Create your views here.
