from django.conf.urls import url
from bite import views

urlpatterns = [
    url(r'^$', views.BiteCollection.as_view()),
]
