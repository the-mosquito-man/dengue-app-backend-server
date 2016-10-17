from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class AdminLoginPage(APIView):

    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request,  *args, **kwargs):
        return Response(template_name='admin_breeding_source.html')

