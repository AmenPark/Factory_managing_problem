from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import userKey,userProgress
from manage.models import senarioInfo
import hashlib
import random
import string

class startTest(APIView):
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


class startProblem(APIView):
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
            senariodata = senarionInfo.objects.get(id=p-1)
            obj=userProgress(user=user,problemkey=problemkey,senarioNumber=1)
            index=obj.id
            problemkey += str(index).zfill(16)
            data = {"key" : problemkey,
                    "max_time" : senariodata.max_time,
                    "part_timer" : senariodata.part_timer,
                    "items": senariodata.items,
                    "customer_capacity" : senariodata.customer_capacity,
                    "max_item" : senariodata.max_item}
            obj.save()
            return (Response(data=data,status=200))
        except:
            return(Response(data={"message":"Bad Request"},status=400))

# Create your views here.
