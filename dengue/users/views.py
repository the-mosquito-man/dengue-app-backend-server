import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UserProfile

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class UserFast(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        user_uuid = uuid.uuid4()
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=user_uuid, password=password)

        userprofile = UserProfile(user=user, user_uuid=user_uuid)
        userprofile.save()

        token_tuple = Token.objects.get_or_create(user=user)
        res_data = {"user_uuid": user_uuid,
                    "token": token_tuple[0].key}
        return Response(res_data, status=status.HTTP_201_CREATED)

class UserManually(APIView):

    def post(self, request):
        user_uuid = request.data.get('user_uuid', '')
        name = request.data.get('name', '')
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')

        if user_uuid == '' or name == '' or password == '' or len(phone) != 10:
            return Response({"detail": "請填寫完整註冊訊息"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        for phone_char in phone:
            try:
                int(phone_char)
            except:
                return Response({"detail": "請填寫完整註冊訊息"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = request.user
        userprofile = user.userprofile

        ## 判斷使用者的註冊訊息user_uuid是否正確、是否已經註冊過了、是否有重複的電話
        userprofile_filter = UserProfile.objects.filter(phone=phone)
        if userprofile.user_uuid != user_uuid:
            return Response({"detail": "系統錯誤"}, status=status.HTTP_409_CONFLICT)
        elif userprofile.is_signup == True:
            return Response({"detail": "此帳號已註冊"}, status=status.HTTP_409_CONFLICT)
        elif len(userprofile_filter) >= 1:
            return Response({"detail": "此手機已註冊"}, status=status.HTTP_409_CONFLICT)

        user.set_password(password)
        user.email = email
        user.save()

        userprofile.name = name
        userprofile.phone = phone
        userprofile.is_signup = True
        userprofile.save()

        ## 重新產生token
        token = Token.objects.get(user=user)
        token.delete()
        token_tuple = Token.objects.get_or_create(user=user)
        res_data = {"token": token_tuple[0].key}

        return Response(res_data, status=status.HTTP_201_CREATED)

class UserLogin(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')

        userprofile = get_object_or_404(UserProfile, phone=phone)
        user = authenticate(username=userprofile.user_uuid, password=password)
        token = Token.objects.get(user=user)
        res_data = {"token": token.key}

        return Response(res_data, status=status.HTTP_200_OK)
