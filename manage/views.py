from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from userkey.models import userProgress
from .models import problem, customerModel, senarioInfo
class getCustomers(APIView):
    def get(self,request):
        k=request.headers.get("key")
        if k == None:
            return Response(status=400)
        try:
            key = k[:16]
            index = int(k[16:])
            user=userProgress.objects.get(id=index)
            assert(key==user.problemKey)
        except:
            return Response(data={"message":"INVALID KEY"},status=404)
        try:
            data=problem.object.filter(senarioNum=user.senarioNumber).get(today=user.progress)
        except:
            return Response(data={"message":"DONE"},status=200)
        return Response(data=data.data)

    def post(self,request):
        k = request.headers.get("key")
        if k == None:
            return Response(status=400)
        try:
            key = k[:16]
            index = int(k[16:])
            user = userProgress.objects.get(id=index)
            assert (key == user.problemKey)
        except:
            return Response(data={"message": "INVALID KEY"}, status=404)
        accepted=request.data.GET("accepted")
        rejected=request.data.GET("rejected")
        work=request.data.GET("action")
        today=user.progress
        today_customer=problem.object.filter(senarioNum=user.senarioNumber).get(today=today)
        today_customer_checker={today_customer[i*6:(i+1)*6] for i in range(len(today_customer)//6)}
        waiting_line = [user.waitings[i*6:(i+1)*6] for i in range(len(user.waitings)//6)]
        waiting_customer_datas=[customerModel.objects.get(id=int(CID)) for CID in waiting_line]

        # check 15min passed
        to_delete=[]
        for idx,w in waiting_customer_datas:
            if w.today <= today-16:
                to_delete.append(idx)
        for idx in to_delete:
            user.rejectedNum += 1
            user.waitingTimeSquare += 225
            waiting_line.pop(idx)
            waiting_customer_datas.pop(idx)

        # do rejected
        for r in rejected:
            if r in today_customer_checker:
                today_customer_checker.remove(r)
                user.rejectedNum += 1
            elif r in waiting_line:
                ind = waiting_line.index(r)
                waiting_line.pop(ind)
                user.rejectedNum+=1
                user.waitingTimeSquare += (today-waiting_customer_datas.pop(ind).today)**2

        # get accepted.
        senarioinfo=senarioInfo.objects.get(id=user.senarioNumber-1)
        capacity=senarioinfo.customer_capacity
        for r in accepted:
            if r in today_customer_checker:
                if len(waiting_line) == capacity:
                    break
                waiting_line.append(r)
                today_customer_checker.remove(r)

        itemstatus = user.itemstatus
        itemnums = [int(itemstatus[])]
        part_timer = senarioinfo.part_timer
        p = 0
        for w in work:
            if p == part_timer:
                break
            p+=1
            if len(w)<6:





        return Response()
# Create your views here.
