from rest_framework.response import Response
from rest_framework.views import APIView
from userkey.models import userProgress, userKey
from manage.models import senarioInfo

class getScore(APIView):
    def get(self, request):
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

        if user.end == False:
            return Respons(data={"sell":0,"efficiency":0,"penalty":0,"score":0})
        senarioinfo = senarioInfo.objects.get(id=user.senarioNumber-1)
