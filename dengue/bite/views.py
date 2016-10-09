from .models import DengueBite

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class BiteCollection(APIView):

    def post(self, request):
        lng = request.data.get('lng', '')
        lat = request.data.get('lat', '')

        try:
            lng = float(lng)
            lat = float(lat)
        except:
            return Response({"detail": "經緯度錯誤"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        bite = DengueBite(userprofile=request.user.userprofile,
                          lng=lng,
                          lat=lat)
        bite.save()
        return Response(status=status.HTTP_201_CREATED)
