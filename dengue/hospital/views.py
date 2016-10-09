from .models import Hospital

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.forms.models import model_to_dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class HospitalNearby(APIView):

    def get(self, request):
        lng = request.GET.get('lng', '')
        lat = request.GET.get('lat', '')

        try:
            lng = float(lng)
            lat = float(lat)
        except:
            return Response({"detail": "經緯度錯誤"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        point = Point(lng, lat, srid=4326)
        hospital_set = Hospital.objects\
            .annotate(distance=Distance('location', point))\
            .filter(location__distance_lte=(point, D(km=5)))\
            .order_by('distance')

        res_data = []
        for hospital in hospital_set:
            hospital_dict = model_to_dict(hospital, exclude=['hospital_uuid', 'location', 'objects'])
            hospital_dict['distance'] = str(hospital.distance)
            res_data.append(hospital_dict)
        return Response(res_data, status=status.HTTP_200_OK)
