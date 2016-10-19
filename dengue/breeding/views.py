import base64
import mimetypes
import pytz
from datetime import datetime

from .models import Source
from taiwan.models import Substitute

from django.conf import settings
from django.contrib.gis.geos import Point
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from boto.s3.connection import S3Connection
from boto.s3.key import Key

tw_tz = pytz.timezone('Asia/Taipei')

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

def photo_to_s3(user_uuid, source_uuid, photo_obj):
    photo_name = photo_obj._name
    photo_content = photo_obj.read()
    photo_mime = mimetypes.guess_type(photo_name)[0]
    if 'image' not in photo_mime:
        return ""

    photo_type = photo_name.split('.')[-1]
    conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    bucket = conn.get_bucket('dengue-backend')
    k = Key(bucket)
    k.key = 'breeding_source/' + user_uuid + '_' + source_uuid + '.' + photo_type
    k.set_metadata("Content-Type", photo_mime)
    k.set_contents_from_string(photo_content)
    k.set_acl("public-read")
    return photo_content, k.generate_url(expires_in=0, query_auth=False)


class SourceCollection(APIView):

    parser_classes = (MultiPartParser,)

    def post(self, request):
        userprofile = request.user.userprofile
        photo_obj = request.data.get('photo', '')
        source_type = request.data.get('source_type', '')
        lng = request.data.get('lng', 0)
        lat = request.data.get('lat', 0)
        address = request.data.get('address', '')
        modified_address = request.data.get('modified_address', '')
        description = request.data.get('description', '')

        if photo_obj == '' or source_type == '' or lng == 0 or lat == 0:
            return Response({"detail": "請填寫完整孳生源資料"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            source_point = Point(float(lng), float(lat), srid=4326)
            substitute = Substitute.objects.filter(mpoly__intersects=source_point)[0]
        except:
            return Response({"detail": "經緯度錯誤"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        breeding_source = Source(userprofile=userprofile)
        photo_content, photo_url = photo_to_s3(userprofile.user_uuid, \
                                               str(breeding_source.source_uuid), \
                                               photo_obj)
        if photo_url == "":
            return Response({"detail": "照片上傳錯誤"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        photo_base64 = base64.b64encode(photo_content)

        breeding_source.photo_url = photo_url
        breeding_source.photo_base64 = photo_base64
        breeding_source.source_type = source_type
        breeding_source.lng = lng
        breeding_source.lat = lat
        breeding_source.address = address
        breeding_source.modified_address = modified_address
        breeding_source.village_name = substitute.v_name
        breeding_source.description = description
        breeding_source.save()

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        qualified_status = request.GET.get('qualified_status', '')
        before_timestamp = request.GET.get('before_timestamp', '')
        limit = request.GET.get('limit', 10)

        if qualified_status == '':
            qualified_status = ['待審核', '已通過', '未通過']
        else:
            qualified_status = qualified_status.split(',')

        try:
            before_timestamp = datetime.fromtimestamp(float(before_timestamp))
        except:
            before_timestamp = timezone.now()

        try:
            limit = int(limit)
        except:
            limit = 10

        source_filter = Source.objects.filter(
            userprofile=request.user.userprofile,
            qualified_status__in=qualified_status,
            created_at__lt=before_timestamp).order_by('-updated_at')[:limit]

        res_data = list()
        for source in source_filter:
            source_dict = model_to_dict(source, exclude=\
                                        ['userprofile', 'created_at', 'updated_at', 'location'])
            source_dict['created_at'] = str(source.created_at.astimezone(tw_tz))
            source_dict['timestamp'] = str(source.created_at.astimezone(tw_tz).timestamp())
            res_data.append(source_dict)


        return Response(res_data, status=status.HTTP_200_OK)

class SourceTotal(APIView):

    def get(self, request):
        qualified_status = request.GET.get('qualified_status', '')

        if qualified_status == '':
            qualified_status = ['待審核', '已通過', '未通過']
        else:
            qualified_status = qualified_status.split(',')

        total = Source.objects.filter(
            userprofile=request.user.userprofile,
            qualified_status__in=qualified_status).count()
        res_data = {'total': total}
        return Response(res_data, status=status.HTTP_200_OK)

class AdminSourceCollection(APIView):

    if settings.DEBUG == "False":
        authentication_classes = (SessionAuthentication, BasicAuthentication)
    else:
        authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    permission_classes = (IsAdminUser,)

    def get(self, request):
        phone = request.GET.get('phone', '')
        if phone == '':
            source = Source.objects.filter(qualified_status="待審核").order_by('?')[0]
        else:
            try:
                source = Source.objects.filter(userprofile__phone=phone,
                                           qualified_status="待審核").order_by('?')[0]
            except:
                return Response([], status=status.HTTP_200_OK)

        source_filter = Source.objects.filter(userprofile=source.userprofile,
                                              qualified_status="待審核")
        res_data = list()
        for source in source_filter:
            source_dict = model_to_dict(source, fields=['photo_url'])
            source_dict['source_uuid'] = str(source.source_uuid)
            res_data.append(source_dict)

        return Response(res_data, status=status.HTTP_200_OK)

    def put(self, request):
        breeding_source_list = request.data.get('breeding_source_list', list())
        for source_dict in breeding_source_list:
            source = get_object_or_404(Source, source_uuid=source_dict['source_uuid'])
            source.qualified_status = source_dict['qualified_status']
            source.save()
        return Response(status=status.HTTP_200_OK)

