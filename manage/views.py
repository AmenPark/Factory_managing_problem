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
        if user.end == True:
            return Response(data={"message":"DONE"})

        accepted=request.data.GET("accepted")
        rejected=request.data.GET("rejected")
        work=request.data.GET("action")
        today=user.progress
        today_customer=problem.object.filter(senarioNum=user.senarioNumber).get(today=today)
        today_customer_checker={today_customer[i*6:(i+1)*6] for i in range(len(today_customer)//6)}
        waiting_line = [user.waitings[i*6:(i+1)*6] for i in range(len(user.waitings)//6)]
        waiting_customer_datas=[customerModel.objects.get(id=int(CID)) for CID in waiting_line]
        sold_count = user.soldNum
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
        itemnums = [int(itemstatus[i*3:(i+1)*3]) for i in range(len(itemstatus)//3)]
        part_timer = senarioinfo.part_timer
        failed=0
        for p, w in enumerate(work):
            if p == part_timer:
                break
            if len(w)<6:
                idx = int(w)
                itemnums[idx] = senarioinfo.max_item
            else:
                try:
                    waiting_line.remove(w)
                    customer = customerModel.objects.get(id=int(w))
                    needs = customer.needs
                    needs_list = [int(needs[i*3:(i+1)*3]) for i in range(len(needs)//3)]
                    next_itemnums=[0]*len(itemnums)
                    try:
                        for idx, (x,y) in enumerate(zip(itemnums,needs_list)):
                            assert x>=y
                            next_itemnums[idx] = x-y
                        itemnums = next_itemnums
                        user.waitingTimeSquare += (today - customer.today)**2
                        sold_count += sum(needs_list)
                    except:
                        failed+=1
                        user.waitingTimeSquare += (today - customer.today) ** 2
                        user.rejectedNum += 1
                except:
                    pass


        today += 1
        user.progress = today
        user.soldNum=sold_count
        user.waitings = "".join(waiting_line)
        user.failedNum += failed
        user.itemstatus = "".join(map(lambda x : str(x).zfill(3),itemnums))

        user.save()

        if today == senarioinfo.max_time:
            user.end = True


        return Response(data={"serve failed":failed, "time":today})
# Create your views here.
