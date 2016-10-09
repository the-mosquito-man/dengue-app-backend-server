from django.conf.urls import url
from hospital import views

urlpatterns = [
    url(r'^nearby/$', views.HospitalNearby.as_view()),
]
